# Add top 5 most revised controls. 
# Sort new and revised controls by date. 
# Ensure new and revised control dates align.
# Add ISM chapter headings. 

import os.path
import requests
import xml.etree.ElementTree as ET
import re
import bs4
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
previouscontrols          = []
latestcontrols            = []
deletedcontroldetails     = {}

# Get date and assign month and year to variables.
currentdate = date.today()
currentmonth= currentdate.strftime("%B")
currentyear = currentdate.strftime("%Y")
getlastmonth = date.today() -relativedelta(months=1)
lastmonth = format(getlastmonth, '%B')

url = 'https://www.cyber.gov.au/acsc/view-all-content/ism'
retrievehtml = requests.get(url, allow_redirects=True)
nosoup = bs4.BeautifulSoup(retrievehtml.text, features="lxml")

print(f'[+]\tScraping {url} to find ISM XML file.')
gethref = (nosoup.find(href=re.compile(".xml")))
xmlurl = gethref.get('href')

spliturl = xmlurl.split('%')
getdate = spliturl[7]
ismmonth = ''.join([i for i in spliturl[7] if not i.isdigit()])
ismyear = (spliturl[8])
ismyear = ismyear[2:7]
ismreleasedate = (f'{getdate[0:2]} {ismmonth} {ismyear}')
ismversion = ismmonth + ismyear + 'ISM.xml'
oldismversion = currentmonth + currentyear + 'ISM.xml'
lastmonthism = lastmonth + currentyear + 'ISM.xml'

# Retrieve xml file from CGA.
print(f'[+]\tDownloading the {ismmonth} {ismyear} ISM XML file from {url}')
retrievexml = requests.get(xmlurl, allow_redirects=True)
if '200' in str(retrievexml):
  print(f'[+]\t{ismmonth} {ismyear} ISM downloaded successfully.')
else:
  print('ISM XML file failed to download')
  exit()
open('./ISM.xml', 'wb').write(retrievexml.content)

if os.path.isfile('./CurrentISM/' + ismversion):
  print(f'[+]\t{ismmonth} {ismyear} ISM already exists on filesystem.')
elif not os.path.isfile('./CurrentISM/' + ismversion):
  print('[+]\tNew ISM Version identified!')
  if os.path.isfile('./CurrentISM/' + oldismversion):
    print('[+]\tlocated previous ISM file. Moving to other folder.')
    shutil.move('./CurrentISM/' + oldismversion, './PreviousISMs/' + oldismversion)
  elif os.path.isfile('./CurrentISM/' + lastmonthism):
    print('[+]\tfile not found')
    shutil.move('./CurrentISM/' + lastmonthism, './PreviousISMs/' + lastmonthism)

open('./CurrentISM/' + ismversion, 'wb').write(retrievexml.content)

tree = ET.parse('./CurrentISM/' + ismversion)
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

sortnewcontrolsdetails = sorted(newcontroldetails.items())
newcontrolcount = Counter(newcontrol)

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

sortupdatedcontrolsdetails = sorted(updatedcontroldetails.items())
updatedcontrolcount = Counter(updatedcontrol)

tree = ET.parse('./PreviousISMs/' + lastmonthism)
root = tree.getroot()
for control in root.findall('Control'):
  previouscontrols.append(control.find('Identifier').text)

tree = ET.parse('./CurrentISM/' + ismversion)
root = tree.getroot()

for control in root.findall('Control'):
  latestcontrols.append(control.find('Identifier').text)

controldiff = [item for item in previouscontrols if item not in latestcontrols]

tree= ET.parse('./PreviousISMs/' + lastmonthism)
root = tree.getroot()

for control in root.findall('Control'):
  for identifier in controldiff:
    if identifier == (control.find('Identifier').text):
      deletedcontroldetails[identifier] = []
      deletedcontroldetails[identifier].append({'Guideline':control.find('Guideline').text, 'Section':control.find('Section').text, 'Topic':control.find('Topic').text,
      'Revision':control.find('Revision').text, 'Updated':control.find('Updated').text, 'OFFICIAL':control.find('OFFICIAL').text, 'PROTECTED':control.find('PROTECTED').text,
      'SECRET':control.find('SECRET').text, 'TOP_SECRET':control.find('TOP_SECRET').text, 'Description':control.find('Description').text})

