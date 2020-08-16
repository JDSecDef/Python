#Add download file check to confirm if succesful or not.

import requests
import xml.etree.ElementTree as ET
import re
import bs4

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    OKYELLOW = '\033[93m'
    OKRED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

totalcontrols = 0
uniqueofficial = 0
officialcontrols = 0
uniqueprotected = 0
protectedcontrols = 0
uniquesecret = 0
secretcontrols = 0
uniquetopsecret = 0
topsecretcontrols = 0

url = 'https://www.cyber.gov.au/acsc/view-all-content/ism'
retrievehtml = requests.get(url, allow_redirects=True)
nosoup = bs4.BeautifulSoup(retrievehtml.text, features="lxml")
gethref = (nosoup.find(href=re.compile(".xml")))
xmlurl = gethref.get('href')
filename = xmlurl.split("%")
month = filename[7]
year = filename[8]
print('\nDownloading the ISM XML File from ' + bcolors.OKGREEN + url + bcolors.ENDC)
retrievexml = requests.get(xmlurl, allow_redirects=True)
open(month[2:] + year[2:] + 'ISM.xml', 'wb').write(retrievexml.content)

tree = ET.parse('./' + month[2:] + year[2:] + 'ISM.xml')
root = tree.getroot()

for control in root.findall('Control'):
  official = control.find('OFFICIAL').text
  protected = control.find('PROTECTED').text
  secret = control.find('SECRET').text
  topsecret = control.find('TOP_SECRET').text
  if official == 'Yes' and protected == 'No' and secret == 'No' and topsecret == 'No':
    uniqueofficial+=1
  if official == 'Yes':
    officialcontrols+=1
  if official == 'No' and protected == 'Yes' and secret == 'No' and topsecret == 'No':
    uniqueprotected+=1
  if protected == 'Yes':
    protectedcontrols+=1
  if official == 'No' and protected == 'No' and secret == 'Yes' and topsecret == 'No':
    uniquesecret+=1
  if secret == 'Yes':
    secretcontrols+=1
  if official == 'No' and protected == 'No' and secret == 'No' and topsecret == 'Yes':
    uniquetopsecret+=1
  if topsecret == 'Yes':
    topsecretcontrols+=1
totalcontrols = sum(1 for entry in root.iter('Identifier'))

print('Analysing the ' + bcolors.OKGREEN + month[2:] + ' ' + year[2:] + ' ' + 'ISM' + bcolors.ENDC + '\n')
print('There are ' + bcolors.OKRED + str(uniqueofficial) + bcolors.ENDC + ' unique OFFICIAL controls in the ' + month[2:] + ' '  + year[2:] + ' ISM')
print('There are ' + bcolors.OKRED + str(officialcontrols) + bcolors.ENDC + ' OFFICIAL Controls in the ' + month[2:] + ' '  + year[2:] + ' ISM')
print('There are ' + bcolors.OKRED + str(uniqueprotected) + bcolors.ENDC + ' unique PROTECTED controls in the ' + month[2:] + ' '  + year[2:] + ' ISM')
print('There are ' + bcolors.OKRED + str(protectedcontrols) + bcolors.ENDC + ' PROTECTED Controls in the ' + month[2:] + ' '  + year[2:] + ' ISM')
print('There are ' + bcolors.OKRED + str(uniquesecret) + bcolors.ENDC + ' unique SECRET controls in the ' + month[2:] + ' '  + year[2:] + ' ISM')
print('There are ' + bcolors.OKRED + str(secretcontrols) + bcolors.ENDC + ' SECRET Controls in the ' + month[2:] + ' '  + year[2:] + ' ISM')
print('There are ' + bcolors.OKRED + str(uniquetopsecret) + bcolors.ENDC + ' unique TOP_SECRET controls in the ' + month[2:] + ' '  + year[2:] + ' ISM')
print('There are ' + bcolors.OKRED + str(topsecretcontrols) + bcolors.ENDC + ' TOP SECRET Controls in the ' + month[2:] + ' '  + year[2:] + ' ISM')
print('There are ' + bcolors.OKRED + str(totalcontrols) + bcolors.ENDC + ' controls in total in the ' + month[2:] + ' '  + year[2:] + ' ISM')