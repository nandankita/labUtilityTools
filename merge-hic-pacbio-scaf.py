
'''
python ~/aTools/utilities/merge-hic-pacbio-scaf.py
'''
from _collections import defaultdict


#####################################################################

class Node :
    def __init__( self, hicChr,hicSt,hicEnd):
        self.chr = hicChr
        self.st = hicSt
        self.end = hicEnd
        
        self.next = None
        self.prev = None

        
class LinkedList :
    def __init__( self ) :
        self.head = None
        self.tail = None
        self.size = 0        

    def add( self, count,hicChr,hicSt,hicEnd):
        node = Node(hicChr,hicSt,hicEnd)
        self.size+=1
        if self.head == None :    
            self.head = node
            if(count==0):
                self.tail = node
        else :
            node.next = self.head
            node.next.prev = node                        
            self.head = node            
    
    def reverse(self):
        node=self.tail
        while node != None:
            p=node.prev
            n=node.next
            node.prev=n
            node.next=p
            node = p
        t=self.tail
        h=self.head
        self.head=t
        self.tail=h
 


####################################################################


scfList=defaultdict(list)
#hicList=defaultdict(list)

with open("scaffold", "r") as scfH, open("merged-hic-pacbio", "r") as hifH, open("merged-scaffold-hic-pacbio.bed", "w") as mrgfH:
    for line in scfH:
        line=line.rstrip("\n")
        linesp=line.split("\t")
        scfChr=linesp[0]
        scfSt=int(linesp[1])
        scfEnd=int(linesp[2])
        scfList[scfChr].append([scfSt,scfEnd])
    
    
    count=0
    l = LinkedList()
    for hicLine in hifH:
        hicLine=hicLine.rstrip("\n")
        hicLinesp=hicLine.split("\t")
        hicChr=hicLinesp[0]
        hicSt=int(hicLinesp[1])
        hicEnd=int(hicLinesp[2])
        l.add(count,hicChr,hicSt,hicEnd)
        count+=1
    l.reverse()
    
    
    for scKeys, scValues in sorted(scfList.items()):
        print(scKeys)
        for scValue in scValues:
            hic = l.head
            while hic != None:
                #print(scKeys,scValue,hic.chr,hic.st,hic.end)
                if(hic.chr==scKeys) and (scValue[0]<hic.end<scValue[1]):
                    if(hic.next.chr==scKeys) and (scValue[0]<hic.next.st<scValue[1]):
                        mrgfH.write("\t".join([hic.chr,str(hic.st),str(hic.next.end)]))
                        mrgfH.write("\n")
                        hic=hic.next
                    else:
                        mrgfH.write("\t".join([hic.chr,str(hic.st),str(hic.end)]))
                        mrgfH.write("\n")
                elif(hic.end>scValue[1]):
                    mrgfH.write("\t".join([hic.chr,str(hic.st),str(hic.end)]))
                    mrgfH.write("\n")
                else:
                    pass
    
                hic=hic.next
             
    
    
    
#          
#         hicList[hicChr].append([hicSt,hicEnd])
#     
#     
#     
#     for scKeys, scValues in sorted(scfList.items()):
#         count=0
#         print(scKeys)
#         if(count<len(scValues)):
#             scValue=scValues[count]
#         newList=[]
#         sortedNewList=[]
#             print("hicList",hicList[scKeys])
#             print("scvalue",scValue)
#             break
#         for hicValue in hicList[scKeys]:
#             print(scValue,hicValue)
#             if(scValue[0]<=hicValue[0]<scValue[1]) and (scValue[0]<hicValue[1]<=scValue[1]):
#                 newList.append(hicValue)
#                 
#             
#             
#             else:
#                 if(len(newList)>0):
#                     sortedNewList=sorted(newList, key=lambda x:x[0], reverse=False)
#                      
#                     newRangeSt=sortedNewList[0][0]
#                     newRangeEnd=sortedNewList[len(sortedNewList)-1][1]
#                      
#                     mrgfH.write("\t".join([scKeys,str(newRangeSt),str(newRangeEnd)]))
#                     mrgfH.write("\n")
#                     newList=[]
#                     sortedNewList=[]
#                 
#                 count+=1
#                 if(count<len(scValues)):
#                     scValue=scValues[count]
#                     newList=[]
#                     sortedNewList=[]
#                     
#                     if(scValue[0]<=hicValue[0]<scValue[1]) and (scValue[0]<hicValue[1]<=scValue[1]):
#                         newList.append(hicValue)
#                     
#                     else:
#                         mrgfH.write("\t".join([scKeys,str(hicValue[0]),str(hicValue[1])]))
#                         mrgfH.write("\n")
#                 
#         ind=0
#         for hicValue in hicList[scKeys]:
#             
#             if(ind+1<len(hicList[scKeys])):
#                 if(scValue[0]<=hicValue[1]) and (hicList[scKeys][ind+1][0]<=scValue[1]):
#                     newList.append(hicValue)
#                     newList.append(hicList[scKeys][ind+1])
#             
#             else:
#                 if(len(newList)>0):
#                     sortedNewList=sorted(newList, key=lambda x:x[0], reverse=False)
#                      
#                     newRangeSt=sortedNewList[0][0]
#                     newRangeEnd=sortedNewList[len(sortedNewList)-1][1]
#                      
#                     mrgfH.write("\t".join([scKeys,str(newRangeSt),str(newRangeEnd)]))
#                     mrgfH.write("\n")
#                     newList=[]
#                     sortedNewList=[]
#                 
#                 count+=1
#                 if(count<len(scValues)):
#                     scValue=scValues[count]
#                     newList=[]
#                     sortedNewList=[]
#                     
#                     if(ind+1<len(hicList[scKeys])):
#                         if(scValue[0]<=hicValue[1]) and (hicList[scKeys][ind+1][0]<=scValue[1]):
#                             newList.append(hicValue)
#                             newList.append(hicList[scKeys][ind+1])
#                     
#                     else:
#                         mrgfH.write("\t".join([scKeys,str(hicValue[0]),str(hicValue[1])]))
#                         mrgfH.write("\n")
#             
#             ind+=1

    
                        
        
           
            
            
            
            