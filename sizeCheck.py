'''
Created on Aug 21, 2018

@author: nanda
python ~/aTools/utilities/sizeCheck.py sortedMissingScaffolds 
'''
import sys

with open(sys.argv[1]) as FH:
    t=0
    for line in FH:
        line=line.rstrip("\n")
        n=line.split("\t")
        v=n[0].split("__")
        t+=int(v[2])-int(v[1])+1
 
print(t)


# with open(sys.argv[1]) as FH:
#     t=0
#     for line in FH:
#         line=line.rstrip("\n")
#         n=line.split(":")
#         v=n[1].split("-")
#         t+=int(v[1])-int(v[0])+1
# 
# print(t)