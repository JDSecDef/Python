# Add top 5 most revised controls. 
# Sort new and revised controls by date. 
# Ensure new and revised control dates align.
# Add ISM chapter headings. 

import os.path
import requests
import xml.etree.ElementTree as ET
import re
import bs4
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from datetime import date

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
updatedcontrol    = []
newcontrol        = []
controlnumber     = []

# Get date and assign month and year to variables.
currentdate = date.today()
currentmonth= currentdate.strftime("%B")
currentyear = currentdate.strftime("%Y")

url = 'https://www.cyber.gov.au/acsc/view-all-content/ism'
retrievehtml = requests.get(url, allow_redirects=True)
nosoup = bs4.BeautifulSoup(retrievehtml.text, features="lxml")

print('\n[+]\tChecking if ' + bcolors.OKGREEN + currentmonth + currentyear + 'ISM.xml' + bcolors.ENDC + bcolors.ENDC + ' already exists in current directory.')
if os.path.isfile('./' + currentmonth + currentyear + 'ISM.xml'):
  print('[+]\tLocated ' + bcolors.OKGREEN + currentmonth + currentyear + 'ISM.xml' + bcolors.ENDC + ' in current directory.')
  xmlexists = True
else:
    xmlexists = False
    print('[+]\tISM XML file not found!')
    # Scrape CGA ISM page to get XML file.  
    print('[+]\tScraping ' + bcolors.OKGREEN + url + bcolors.ENDC + ' to find ISM XML file.')
    gethref = (nosoup.find(href=re.compile(".xml")))
    xmlurl = gethref.get('href')

if xmlexists != True:
  # Retrieve xml file from CGA. 
  print('[+]\tDownloading the ISM XML file from ' + bcolors.OKGREEN + url + bcolors.ENDC)
  retrievexml = requests.get(xmlurl, allow_redirects=True)
  # Check if xml file downloaded successfully.
  if '200' in str(retrievexml):
    print('[+]\tSucessfully downloaded the ' + bcolors.OKGREEN +  currentmonth + ' ' + currentyear + ' ' + 'ISM.xml ' + bcolors.ENDC + '.')
  else:
    print('ISM XML file failed to download')
    exit()
  open(currentmonth + currentyear + 'ISM.xml', 'wb').write(retrievexml.content)

print('[+]\tChecking if ' + bcolors.OKGREEN + currentmonth + currentyear + 'ISM.pdf' + bcolors.ENDC + bcolors.ENDC + ' already exists in current directory.')
if os.path.isfile('./' + currentmonth + currentyear + 'ISM.pdf'):
  print('[+]\tLocated ' + bcolors.OKGREEN + currentmonth + currentyear + 'ISM.pdf' + bcolors.ENDC + ' in current directory.')
  pdfexists = True
else:
    pdfexists = False
    print('[+]\tISM PDF file not found!')
    # Scrape CGA ISM page to find ISM pdf file.
    print('[+]\tScraping ' + bcolors.OKGREEN + url + bcolors.ENDC + ' to find ISM PDF file.')
    getpdf = (nosoup.find(href=re.compile(".pdf")))
    pdfurl = getpdf.get('href')

if pdfexists != True:
  retrievepdf = requests.get(pdfurl, allow_redirects=True)
  if '200' in str(retrievepdf):
    print('[+]\tSucessfully downloaded the ' + bcolors.OKGREEN +  currentmonth + ' ' + currentyear + ' ' + 'ISM.pdf ' + bcolors.ENDC + '.')
  else:
    print('ISM PDF file failed to download')
    exit()
  open(currentmonth + currentyear + 'ISM.pdf', 'wb').write(retrievepdf.content)

print('[+]\tAnalysing the ' + bcolors.OKGREEN +  currentmonth + currentyear + 'ISM.xml' + bcolors.ENDC + '.' + '\n')
tree = ET.parse('./' + currentmonth + currentyear + 'ISM.xml')
root = tree.getroot()