sortdeletedcontrolsdetails = sorted(deletedcontroldetails.items())

with open('./dataoutput/deletedcontrols.txt', 'w') as outfile:
    json.dump(sortdeletedcontrolsdetails, outfile)

with open('./dataoutput/deletedcontrols.txt') as tf:
  delcontrolstolines = tf.readlines()

subdelcontrols = re.sub(r'[\[\]\,\{\'\']', '', str(delcontrolstolines))
delcontrolsreplace = (subdelcontrols.replace('"}', '\n'))
delcontrolsreplace2 = (delcontrolsreplace.replace('"', ''))

# Write the matching prior controls to file. 
with open('./dataoutput/newcontrols.txt', 'w') as outfile:
    json.dump(sortnewcontrolsdetails, outfile)
outfile.close()

with open('./dataoutput/newcontrols.txt') as tf:
    newcontrolstolines = tf.readlines()
tf.close()

# Perform a number a substitute and replace actions on the new ISM controls to prepare for diff. 
subnewcontrols = re.sub(r'[\[\]\,\{\'\']', '', str(newcontrolstolines))
newcontrolsreplace = (subnewcontrols.replace('"}', ' \n'))
newcontrolsreplace2 = (newcontrolsreplace.replace('"', ''))

totalcontrols = sum(1 for entry in root.iter('Identifier'))

with open('./dataoutput/' + ismmonth + ismyear + 'updatedcontrols.txt', 'w') as outfile:
    json.dump(sortupdatedcontrolsdetails, outfile)

# Print number of new controls. 
if bool(newcontrolcount) == True:
  for i in newcontrolcount:
    print(f'\nThere are {bcolors.OKRED}{newcontrolcount[i]}{bcolors.ENDC} new controls in the {ismmonth} {ismyear} ISM.')
else: 
  print(f'\nThere are {bcolors.OKRED}0{bcolors.ENDC} new controls in the {ismmonth} {ismyear} ISM.')

# Print number of updated controls.
if bool(updatedcontrolcount) == True:
  for i in updatedcontrolcount:
    print(f'There are {bcolors.OKRED}{(updatedcontrolcount[i])}{bcolors.ENDC} updated controls in the {ismmonth} {ismyear} ISM.')
else:
  print(f'There are {bcolors.OKRED}0{bcolors.ENDC} updated controls in the {ismmonth} {ismyear} ISM.')

print(f'There were {bcolors.OKRED}{(len(controldiff))}{bcolors.ENDC} controls rescinded from the {ismmonth} {ismyear} ISM.')
print(f'There are {bcolors.OKRED}{(totalcontrols)}{bcolors.ENDC} controls in total in the {ismmonth} {ismyear} ISM.')

# Build Report
reportfile = open('./dataoutput/' + ismmonth + ismyear + 'ISMReport.txt', 'w')
reportfile.write(f'{ismmonth} {ismyear} ISMExplorer Report\n')
reportfile.write(f'ISM released on the {ismreleasedate}\n')
reportfile.write(f'There are {(totalcontrols)} controls in the {ismmonth} {ismyear} ISM\n')
if newcontrolcount == 0:
  reportfile.write(f'\nThere are 0 new controls in the {ismmonth} {ismyear} ISM\n')
else:
  for i in newcontrolcount:
    reportfile.write(f'There are {(newcontrolcount[i])} new controls in the {ismmonth} {ismyear} ISM\n')
    reportfile.write(f'\n{newcontrolsreplace2}')
reportfile.write(f'\nThere were {(len(controldiff))} rescinded controls in the {ismmonth} {ismyear} ISM:\n \n {delcontrolsreplace2}')
for i in updatedcontrolcount:
  reportfile.write(f'\nThere are {(updatedcontrolcount[i])} updated controls in the {ismmonth} {ismyear} ISM:\n')
reportfile.close()