# Python script to get the difference between ISM controls. 
# Add in controls that were removed. 

import re
import json
import xml.etree.ElementTree as ET
import difflib
from datetime import date
from dateutil.relativedelta import relativedelta

currentdate = date.today()
currentmonth= currentdate.strftime("%B")
currentyear = currentdate.strftime("%Y")
getlastmonth = date.today() -relativedelta(months=1)
lastmonth = format(getlastmonth, '%B')

updatedcontrolsfile = open('./ISMExplorer/dataoutput/September2020updatedcontrols.txt')

diffoutfile = open('./ISMExplorer/dataoutput/' + lastmonth + currentyear + 'controldiff.txt', 'w')

tree = ET.parse('./ISMExplorer/PreviousISMs/August2020ISM.xml')
root = tree.getroot()

extractcontrols = []
newcontrol = []
priorcontroldetails = {}


updatedcontrols = updatedcontrolsfile.read()
extractcontrols = re.findall(r'\b\d{4}\b', updatedcontrols)

# Using the updated controls find their previous version in the n-1 ISM. 
for control in root.findall('Control'):
    for i in extractcontrols:
        if i == (control.find('Identifier').text):
            priorcontroldetails['##' + i] = []
            priorcontroldetails['##' + i].append({'Guideline':control.find('Guideline').text, 'Section':control.find('Section').text, 'Topic':control.find('Topic').text,
            'Revision':control.find('Revision').text, 'Updated':control.find('Updated').text, 'OFFICIAL':control.find('OFFICIAL').text, 'PROTECTED':control.find('PROTECTED').text,
            'SECRET':control.find('SECRET').text, 'TOP_SECRET':control.find('TOP_SECRET').text, 'Description':control.find('Description').text})

# Sort the identified prior controls to prepare for the diff. 
sortpriorcontrolsdetails = sorted(priorcontroldetails.items())

# Write the matching prior controls to file. 
with open('./ISMExplorer/dataoutput/priorcontrols.txt', 'w') as outfile:
    json.dump(sortpriorcontrolsdetails, outfile)

# Open the updated controls and prior controls and read to lines. 
with open('./ISMExplorer/dataoutput/September2020updatedcontrols.txt') as ff:
    updatedcontrolstolines = ff.readlines()
with open('./ISMExplorer/dataoutput/priorcontrols.txt') as tf:
    priorcontrolstolines = tf.readlines()

# Perform a number a substitute and replace actions on the updated ISM controls to prepare for diff. 
subupdatedcontrols = re.sub(r'[\[\]\,\{\'\']', '', str(updatedcontrolstolines))
updatedcontrolsreplace = (subupdatedcontrols.replace('##', ''))
updatedcontrolsreplace2 = (updatedcontrolsreplace.replace('"}', ' \n'))
updatedcontrolsreplace3 = (updatedcontrolsreplace2.replace('"', ''))

# Perform a number a substitute and replace actions on the prior ISM controls to prepare for diff. 
subpriorcontrols = re.sub(r'[\[\]\,\{\'\']', '', str(priorcontrolstolines))
priorcontrolsreplace = (subpriorcontrols.replace('##', ''))
priorcontrolsreplace2 = (priorcontrolsreplace.replace('"}', ' \n'))
priorcontrolsreplace3 = (priorcontrolsreplace2.replace('"', ''))

# Split the lines of the prior and updated controls strings. 
updatedcontrolssplit = (updatedcontrolsreplace3.splitlines(keepends=True))
priorcontrolssplit = (priorcontrolsreplace3.splitlines(keepends=True))

# Perform the diff action and write to file. 
diffresult = difflib.ndiff(priorcontrolssplit, updatedcontrolssplit)
diffjoin = (''.join(diffresult))
diffoutfile.writelines(diffjoin)

with open('./ISMExplorer/dataoutput/September2020ISMReport.txt', "a") as reportfile:
    reportfile.write('\n' + diffjoin)