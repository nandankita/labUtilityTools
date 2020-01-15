'''
Created on Feb 2, 2019

@author: nanda
python ~/aTools/utilities/checkNewScaffoldList.py 
'''
from _collections import defaultdict
import itertools

def to_ranges(iterable):
    iterable = sorted(set(iterable))
    for key, group in itertools.groupby(enumerate(iterable),
                                        lambda t: t[1] - t[0]):
        group = list(group)
        yield group[0][1], group[-1][1]
            

with open("/nl/umw_job_dekker/users/an27w/dinoflagellets/analysis/lines-manualAssembly-4/genomeAll/60percentremoved1kb/newScaffoldList1kb60percent") as FH1, \
open("t5-finalscaffoldList-1-94") as FH2, open("unselectedBins-ManualRemoval", "w") as FH3:
    scaffoldList60PerRemoved=defaultdict(list)
    sortedScaffoldList60PerRemoved=defaultdict(list)
    t5finalscaffoldList=defaultdict(list)
    sortedT5finalscaffoldList=defaultdict(list)
    list60=[]
    listT5=[]
    
    for l in FH1:
        l=l.rstrip("\n")
        v=l.split("\t") 
        v1=v[0].split("__")
        scaffoldList60PerRemoved[v1[0]].append([int(v1[1]),int(v1[2])])
    
    
    for keys, values in scaffoldList60PerRemoved.items():
        sortedScaffoldList60PerRemoved[keys] = sorted(values, key=lambda x:x[0])
    
    
    for n in FH2:
        n=n.rstrip("\n")
        vn=n.split("\t") 
        v2=vn[0].split("__")
        t5finalscaffoldList[v2[0]].append([int(v2[1]),int(v2[2])])
    
    for keys, values in t5finalscaffoldList.items():
        sortedT5finalscaffoldList[keys] = sorted(values, key=lambda x:x[0])
    
    
    for k, v in sortedScaffoldList60PerRemoved.items():
        list60=[]
        listT5=[]
        for r in v:
            list60.append(range(r[0],r[1]+1))
        
        for i in sortedT5finalscaffoldList[k]:
            listT5.append(range(i[0],i[1]+1))
            
            
        flatList60=set([item for sublist in list60 for item in sublist])
        flatlistT5=set([item for sublist in listT5 for item in sublist])
        
        diff=list(flatList60-flatlistT5)
        if(len(diff)>0):
            check=list(to_ranges(diff))
            for vN in check:
                nl=k+"__"+str(vN[0])+"__"+str(vN[1])
                FH3.write(nl+"\n")
                     
        