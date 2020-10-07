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
import shutil

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

spliturl = xmlurl.split('%')
getdate = spliturl[7]
ismmonth = ''.join([i for i in spliturl[7] if not i.isdigit()])
ismyear = (spliturl[8])
ismyear = ismyear[2:7]
ismreleasedate = getdate[0:2] + ' ' + ismmonth + ' ' + ismyear
ismversion = ismmonth + ismyear + 'ISM.xml'
oldismversion = currentmonth + currentyear + 'ISM.xml'
lastmonthism = lastmonth + currentyear + 'ISM.xml'

if os.path.isfile('./' + ismversion):
  print('ISM Version already downloaded.')
elif not os.path.isfile('./' + ismversion):
  print('New ISM Version downloaded.')
  if os.path.isfile('./' + oldismversion):
    print('located file')
    shutil.move('./' + oldismversion, './PreviousISMs/' + oldismversion)
  elif os.path.isfile('./' + lastmonthism):
    print('file not found')
    shutil.move('./' + lastmonthism, './PreviousISMs/' + lastmonthism)

open('./' + ismversion, 'wb').write(retrievexml.content)

tree = ET.parse('./' + ismversion)
root = tree.getroot()

# Identify new controls in the ISM and add them to the newcontrol variable. 
# For identified controls, scrape all of the control details and add to the newcontroldetails variable.
for control in root.findall('Control'):
  if int(control.find('Revision').text) == 0 and control.find('Updated').text == ismmonth[0:3] + '-' + ismyear[0:2]:
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
  if int(control.find('Revision').text) != 0 and control.find('Updated').text == ismmonth[0:3] + '-' + ismyear[0:2]:
      updatedcontrol.append(control.find('Updated').text)
      updatedcontrolnumber.append(control.find('Identifier').text)
      for child in root.findall('Control'):
        for number in updatedcontrolnumber:
          if number == (child.find('Identifier').text):
            if number not in updatedcontroldetails:
              updatedcontroldetails['##' + number] = []
              updatedcontroldetails['##' + number].append({'Guideline':child.find('Guideline').text, 'Section':child.find('Section').text, 'Topic':child.find('Topic').text,
              'Revision':child.find('Revision').text, 'Updated':child.find('Updated').text, 'OFFICIAL':child.find('OFFICIAL').text, 'PROTECTED':child.find('PROTECTED').text,
              'SECRET':child.find('SECRET').text, 'TOP_SECRET':child.find('TOP_SECRET').text, 'Description':child.find('Description').text})

sortnewcontrolsdetails = sorted(newcontroldetails.items())
sortupdatedcontrolsdetails = sorted(updatedcontroldetails.items())
newcontrolcount = Counter(newcontrol)
updatedcontrolcount = Counter(updatedcontrol)

# Write the matching prior controls to file. 
with open('./ISMExplorer/dataoutput/newcontrols.txt', 'w') as outfile:
    json.dump(sortnewcontrolsdetails, outfile)

with open('./ISMExplorer/dataoutput/newcontrols.txt') as tf:
    newcontrolstolines = tf.readlines()

# Perform a number a substitute and replace actions on the new ISM controls to prepare for diff. 
subnewcontrols = re.sub(r'[\[\]\,\{\'\']', '', str(newcontrolstolines))
newcontrolsreplace = (subnewcontrols.replace('"}', ' \n'))
newcontrolsreplace2 = (newcontrolsreplace.replace('"', ''))

totalcontrols = sum(1 for entry in root.iter('Identifier'))

# Print number of new controls. 
if bool(newcontrolcount) == True:
  for i in newcontrolcount:
    print("There are " + bcolors.OKRED + str(newcontrolcount[i]) + bcolors.ENDC + " new controls in the " + ismmonth + ' ' + ismyear + " ISM.")
else: 
  print("There are " + bcolors.OKRED + '0' + bcolors.ENDC + ' new controls in the ' + ismmonth + ' ' + ismyear + ' ISM.')

# Print number of updated controls.
if bool(updatedcontrolcount) == True:
  for i in updatedcontrolcount:
    print("There are " + bcolors.OKRED + str(updatedcontrolcount[i]) + bcolors.ENDC + " updated controls in the " + ismmonth + ' ' + ismyear + " ISM.")
else:
  print("There are " + bcolors.OKRED + '0' + bcolors.ENDC + ' controls updated in the ' + ismmonth + ' ' + ismyear + ' ISM.')

print('There are ' + bcolors.OKRED + str(totalcontrols) + bcolors.ENDC + ' controls in total in the ' + ismmonth + ' '  + ismyear + ' ISM')

# Build Report
reportfile = open('./ISMExplorer/dataoutput/' + ismmonth + ismyear + 'ISMReport.txt', 'w')
reportfile.write(ismmonth + ' ' + ismyear + ' ISMExplorer Report\n')
reportfile.write('ISM released on the ' + ismreleasedate + '\n')
reportfile.write('There are ' + str(totalcontrols) + ' controls in total in the ' + ismmonth + ' '  + ismyear + ' ISM\n')
if newcontrolcount[0] == 0:
  reportfile.write('There are no new controls in the ' + ismmonth + ' ' + ismyear + ' ISM\n')
else:
  reportfile.write('There are ' + newcontrolcount[0] + ' in the ' + ismmonth + ' ' + ismyear + ' ISM\n')
  reportfile.write('\n' + newcontrolsreplace2)
for i in updatedcontrolcount:
  reportfile.write('There are ' + str(updatedcontrolcount[i]) + ' updated controls in the ' + ismmonth + ' ' + ismyear + ' ISM\n')

with open('./ISMExplorer/dataoutput/' + ismmonth + ismyear + 'updatedcontrols.txt', 'w') as outfile:
    json.dump(sortupdatedcontrolsdetails, outfile)