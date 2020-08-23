'''
Created on May 9, 2020

@author: nanda
'''
with open("headerN4") as inFH, open("coveragetxt") as orderFH, open("rearranged.coveragetxt","w") as outFH:
    new_order = []
    old_order = []
    for line in orderFH:
        line=line.rstrip("\n")
        new_order.append(line)
    c=0
    for line in inFH:
        line=line.rstrip("\n")
        header=line.split("__")
        start=header[1]
        end=header[2]
        new_order[c][0].split("|")[2]