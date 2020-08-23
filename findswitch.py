'''
Created on Jun 3, 2020

@author: nanda
python ~/aTools/utilities/findswitch.py
'''
from scalingPlotDomainsWrapper import calDominas
domains=calDominas("domains")
# for keys,value in domains.items():
#     print(len(value))
import re
import operator

class Node :
    def __init__( self, hicChr,hicSt,hicEnd,hicswitch):
        self.chr = hicChr
        self.st = hicSt
        self.end = hicEnd
        self.switch = hicswitch
        
        self.next = None
        self.prev = None


class LinkedList :
    def __init__( self ) :
        self.head = None
        self.tail = None
        self.size = 0        

    def add(self, count,hicChr,hicSt,hicEnd,hicswitch):
        node = Node(hicChr,hicSt,hicEnd,hicswitch)
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
        
    def get(self, chVal):
        node=self.head
        filterList=[]
        while node != None:
            if(node.chr==chVal):
                filterList.append(node)
            node=node.next
        return(filterList)


def filter(filteredNode, start, end):
    domainalNodes=[]
    for n in filteredNode:
        if(int(start)<=int(n.st)<=int(end)) and (int(start)<=int(n.end)<=int(end)):
            domainalNodes.append(n)
    
    return domainalNodes



with open("Coordinates_Old_annotation_to_scaffolded_smic_sorted.bed", "r") as ORD1, open("switchPositions" , "w") as ORD2:
    count=0
    l = LinkedList()
    for hicLine in ORD1:
        hicLine=hicLine.rstrip("\n")
        hicLinesp=hicLine.split("\t")
        hicChr=hicLinesp[0]
        hicSt=int(hicLinesp[1])
        hicEnd=int(hicLinesp[2])
        hicswitch=hicLinesp[5]
        l.add(count,hicChr,hicSt,hicEnd,hicswitch)
        count+=1
    l.reverse()
    
    for keychrom, valuesdomains in  domains.items():
        filteredNode=l.get(keychrom)
        for i in valuesdomains:
            signs=[]
            d=i.split(":")[1].split("-")
            filterDomainList=filter(filteredNode,d[0],d[1])
            for f in filterDomainList:
                signs.append(f.switch)
            switchString="".join(signs)


#             a = re.sub(r'(?<!\+)\+(?=[^\+]|$)', '-', switchString)
#             c = re.sub(r'(?<!\-)\-(?=[^\-]|$)', '+', a)
#             d = re.sub(r'(?<!\+)\+\+(?=[^\+]|$)', '--', c)
#             e = re.sub(r'(?<!\-)\-\-(?=[^\-]|$)', '++', d)
#             f = re.sub(r'(?<!\+)\+\+\+(?=[^\+]|$)', '---', e)
#             b = re.sub(r'(?<!\-)\-\-\-(?=[^\-]|$)', '+++', f)

            a = re.sub(r'(?<!\+)\+(?=[^\+]|$)', '-', switchString)
            b = re.sub(r'(?<!\-)\-(?=[^\-]|$)', '+', a)
            
            pos=[str(match.span())+"_"+(str(match.end()-match.start())) for match in re.finditer(r'\+{2,}((?=[^+])|$)', b)]
            neg=[str(match.span())+"_"+(str(match.end()-match.start()))  for match in re.finditer(r'\-{2,}((?=[^-])|$)', b)]
            indexP = lenMostP = indexN = lenMostN = 0
            
            if("+" in b) and ("-" in b):
                indexP, lenMostP = max(enumerate([int(i.split("_")[1]) for i in pos]), key=operator.itemgetter(1))
                indexN, lenMostN = max(enumerate([int(i.split("_")[1]) for i in neg]), key=operator.itemgetter(1))
            
            #max_n = max(pos, key=enumerate([i.split("")[1] for i in pos]))
                locP=eval(pos[indexP].split("_")[0])
                locN=eval(neg[indexN].split("_")[0])
            
#                 if(lenMostP>lenMostN) and :
#                     locP=pos[indexP]
#                 
                if(lenMostN>lenMostP) and (locN[1] < locP[1]):
                    switchLocation=filterDomainList[locN[1]].end
                
                elif(lenMostN>lenMostP) and (locN[1] > locP[1]):
                    switchLocation=filterDomainList[locN[0]].end
                
                elif(lenMostN<lenMostP) and (locN[1] > locP[1]):
                    switchLocation=filterDomainList[locP[1]].end
                
                elif(lenMostN<lenMostP) and (locN[1] < locP[1]):
                    switchLocation=filterDomainList[locP[0]].end
                
                elif(lenMostN==lenMostP) and (locN[1] < locP[1]):
                    switchLocation=filterDomainList[locN[1]].end
                
                elif(lenMostN==lenMostP) and (locN[1] > locP[1]):
                    switchLocation=filterDomainList[locP[1]].end
                    
                else:
            
                    print(b,pos,neg,lenMostP,lenMostN)
            
            
                ORD2.write("\t".join([keychrom,str(int(switchLocation)-5000),str(int(switchLocation)+5000)+"\n"]))
    
