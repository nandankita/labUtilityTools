'''
Created on Aug 1, 2017

@author: nanda
'''


with open ('removed40kbbinsScaffolds', "r") as oldMatrixSc, open ("rawScaffolds", "r") as newMatrixSc:
    oldsc=[]
    newsc=[]
    for l in oldMatrixSc:
        l=l.rstrip("\n")
        oldsc.append(l)
        
    for l in newMatrixSc:
        l=l.rstrip("\n")
        newsc.append(l)
        
    diffSc=list(set(oldsc) - set(newsc))
    print(len(diffSc))