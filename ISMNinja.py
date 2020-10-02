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
from dateutil.relativedelta import relativedelta
import json

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    OKYELLOW = '\033[93m'
    OKRED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

totalcontrols             = 0
uniqueofficial            = 0
officialcontrols          = 0
uniqueprotected           = 0
protectedcontrols         = 0
uniquesecret              = 0
secretcontrols            = 0
uniquetopsecret           = 0
topsecretcontrols         = 0
newcontrol                = []
newcontrolnumber          = []
newcontroldetails         = {}
updatedcontrol            = []
updatedcontrolnumber      = []
updatedcontroldetails     = {}
outfile                   = ('./test.txt', 'wb')

# Get date and assign month and year to variables.
currentdate = date.today()
currentmonth= currentdate.strftime("%B")
currentyear = currentdate.strftime("%Y")
getlastmonth = date.today() -relativedelta(months=1)
lastmonth = format(getlastmonth, '%B')

url = 'https://www.cyber.gov.au/acsc/view-all-content/ism'
retrievehtml = requests.get(url, allow_redirects=True)
nosoup = bs4.BeautifulSoup(retrievehtml.text, features="lxml")

print('[+]\tScraping ' + bcolors.OKGREEN + url + bcolors.ENDC + ' to find ISM XML file.')
gethref = (nosoup.find(href=re.compile(".xml")))
xmlurl = gethref.get('href')

# Retrieve xml file from CGA.
print('[+]\tDownloading the ISM XML file from ' + bcolors.OKGREEN + url + bcolors.ENDC)
retrievexml = requests.get(xmlurl, allow_redirects=True)
if '200' in str(retrievexml):
  print('[+]\tISM downloaded successfully.')
else:
  print('ISM XML file failed to download')
  exit()
open('./ISM.xml', 'wb').write(retrievexml.content)

with open('./ISM.xml') as f:
  if currentmonth in f.read():
    os.rename (r'./ISM.xml',r'./' + currentmonth + currentyear + 'ISM.xml')
    outfile = open('./' + currentmonth + currentyear + 'ISMchange.txt', 'w')
    currentmonthism = True
  else:
    currentmonthism = False

with open('./ISM.xml') as f:
  if lastmonth in f.read():
    os.rename(r'./ISM.xml',r'./' + lastmonth + currentyear + 'ISM.xml')
    outfile = open('./' + lastmonth + currentyear + 'ISMchange.txt', 'w')
    lastmonthism = True
  else:
    lastmonthism = False

if bool(currentmonthism) == True:
  print('[+]\tAnalysing the ' + bcolors.OKGREEN +  currentmonth + currentyear + 'ISM.xml' + bcolors.ENDC + '.' + '\n')
  tree = ET.parse('./' + currentmonth + currentyear + 'ISM.xml')
elif bool(lastmonthism) == True:
  print('[+]\tAnalysing the ' + bcolors.OKGREEN +  lastmonth + currentyear + 'ISM.xml' + bcolors.ENDC + '.' + '\n')
  tree = ET.parse('./' + lastmonth + currentyear + 'ISM.xml')

root = tree.getroot()

# Identify new controls in the ISM and add them to the newcontrol variable. 
# For identified controls, scrape all of the control details and add to the newcontroldetails variable.
for control in root.findall('Control'):
  if int(control.find('Revision').text) == 0 and control.find('Updated').text == currentmonth[0:3] + '-' + currentyear[0:2]:
    newcontrol.append(control.find('Updated').text)
    newcontrolnumber.append(control.find('Identifier').text)
    for child in root.findall('Control'):
      for number in newcontrolnumber:
        if number == (child.find('Identifier').text):
          if number not in newcontroldetails:
            newcontroldetails[number] = []
            newcontroldetails[number].append({'Guideline':child.find('Guideline').text, 'Section':child.find('Section').text, 'Topic':child.find('Topic').text,
            'Revision':child.find('Revision').text, 'Updated':child.find('Updated').text, 'OFFICIAL':child.find('OFFICIAL').text, 'PROTECTED':child.find('PROTECTED').text,
            'SECRET':child.find('SECRET').text, 'TOP_SECRET':child.find('TOP_SECRET').text, 'Description':child.find('Description').text})

# Identifiy updated controls and add them to the updated control variable.
# For identified controls, scrape all of the control and add to the updatedcontroldetails variable.
for control in root.findall('Control'):
  if bool(currentmonthism) == True and int(control.find('Revision').text) != 0 and control.find('Updated').text == currentmonth[0:3] + '-' + currentyear[0:2]:
      updatedcontrol.append(control.find('Updated').text)
      updatedcontrolnumber.append(control.find('Identifier').text)
  if bool(lastmonthism) == True and int(control.find('Revision').text) != 0 and control.find('Updated').text == lastmonth[0:3] + '-' + currentyear[0:2]:
      updatedcontrol.append(control.find('Updated').text)
      updatedcontrolnumber.append(control.find('Identifier').text)
      for child in root.findall('Control'):
        for number in updatedcontrolnumber:
          if number == (child.find('Identifier').text):
            if number not in updatedcontroldetails:
              updatedcontroldetails[number] = []
              updatedcontroldetails[number].append({'Guideline':child.find('Guideline').text, 'Section':child.find('Section').text, 'Topic':child.find('Topic').text,
              'Revision':child.find('Revision').text, 'Updated':child.find('Updated').text, 'OFFICIAL':child.find('OFFICIAL').text, 'PROTECTED':child.find('PROTECTED').text,
              'SECRET':child.find('SECRET').text, 'TOP_SECRET':child.find('TOP_SECRET').text, 'Description':child.find('Description').text})

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

json.dump(updatedcontroldetails, outfile)