
import re
import json
import xml.etree.ElementTree as ET
import difflib
from pprint import pprint

diff3 = open('./dataoutput/testdiff.txt', 'w')

#updatefile3 = open('./dataoutput/three1.txt')
#updatefile2 = open('./dataoutput/four.txt')
#controlsnew = updatefile3.readlines()

with open('./dataoutput/September2020updatedcontrols.txt') as ff:
    fromlines = ff.readlines()
with open('./dataoutput/test445.txt') as tf:
    tolines = tf.readlines()

sub = re.sub(r'[\[\]\,\{\'\']', '', str(fromlines))
match = (sub.replace('##', ''))
match2 = (match.replace('"}', ' \n'))
match3 = (match2.replace('"', ''))
#print(match3)

sub = re.sub(r'[\[\]\,\{\'\']', '', str(tolines))
catch = (sub.replace('##', ''))
catch2 = (catch.replace('"}', ' \n'))
catch3 = (catch2.replace('"', ''))
#print(catch3)

matchtest = (match3.splitlines(keepends=True))
catchtest = (catch3.splitlines(keepends=True))

result = difflib.ndiff(catchtest, matchtest)
result2 = (''.join(result))
print(result2)
diff3.writelines(result2)

#print(''.join(d))

#result = []
#for line in difflib.ndiff(matchtest, catchtest):
 #   result.append = line

#print(result)


#oldcontrols = match3.readlines()
#print(oldcontrols)
            
#thistext = '1418 Guideline: Guidelines for System Hardening Section: Operating system hardening Topic: Endpoint device control software Revision: 1 Updated: Sep-18 OFFICIAL: Yes PROTECTED: Yes SECRET: Yes TOP_SECRET: Yes Description: Endpoint device control software is implemented on workstations and servers to prevent unauthorised devices from being used.\n'
# 0345 Guideline: Guidelines for Media Section \n'
#nexttext = '1418 Guideline: Guidelines for System Hardening Section: Operating system hardening Topic: Device access control software Revision: 2 Updated: Sep-20 OFFICIAL: Yes PROTECTED: Yes SECRET: Yes TOP_SECRET: Yes Description: Device access control software is implemented on workstations and servers to prevent unauthorised devices from being connected.  \n'
#: .'

#Revision: 5 Updated: Sep-20 OFFICIAL: Yes PROTECTED: Yes SECRET: Yes TOP_SECRET: Yes Description: External interfaces of workstations and servers that allow DMA are disabled 
#Revision: 4 Updated: Sep-18 OFFICIAL: Yes PROTECTED: Yes SECRET: Yes TOP_SECRET: Yes Description: External interface connections that allow DMA are disabled
#0345 Guideline: Guidelines for Media Section: Media usage Topic: External interface connections that allow Direct Memory Access Revision:
# 
#print(controlsnew[0:1])
#trytest = '\''.join(controlsnew)
#trytest1 = (thistext.splitlines(keepends=True))
#newtest = '\''.join(oldcontrols)
#newtest1 = (nexttext.splitlines(keepends=True))
#print(trytest1)
#print(newtest1)

#for line in difflib.ndiff(trytest1, newtest1):
 #   print(line)

#print(trytest1[0][-1])

#print(controlsnew)
#print(oldcontrols)

#d = difflib.ndiff(match3, catch3, linejunk=None, charjunk=None)
#print(''.join(d))
#print(''.join(d), end="")
#testing = testing.splitlines(keepends=True)
#testing2 = testing2.splitlines(keepends=True)
#testing = [readable_whitespace(line) for line in testing]
#testing2 = [readable_whitespace(line) for line in testing2]


#jointesting = '\n'.join(testing)
#print(jointesting)
#jointesting2 = '\n'.join(testing2)
#print(jointesting)

#result = list(d(trytest1, newtest1))
#print(result)
#result2 = ('\''.join(result))
#print(result2)
#diff3.writelines(result2)