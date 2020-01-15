'''
Created on Oct 15, 2019

@author: nanda
'''
import sys
import numpy
import argparse
import textwrap
import os
from _collections import defaultdict


#####################################################################

def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    find out the overlapping reads given the scaffolds break
    python ~/aTools/utilities/scaffoldJuctionBoundary.py -s merged-1based.Smic1.0.sub-scaffoldList -b 10kbInsulation-filtered-manuallyCorrected.bed 
    ''') )

    parser.add_argument("-s" ,
                        metavar = 'merged scaffolds file' ,
                        help = "merged scaffolds file" ,
                        dest = "scaffolds",
                        required = True ,
                        type = str)
    
    
    parser.add_argument("-b" ,
                        metavar = 'boundaries file' ,
                        help = "boundaries file to find out the junction overlap" ,
                        dest = "bound",
                        required = True ,
                        type = str)
    

    return parser.parse_args()


####################################################################


class Node :
    def __init__( self, hicChr,hicSt,hicEnd,hicScaf):
        self.chr = hicChr
        self.st = hicSt
        self.end = hicEnd
        self.sca = hicScaf
        
        self.next = None
        self.prev = None

        
class LinkedList :
    def __init__( self ) :
        self.head = None
        self.tail = None
        self.size = 0        

    def add(self, count,hicChr,hicSt,hicEnd,hicScaf):
        node = Node(hicChr,hicSt,hicEnd,hicScaf)
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
 


####################################################################


#####################################################################
def  findJunc(scaffolds, bound):
    with open(scaffolds, "r") as scfH, open(bound, "r") as hiBd, open("tmp-juctionBoundaries.bed", "w") as juncfH, open("boundariesWithinSubscaffolds.bed", "w") as nonfH:
        count=0
        l = LinkedList()
        for hicLine in scfH:
            hicLine=hicLine.rstrip("\n")
            hicLinesp=hicLine.split("\t")
            hicChr=hicLinesp[0]
            hicSt=int(hicLinesp[1])
            hicEnd=int(hicLinesp[2])
            hicScaf=hicLinesp[3]
            l.add(count,hicChr,hicSt,hicEnd,hicScaf)
            count+=1
        l.reverse()
    
        for line in hiBd:
            line=line.rstrip("\n")
            linebd=line.split("\t")
            chB=linebd[0]
            stB=int(linebd[1])
            endB=int(linebd[2])
            filteredNode=l.get(chB)
            for i in filteredNode:
                if(i.st<=stB<i.end)and(endB>i.end):
                    #juncfH.write("\t".join([i.chr,str(i.st),str(i.end),i.sca,"\n"]))
                    juncfH.write(line+"\n")
                elif(i.st<stB<i.end)and(i.st<endB<i.end):
                    #nonfH.write("\t".join([i.chr,str(i.st),str(i.end),i.sca,"\n"]))
                    nonfH.write(line+"\n")
                
            
    
#####################################################################

def main():
    arguments = get_arguments()
    scaffolds = os.path.abspath(arguments.scaffolds)
    bound = os.path.abspath(arguments.bound)
    
    
    findJunc(scaffolds, bound)


#####################################################################
if __name__ == '__main__':
    main()
