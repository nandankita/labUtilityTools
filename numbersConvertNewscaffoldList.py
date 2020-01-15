'''
Created on Jul 31, 2018

@author: nanda
'''

from Bio import SeqIO
from Bio.Seq import Seq
import argparse
import textwrap
import os
from _collections import defaultdict
from scipy.interpolate import interp1d

#####################################################################

def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Delete the given bins and create new scaffold list.
    python3 ~/aTools/utilities/numbersConvertNewscaffoldList.py -i singCorrectListHang4NMPos -n unselectedIndexLocation1kb60percentMergedSort 
    python3 ~/aTools/utilities/numbersConvertNewscaffoldList.py -i pstest -n rmtest 
    python3 ~/aTools/utilities/numbersConvertNewscaffoldList.py -i singCorrectListHang4NMPos -n uniqSortTotalAppendedIndx
    
    http://guest.dekkerlab.org/app/?config=I49kdlmUThyPxPhQlAu9CA
    http://guest.dekkerlab.org/app/?config=DiT1I45tQvyoA3Ijd3yIbg

    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_scaffold_postion_file' ,
                        help = "Input scaffold_postion file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-n" ,
                        metavar = 'Bins to be removed file.' ,
                        help = "Bins to be removed file." ,
                        dest = "order",
                        required = True ,
                        type = str)
    
    
    return parser.parse_args()

#####################################################################

class Node :
    def __init__( self, data, cluster, strand, chromosome, mapping,filtered ):
        self.data = data
        self.cluster = cluster
        self.strand = strand
        self.chromosome = chromosome
        self.mapping = mapping
        self.filtered = filtered
        self.anotherScaffoldList = []
        self.next = None
        self.prev = None
        self.skip = False
        
class LinkedList :
    def __init__( self ) :
        self.head = None
        self.tail = None
        self.size = 0        

    def add( self, data, cluster, strand, chromosome, mapping, filtered, count ) :
        node = Node( data, cluster, strand, chromosome, mapping, filtered )
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
def filterList(removelocs,chrLoc):
    filtered=[]
    for i in removelocs:
        loc=i.split("-")
        if(int(chrLoc[0])<=int(loc[0])<=int(chrLoc[1])) or (int(chrLoc[0])<=int(loc[1])<=int(chrLoc[1])):
            filtered.append(range(int(loc[0]),int(loc[1])))
    return(filtered)
    
def findNew(ls,i):
    loc=i.split("-")
    for v in ls:
        n=v.split("\t")[3].split(":")[1]
        chrLoc=n.split("-")
        if(int(chrLoc[0])<=int(loc[0])<=int(chrLoc[1])) or (int(chrLoc[0])<=int(loc[1])<=int(chrLoc[1])):
            return(n)
    return None

###################################################################
def findrange(anotherScaffoldList,val):
    for i in anotherScaffoldList:
        st=i.start
        end=i.stop+1
        if val in range(st,end):
            return i
    return None

##################################################################

def takeStart(elem):
    return elem.start


####################################################################

def filterInsideRange(node,chrLocataionRange):
    #print(node.filtered, chrLocataionRange)
    for sub_range in node.filtered:
        start=sub_range.start
        end=sub_range.stop
        if(chrLocataionRange.start<start) and (end<chrLocataionRange.stop):
            value2updateSt=findrange(node.anotherScaffoldList,start)
            if(value2updateSt != None):
                node.anotherScaffoldList.append(range(value2updateSt.start,start-1))
                node.anotherScaffoldList.append(range(start,value2updateSt.stop))
                node.anotherScaffoldList.remove(value2updateSt)
                
            
            value2updateEnd=findrange(node.anotherScaffoldList,end)
            if(value2updateEnd != None):
                node.anotherScaffoldList.append(range(end+1,value2updateEnd.stop))
                node.anotherScaffoldList.remove(value2updateEnd)
            
            
            
def filterOneInsideRange(node,chrLocataionRange):
    for sub_range in node.filtered:
        start=sub_range.start
        end=sub_range.stop
        if(chrLocataionRange.start<start<chrLocataionRange.stop) and (chrLocataionRange.stop<end):
            value2updateSt=findrange(node.anotherScaffoldList,start)
            if(value2updateSt != None):
                node.anotherScaffoldList.append(range(value2updateSt.start,start-1))
                node.anotherScaffoldList.remove(value2updateSt)
        
        
        if(chrLocataionRange.start<end<chrLocataionRange.stop) and (start<chrLocataionRange.start):
            value2updateEnd=findrange(node.anotherScaffoldList,end)
            if(value2updateEnd != None):
                node.anotherScaffoldList.append(range(end+1,value2updateEnd.stop))
                node.anotherScaffoldList.remove(value2updateEnd)
                 
            
