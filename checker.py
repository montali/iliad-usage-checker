from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import subprocess
import argparse
import sys

ACCOUNT_URL = "https://www.iliad.it/account/"
INFO_CSS_CLASS = "conso__text"
HEADLESS = True


parser = argparse.ArgumentParser()
parser.add_argument('-w', '--wifi',
                    dest='wifi', type=str, required=True)
parser.add_argument('-f', '--file',
                    dest='file', type=argparse.FileType('a'), required=True)
args = parser.parse_args()

# The SSID getting method is platform specific.
if sys.platform == "win32":
    ssid_checker = "netsh wlan show interfaces"
elif sys.platform == "darwin":
    ssid_checker = "/Sy*/L*/Priv*/Apple8*/V*/C*/R*/airport -I"
elif sys.platform == "linux":
    ssid_checker = "iwgetid"
else:
    raise Exception("The platform is not compatible")


if args.wifi not in str(subprocess.check_output(ssid_checker, shell=True)):
    raise Exception("Not connected to home WiFi")


options = Options()
options.headless = HEADLESS
driver = webdriver.Firefox(options=options)
driver.get(ACCOUNT_URL)
driver.implicitly_wait(10)  # seconds
infos = driver.find_elements_by_class_name(INFO_CSS_CLASS)
args.file.seek(0, 0)
args.file.truncate()
args.file.write(infos[2].text.split("\n")[0])
