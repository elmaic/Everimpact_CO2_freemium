import requests
from subprocess import Popen
from getpass import getpass
import platform
import os
import shutil


""" from pydap.client import open_url
from pydap.cas.urs import setup_session

dataset_url = 'https://data.gesdisc.earthdata.nasa.gov/data/OCO2_DATA/OCO2_L2_Lite_FP.11r/2014/oco2_LtCO2_140906_B11014Ar_230329213249s.nc4'

username = 'your_earthdata_username_goes_here'
password = 'your_earthdata_password_goes_here'

try:
    session = setup_session(username, password, check_url=dataset_url)
    dataset = open_url(dataset_url, session=session)
except AttributeError as e:
    print('Error:', e)
    print('Please verify t """


urs = 'urs.earthdata.nasa.gov' 

homeDir = os.path.expanduser("C:") + os.sep

with open(homeDir + '.urs_cookies', 'w') as file:
    file.write('')
    file.close()
with open(homeDir + '.dodsrc', 'w') as file:
    file.write('HTTP.COOKIEJAR={}.urs_cookies\n'.format(homeDir))
    file.write('HTTP.NETRC={}.netrc'.format(homeDir))
    file.close()

print('Saved .netrc, .urs_cookies, and .dodsrc to:', homeDir)

# Set appropriate permissions for Linux/macOS
if platform.system() != "Windows":
    Popen('chmod og-rw ~/.netrc', shell=True)
else:
    # Copy dodsrc to working directory in Windows  
    shutil.copy2(homeDir + '.dodsrc', os.getcwd())
    print('Copied .dodsrc to:', os.getcwd())

# Set the URL string to point to a specific data URL.

URL = 'https://data.gesdisc.earthdata.nasa.gov/data/OCO2_DATA/OCO2_L2_Lite_FP.11r/2014/oco2_LtCO2_140906_B11014Ar_230329213249s.nc4'

# Set the FILENAME string to the data file name, the LABEL keyword value 
FILENAME = 'result.nc4'
username = 'miguelmartinez_everimpact'
password = '5e@PXB-c!8xmaUk'

result = requests.get(URL, auth=(username,password))
try:
    result.raise_for_status()
    f = open(FILENAME,'wb')
    f.write(result.content)
    f.close()
    print('contents of URL written to '+FILENAME)
except:
    print('requests.get() returned an error code '+str(result.status_code))
    print(result.text)

# wget --load-cookies C:\.urs_cookies --save-cookies C:\.urs_cookies --keep-session-cookies --user=<your username> --ask-password -i <url.txt>