def filterOneEqualRange(node,chrLocataionRange):
    for sub_range in node.filtered:
        start=sub_range.start
        end=sub_range.stop
        if(chrLocataionRange.start==start<chrLocataionRange.stop):
            value2updateSt=findrange(node.anotherScaffoldList,start)
            if(value2updateSt != None):
                node.anotherScaffoldList.append(range(end+1,value2updateSt.stop))
                node.anotherScaffoldList.remove(value2updateSt)
        
        
        if(chrLocataionRange.start==end<chrLocataionRange.stop):
            value2updateEnd=findrange(node.anotherScaffoldList,end)
            if(value2updateEnd != None):
                node.anotherScaffoldList.append(range(end+1,value2updateEnd.stop))
                node.anotherScaffoldList.remove(value2updateEnd)
        
        if(chrLocataionRange.start<start==chrLocataionRange.stop):
            value2updateSt=findrange(node.anotherScaffoldList,start)
            if(value2updateSt != None):
                node.anotherScaffoldList.append(range(value2updateSt.start,start-1))
                node.anotherScaffoldList.remove(value2updateSt)
        
        if(chrLocataionRange.start<end==chrLocataionRange.stop):
            value2updateEnd=findrange(node.anotherScaffoldList,end)
            if(value2updateEnd != None):
                node.anotherScaffoldList.append(range(value2updateEnd.start,start-1))
                node.anotherScaffoldList.remove(value2updateEnd)     
        
def skipNode(node,chrLocataionRange):
    skip=False
    if(node.prev != None):
        lastFilteredList=node.prev.filtered
        for i in lastFilteredList:
            lstStart=i.start
            lstEnd=i.stop
            if(lstStart<chrLocataionRange.start) and (lstEnd>=chrLocataionRange.stop):
                skip=True
    for sub_range in node.filtered:
        start=sub_range.start
        end=sub_range.stop
        if(start==chrLocataionRange.start) and (end==chrLocataionRange.stop):
            skip=True
        if(start==chrLocataionRange.start) and (end>chrLocataionRange.stop):
            skip=True
        if(start<chrLocataionRange.start) and (end>chrLocataionRange.stop):
            print("Here??")
            skip=True
    
    node.skip=skip
    return skip
        


    
#####################################################################
def createFasta(input_file,order):
    output_file="newScaffoldList"
    removeLs = defaultdict(list)
    with open(input_file) as SCPLIST, open(order) as ORD, open(output_file, "w") as OUTFH:
        for l in ORD:
            l=l.rstrip("\n")
            val=l.split(":")
            removeLs[val[0]].append(val[1])
        count=0
        l = LinkedList()
        for line in SCPLIST:
            line=line.rstrip("\n")
            v=line.split("\t")
            sc=v[0].split("__")
            chro=v[3].split(":")
            chrLoc=chro[1].split("-")
            if(v[2]=="minus"):
                m = interp1d([int(chrLoc[0]),int(chrLoc[1])],[int(sc[2]),int(sc[1])])
                
            if(v[2]=="plus"):
                m = interp1d([int(chrLoc[0]),int(chrLoc[1])],[int(sc[1]),int(sc[2])])
            
            filtered = filterList(removeLs[chro[0]],chrLoc)
            
            ##data, cluster, strand, chromosome, mapping,filtered 
            l.add( v[0], v[1], v[2],chro[1],m,filtered,count)
            count+=1
        l.reverse()
        
        node = l.head
        while node != None:
            #print(node.data, node.cluster, node.strand, node.chromosome, node.mapping.x, node.mapping.y, node.filtered)
            chrLocataion=node.chromosome.split("-")
            chrLocataionRange=range(int(chrLocataion[0]),int(chrLocataion[1]))
            node.anotherScaffoldList.append(chrLocataionRange)
            
            skip=skipNode(node,chrLocataionRange)
            
            if(skip==False):
                filterInsideRange(node,chrLocataionRange)
                filterOneInsideRange(node,chrLocataionRange)
                filterOneEqualRange(node,chrLocataionRange)
                if(len(node.anotherScaffoldList)>0):
                    node.anotherScaffoldList = sorted(node.anotherScaffoldList,key=takeStart)
            
            
            
            node=node.next
        
        node = l.head
        while node != None:
            if(node.skip==False):
                scf=node.data.split("__")
                #print(node.data,node.chromosome,node.filtered,node.anotherScaffoldList, node.skip)
                #print(node.data,node.chromosome,node.anotherScaffoldList,node.mapping.x,node.mapping.y)
                for n in node.anotherScaffoldList:
                    if(not(n.start>=n.stop)):
                        if(node.strand=="plus"):
                            v=scf[0]+"__"+str(int(node.mapping(n.start)))+"__"+str(int(node.mapping(n.stop)))
                        else:
                            v=scf[0]+"__"+str(int(node.mapping(n.stop)))+"__"+str(int(node.mapping(n.start)))
                        a="\t".join([v,node.cluster,node.strand,"chr"+str(int(node.cluster)+1)+":"+str(n.start)+"-"+str(n.stop)])
                        OUTFH.write(a+"\n")
                    
            node=node.next
        print("done")
            
           

#####################################################################


def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    order = os.path.abspath(arguments.order)
    createFasta(input_file,order)
    

#####################################################################

if __name__ == '__main__':
    main()