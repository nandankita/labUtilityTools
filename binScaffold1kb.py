'''
Created on Aug 6, 2018

@author: nanda
python ~/aTools/utilities/binScaffold1kb.py
'''
with open("singCorrectListHang4NMPos") as SCPLIST, open("scaffold1kb", "w") as OUT:
    for line in SCPLIST:
        line=line.rstrip("\n")
        v=line.split("\t")
        sc=v[0].split("__")
        start=int(sc[1])
        end=int(sc[2])
        lsEnd=[]
        lsSt=[]
        rght=False
        for i in range(start,end,1000):
            lsSt.append(i)
        
        for i in range(start-1,end,1000):
            lsEnd.append(i)
        
        del(lsEnd[0])
        
        lenSt=len(lsSt)
        lenEnd=len(lsEnd)
        print(line,lsSt,lsEnd)
        
        if(lenSt == 0):
            lsSt.append(start)
        if(lenEnd == 0):
            lsEnd.append(end)
            
        if(lenSt==lenEnd):
            rght=True
        elif(lenSt!=lenEnd) and (lsEnd[-1]!=end):
            lsEnd.append(end)
            lenEnd=len(lsEnd)
            if (lenSt==lenEnd):
                rght=True
        else:
            print("Error Something")
        
        print(lenSt,lenEnd,rght)
        if (v[2]=="minus") and (rght):
            for n in reversed(range(lenSt)):
                nLin=(sc[0]+"__"+str(lsSt[n])+"__"+str(lsEnd[n])+"\t"+v[1]+"\t"+v[2]+"\n")
                OUT.write(nLin)
        
        if (v[2]=="plus") and (rght):
            for n in range(lenSt):
                nLin=(sc[0]+"__"+str(lsSt[n])+"__"+str(lsEnd[n])+"\t"+v[1]+"\t"+v[2]+"\n")
                OUT.write(nLin)
            
