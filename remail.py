#!/usr/bin/env python
# coding: utf-8

import re

#a = open('costom.txt', 'w')
#print a.read()
a = 'a@example.com;b@example.com    100000'


#b = re.search("([\w\.-]+@[\w\.-]+);([\w\.-]+@[\w\.-]+)\
#;?([\w\.-]+@[\w\.-]+)? +([0-9]{6})", a)
b = re.findall("([\w\.-]+@[\w\.-]+)", a)
c = re.findall("[0-9]{6}", a)
d = set(b)
print b
print c
print "{0}".format(d)
#print c.group(0)
#print b.group(0)
#print b.group(1)
#print b.group(2)
#print b.group(3)
#print b.group(4)

f = open("test.txt", "w")
for s in d:
    f.write(s+'\n')
    
f.close()
