'''
Created on Jan 23, 2018

@author: nanda
'''
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
    find singleton bins
    python ~/aTools/utilities/findSingletonBins.py -i combinedSelectedOrderWithclusterNumber-part2.txt -o singletonBins
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_selected_order_file' ,
                        help = "Input order file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    
    parser.add_argument("-o" ,
                        metavar = 'output_file' ,
                        help = "output file" ,
                        dest = "output",
                        required = True ,
                        type = str)
    

    
    return parser.parse_args()


#########################################################

class Node :
    def __init__( self, data, clusterNo, pos ) :
        self.data = data
        self.cluster = clusterNo
        self.position = pos
        self.next = None
        self.prev = None
        self.strand = None

class LinkedList :
    def __init__( self ) :
        self.head = None
        self.tail = None
        self.size = 0        

    def add( self, data, clusterNo, count, pos ) :
        node = Node( data, clusterNo, pos )
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
    
    def findSg(self, OUT):
        node = self.head
        while node != None:
            nextNode=None
            lastNode=None
            pointerNode=node.data.split("__")[0]
            if (node.next != None):
                nextNode=node.next.data.split("__")[0]
            if (node.prev !=None):
                lastNode=node.prev.data.split("__")[0]
            if(pointerNode != nextNode  and pointerNode !=lastNode):
                #OUT.write(node.data+"\t"+node.cluster+"\t"+node.position+"\n")
                OUT.write(node.data+"\t"+node.cluster+"\n")
            node = node.next
            

    def getSize(self):
        return self.size
    
#####################################################################

def findSingleton(input_file,output_file):
    l = LinkedList()
    with open(input_file) as INP, open(output_file,"w") as OUT:
        count=0
        currentChr=0
        p=1 
        for line in INP:
            line=line.rstrip("\n")
            v=line.split("\t")
            blk=v[0].split("__")
            blkSize=int(blk[2])-int(blk[1])
            if(int(currentChr) != int(v[1])):
                p=1
            c=str(int(v[1])+1)
            pos="chr"+c+":"+str(p)+"-"+str(p+blkSize)
            p+=blkSize+1
            l.add( v[0], v[1],count,pos)
            count+=1
            currentChr=v[1]
        l.reverse()
        l.findSg(OUT)
        


#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    output_file = os.path.abspath(arguments.output)
    
    findSingleton(input_file,output_file)


#####################################################################
if __name__ == '__main__':
    main()
    