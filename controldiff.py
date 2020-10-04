
import re
import json
import xml.etree.ElementTree as ET
import difflib

updatefile = open('./dataoutput/September2020updatedcontrols.txt')

diff3 = open('./dataoutput/controldiff1.txt', 'w')

tree = ET.parse('./PreviousISMs/August2020ISM.xml')
root = tree.getroot()

extract = []
newcontrol = []
updatedcontroldetails = {}

updatedcontrols = updatefile.read()
extract = re.findall(r'\b\d{4}\b', updatedcontrols)
#print(extract)

for control in root.findall('Control'):
    for i in extract:
        if i == (control.find('Identifier').text):
            updatedcontroldetails['##' + i] = []
            updatedcontroldetails['##' + i].append({'Guideline':control.find('Guideline').text, 'Section':control.find('Section').text, 'Topic':control.find('Topic').text,
            'Revision':control.find('Revision').text, 'Updated':control.find('Updated').text, 'OFFICIAL':control.find('OFFICIAL').text, 'PROTECTED':control.find('PROTECTED').text,
            'SECRET':control.find('SECRET').text, 'TOP_SECRET':control.find('TOP_SECRET').text, 'Description':control.find('Description').text})

sortupdatedcontrolsdetails = sorted(updatedcontroldetails.items())

#print(updatedcontroldetails)
#for k, v in sorted(updatedcontroldetails.items()):
 #   print(k, v)

sortupdatedcontroldetails = sorted(updatedcontroldetails.items())\

with open('./dataoutput/test445.txt', 'w') as outfile:
    json.dump(sortupdatedcontrolsdetails, outfile)

updatefile2 = open('./dataoutput/test445.txt')
oldcontrols = updatefile2.read()

sub = re.sub(r'[\[\]\"\,\{\}\'\']', '', str(updatedcontrols))
sub2 = re.sub(r'[\[\]\"\,\{\}\'\']', '', str(oldcontrols))

match = re.split(r'[##]', sub)
match2 = re.split(r'[##]', sub2)
while '' in match:
    match.remove('')

while '' in match2:
    match2.remove('')

testing = ('\n'.join(match2))
testing2 = ('\n'.join(match))

def readable_whitespace(line):
    end = len(line.rstrip('\r'))
    return line[:end] + repr(line[end:])[1:-1]

# Two strings are expected as input
#def print_diff(testing, testing2):
d = difflib.Differ()
testing = testing.splitlines(True)
testing2 = testing2.splitlines(True)
testing = [readable_whitespace(line) for line in testing]
testing2 = [readable_whitespace(line) for line in testing2]

result = list(d.compare(testing, testing2))
result2 = ('\n'.join(result))
diff3.write(result2.replace('?', ' '))