# Identify new controls and updated controls in the ISM. 
for control in root.findall('Control'):
  if int(control.find('Revision').text) == 0 and control.find('Updated').text == currentmonth[0:3] + '-' + currentyear[0:2]:
    newcontrol.append(control.find('Updated').text)

for control in root.findall('Control'):
  if int(control.find('Revision').text) != 0 and control.find('Updated').text == currentmonth[0:3] + '-' + currentyear[0:2]:
    updatedcontrol.append(control.find('Updated').text)

# Count new and updated controls in the latest ISM.     
newcontrolcount = Counter(newcontrol)
updatedcontrolcount = Counter(updatedcontrol)

# Print number of new controls. 
if bool(newcontrolcount) == True:
  for i in newcontrolcount:
    print("There are " + bcolors.OKRED + str(newcontrolcount[i]) + bcolors.ENDC + " new controls in the " + currentmonth + ' ' + currentyear + " ISM.")
else: 
  print("There are " + bcolors.OKRED + '0' + bcolors.ENDC + ' new controls in the ' + currentmonth + ' ' + currentyear + ' ISM.')

# Print number of updated controls.
if bool(updatedcontrolcount) == True:
  for i in updatedcontrolcount:
    print("There are " + bcolors.OKRED + str(updatedcontrolcount[i]) + bcolors.ENDC + " updated controls in the " + currentmonth + ' ' + currentyear + " ISM.")
else:
  print("There are " + bcolors.OKRED + '0' + bcolors.ENDC + ' controls updated in the ' + currentmonth + ' ' + currentyear + ' ISM.')

# This is not working properly.
#for key, value in zip(newcontrolcount.items(), (revisedcontrolcount.items())):
 # print('There are ' + bcolors.OKRED + str(key[1]) + bcolors.ENDC + ' new controls in the ' + bcolors.OKRED + str(key[0]) + ' ISM' + bcolors.ENDC)
  #print('There are ' + bcolors.OKRED + str(value[1]) + bcolors.ENDC + ' updated controls in the ' + bcolors.OKRED + str(value[0]) + ' ISM' + bcolors.ENDC)

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

print('\nThere are ' + bcolors.OKRED + str(uniqueofficial) + bcolors.ENDC + ' unique OFFICIAL controls in the ' + currentmonth + ' '  + currentyear + ' ISM')
print('There are ' + bcolors.OKRED + str(officialcontrols) + bcolors.ENDC + ' OFFICIAL Controls in the ' + currentmonth + ' '  + currentyear + ' ISM')
print('There are ' + bcolors.OKRED + str(uniqueprotected) + bcolors.ENDC + ' unique PROTECTED controls in the ' + currentmonth + ' '  + currentyear + ' ISM')
print('There are ' + bcolors.OKRED + str(protectedcontrols) + bcolors.ENDC + ' PROTECTED Controls in the ' + currentmonth + ' '  + currentyear + ' ISM')
print('There are ' + bcolors.OKRED + str(uniquesecret) + bcolors.ENDC + ' unique SECRET controls in the ' + currentmonth + ' '  + currentyear + ' ISM')
print('There are ' + bcolors.OKRED + str(secretcontrols) + bcolors.ENDC + ' SECRET Controls in the ' + currentmonth + ' '  + currentyear + ' ISM')
print('There are ' + bcolors.OKRED + str(uniquetopsecret) + bcolors.ENDC + ' unique TOP_SECRET controls in the ' + currentmonth + ' '  + currentyear + ' ISM')
print('There are ' + bcolors.OKRED + str(topsecretcontrols) + bcolors.ENDC + ' TOP SECRET Controls in the ' + currentmonth + ' '  + currentyear + ' ISM')
print('There are ' + bcolors.OKRED + str(totalcontrols) + bcolors.ENDC + ' controls in total in the ' + currentmonth + ' '  + currentyear + ' ISM')