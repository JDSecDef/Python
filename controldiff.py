
import re
import json
import xml.etree.ElementTree as ET


updatefile = open('./dataoutput/Sep2020updated.txt')

diff1 = open('./dataoutput/Sep1.txt', 'w')
diff2 = open('./dataoutput/Aug1.txt', 'w')

tree = ET.parse('./August2020ISM.xml')
root = tree.getroot()

extract = []
newcontrol = []
updatedcontroldetails = {}

updatedcontrols = updatefile.read()
#print(updatedcontrols)
extract = re.findall(r'\b\d{4}\b', updatedcontrols)

for control in root.findall('Control'):
    for i in extract:
        if i == (control.find('Identifier').text):
            updatedcontroldetails['##' + i] = []
            updatedcontroldetails['##' + i].append({'Guideline':control.find('Guideline').text, 'Section':control.find('Section').text, 'Topic':control.find('Topic').text,
            'Revision':control.find('Revision').text, 'Updated':control.find('Updated').text, 'OFFICIAL':control.find('OFFICIAL').text, 'PROTECTED':control.find('PROTECTED').text,
            'SECRET':control.find('SECRET').text, 'TOP_SECRET':control.find('TOP_SECRET').text, 'Description':control.find('Description').text})

sub = re.sub(r'[\[\]\"\,\{\}\'\']', '', str(updatedcontrols))
sub2 = re.sub(r'[\[\]\"\,\{\}\'\']', '', str(updatedcontroldetails))
match = re.split(r'[##]', sub)
match2 = re.split(r'[##]', sub2)
while '' in match:
    match.remove('')

while '' in match2:
    match2.remove('')

testing = ('\n'.join(match))
testing2 = ('\n'.join(match2))

diff1.write(testing)
diff2.write(testing2)
