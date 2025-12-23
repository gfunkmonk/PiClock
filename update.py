import os
import re
import subprocess
import sys

print('\nUpdating Python Package Manager')
cmd = [sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip']
print(' '.join(cmd))
subprocess.run(cmd, check=False)
print('\nRemoving old Python Modules')
cmd = [sys.executable, '-m', 'pip', 'uninstall', 'python-metar', '-y']
print(' '.join(cmd))
subprocess.run(cmd, check=False)
print('\nUpdating Python Modules')
cmd = [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt']
print(' '.join(cmd))
subprocess.run(cmd, check=False)

buttonFileName = 'Button/gpio-keys'
print(f'\nChecking {buttonFileName}')
if os.path.isfile(buttonFileName):
    print(f'Setting proper permissions on {buttonFileName}')
    os.chmod(buttonFileName, 0o744)

apikeysFileName = 'Clock/ApiKeys.py'
wuapi_re = re.compile(r'\s*wuapi\s*=')
dsapi_re = re.compile(r'\s*dsapi\s*=')
ccapi_re = re.compile(r'\s*ccapi\s*=')
tmapi_re = re.compile(r'\s*tmapi\s*=')
owmapi_re = re.compile(r'\s*owmapi\s*=')

print(f'\nChecking {apikeysFileName}')
if os.path.isfile(apikeysFileName):
    altered = False
    foundtm = False
    foundowm = False
    newfile = ''
    with open(apikeysFileName, 'r', encoding='utf-8') as apikeys:
        for aline in apikeys:
            if tmapi_re.match(aline):
                foundtm = True
            if owmapi_re.match(aline):
                foundowm = True
            skip_line = False
            if wuapi_re.match(aline):
                print(f'Removing wuapi key from {apikeysFileName}')
                altered = True
                skip_line = True
            if dsapi_re.match(aline):
                print(f'Removing dsapi key from {apikeysFileName}')
                altered = True
                skip_line = True
            if ccapi_re.match(aline):
                print(f'Removing ccapi key from {apikeysFileName}')
                altered = True
                skip_line = True
            if not skip_line:
                newfile += aline

    if not foundtm and not foundowm:
        print('\nThis version of PiClock requires a new weather API key.')
        while True:
            print('Please select your weather provider:')
            print('  <1> OpenWeatherMap.org (https://openweathermap.org/price)')
            print('  <2> Tomorrow.io (https://www.tomorrow.io/weather-api/)')
            print('Selection (1 or 2)')
            try:
                choice = int(input('? '))
                if 1 <= choice <= 2:
                    break
            except ValueError:
                print('Invalid input. Please enter 1 or 2.')
        if choice == 1:
            print('Enter your OpenWeatherMap.org API key.')
            k = input('key: ').strip()
            if len(k) > 1:
                newfile += f"owmapi = '{k}'\n"
                altered = True
        else:
            print('Enter your Tomorrow.io API key.')
            k = input('key: ').strip()
            if len(k) > 1:
                newfile += f"tmapi = '{k}'\n"
                altered = True

    if altered:
        print(f'\nWriting updated {apikeysFileName}')
        with open(apikeysFileName, 'w', encoding='utf-8') as apikeys:
            apikeys.write(newfile)
    else:
        print(f'No changes made to {apikeysFileName}')

try:
    import rpi_ws281x  # noqa: F401
except ModuleNotFoundError:
    print('\nERROR: rpi_ws281x not found')
    print('NeoAmbi.py now uses rpi-ws281x/rpi-ws281x-python')
    print('Please install it as follows:')
    print(f'{sys.executable} -m pip install rpi_ws281x')
