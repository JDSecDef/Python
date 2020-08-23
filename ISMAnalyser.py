# Add top 5 most revised controls. 
# Sort new and revised controls by date. 

import requests
import xml.etree.ElementTree as ET
import re
import bs4
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    OKYELLOW = '\033[93m'
    OKRED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

totalcontrols     = 0
uniqueofficial    = 0
officialcontrols  = 0
uniqueprotected   = 0
protectedcontrols = 0
uniquesecret      = 0
secretcontrols    = 0
uniquetopsecret   = 0
topsecretcontrols = 0
revisedcontrol    = []
newcontrol        = []

# Scrape CGA ISM page to get XML file.  
url = 'https://www.cyber.gov.au/acsc/view-all-content/ism'
retrievehtml = requests.get(url, allow_redirects=True)
nosoup = bs4.BeautifulSoup(retrievehtml.text, features="lxml")
print('\n[+]\tScraping ' + bcolors.OKGREEN + url + bcolors.ENDC + ' to find ISM XML file')
gethref = (nosoup.find(href=re.compile(".xml")))
xmlurl = gethref.get('href')
filename = xmlurl.split("%")
month = filename[7]
year = filename[8]

# Retrieve xml file from CGA. 
print('[+]\tDownloading the ISM XML File from ' + bcolors.OKGREEN + url + bcolors.ENDC)
retrievexml = requests.get(xmlurl, allow_redirects=True)
if '200' in str(retrievexml):
  print('[+]\tSucessfully downloaded the ' + bcolors.OKGREEN +  month[2:] + ' ' + year[2:] + ' ' + 'ISM.xml ' + bcolors.ENDC)
else:
    print('ISM XML file failed to download')
    exit()
open(month[2:] + year[2:] + 'ISM.xml', 'wb').write(retrievexml.content)

print('[+]\tAnalysing the ' + bcolors.OKGREEN + month[2:] + ' ' + year[2:] + ' ' + 'ISM' + bcolors.ENDC + '\n')
tree = ET.parse('./' + month[2:] + year[2:] + 'ISM.xml')
root = tree.getroot()

# Identify new controls and revised controls in the ISM. 
for control in root.findall('Control'):
  if int(control.find('Revision').text) >=1:
    revisedcontrol.append(control.find('Updated').text)
  else:
    newcontrol.append(control.find('Updated').text)

newcontrolcount = Counter(newcontrol)
revisedcontrolcount = Counter(revisedcontrol)

for key, value in zip(newcontrolcount.items(), (revisedcontrolcount.items())):
  print('There were ' + bcolors.OKRED + str(key[1]) + bcolors.ENDC + ' new controls and ' + bcolors.OKRED + str(value[1]) + bcolors.ENDC \
    + ' updated controls in ' + str(key[0]))

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

print('\nThere are ' + bcolors.OKRED + str(uniqueofficial) + bcolors.ENDC + ' unique OFFICIAL controls in the ' + month[2:] + ' '  + year[2:] + ' ISM')
print('There are ' + bcolors.OKRED + str(officialcontrols) + bcolors.ENDC + ' OFFICIAL Controls in the ' + month[2:] + ' '  + year[2:] + ' ISM')
print('There are ' + bcolors.OKRED + str(uniqueprotected) + bcolors.ENDC + ' unique PROTECTED controls in the ' + month[2:] + ' '  + year[2:] + ' ISM')
print('There are ' + bcolors.OKRED + str(protectedcontrols) + bcolors.ENDC + ' PROTECTED Controls in the ' + month[2:] + ' '  + year[2:] + ' ISM')
print('There are ' + bcolors.OKRED + str(uniquesecret) + bcolors.ENDC + ' unique SECRET controls in the ' + month[2:] + ' '  + year[2:] + ' ISM')
print('There are ' + bcolors.OKRED + str(secretcontrols) + bcolors.ENDC + ' SECRET Controls in the ' + month[2:] + ' '  + year[2:] + ' ISM')
print('There are ' + bcolors.OKRED + str(uniquetopsecret) + bcolors.ENDC + ' unique TOP_SECRET controls in the ' + month[2:] + ' '  + year[2:] + ' ISM')
print('There are ' + bcolors.OKRED + str(topsecretcontrols) + bcolors.ENDC + ' TOP SECRET Controls in the ' + month[2:] + ' '  + year[2:] + ' ISM')
print('There are ' + bcolors.OKRED + str(totalcontrols) + bcolors.ENDC + ' controls in total in the ' + month[2:] + ' '  + year[2:] + ' ISM')