'''
Created on Feb 2, 2019

@author: nanda
~/aTools/utilities/binScaffoldList1kb.py
Not correctly Working
'''
with open("t5-finalscaffoldList-1-94") as SCPLIST, open("t5-finalscaffoldList-1-94-Bin1kb", "w") as OUT:
    for line in SCPLIST:
        line=line.rstrip("\n")
        v=line.split("\t")
        sc=v[0].split("__")
        start=int(sc[1])
        end=int(sc[2])
        while(start<end):
            nE=start+1000-1
            if(nE>end):
                nE=end
            ln=sc[0]+"__"+str(start)+"__"+str(nE)
            start=start+1000
            OUT.write(ln+"\n")