'''
Created on Dec 6, 2017

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
    Do strand assignment for dino genome
    python ~/aTools/utilities/strandassignment.py -i combinedSelectedOrderWithclusterNumber-part2.txt -o combinedSelectedWithStrand
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
    def __init__( self, data, clusterNo ) :
        self.data = data
        self.cluster = clusterNo
        self.next = None
        self.prev = None
        self.strand = None

class LinkedList :
    def __init__( self ) :
        self.head = None
        self.tail = None
        self.size = 0        

    def add( self, data, clusterNo, count ) :
        node = Node( data, clusterNo )
        self.size+=1
        if self.head == None :    
            self.head = node
            if(count==0):
                self.tail = node
        else :
            node.next = self.head
            node.next.prev = node                        
            self.head = node            

    def search( self, k ) :
        p = self.head
        if p != None :
            while p.next != None :
                if ( p.data == k ) :
                    return p                
                p = p.next
            if ( p.data == k ) :
                return p
        return None
    
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

    def remove(self, p):
        if p==None:
            #return p;
            print ('Searched Element does not exist in the defined linked list');
            return;
        if p == self.head:
            self.size-=1
            tmp = p
            p.next.prev = p.prev
            self.head = p.next
        else:
            self.size-=1
            tmp = p
            p.prev.next = p.next
            p.next.prev = p.prev
        del tmp;
        return;
    
    def insert(self, binToBeInserted, maxV):
        if binToBeInserted is None:
            raise ValueError('Cannot add None item to a list')
            return;
        else:
            p=self.search(maxV)
            pSC=p.data.split("__")[0]
            left=p.prev
            right=p.next
            if(right):
                rSC=right.data.split("__")[0]
            else:
                rSC=None
            bins = Node(binToBeInserted, p.cluster)
            if(pSC != rSC):
                if (right != None):
                    p.next = bins
                    bins.prev = p
                    bins.next = right
                    right.prev = bins
                    
                else:
                    print("Right None")
                    p.next = bins
                    bins.prev = p
                    self.tail=bins
            else:
                if(p == self.head):
                    p.prev=bins
                    bins.next=p
                    self.head = bins
                    
                else:
                    p.prev=bins
                    bins.next=p
                    bins.prev=left
                    left.next=bins
            self.size+=1
                    
    def printList( self,FH ):
        node = self.head
        while node != None:
            #print(node.data, node.strand)
            FH.write(node.data+"\t"+node.cluster+"\t"+node.strand+"\n")
            node = node.next
        
    def assignStrand(self):
        node = self.head
        while node != None:
            pointerNode=node.data.split("__")
            if (node.next != None and node.prev !=None):
                nextNode=node.next.data.split("__")
                lastNode=node.prev.data.split("__")
                if(pointerNode[0] == nextNode[0]):
                    if(int(pointerNode[1])<int(nextNode[1])):
                        node.strand="plus"
                    else:
                        node.strand="minus"
                elif(pointerNode[0] == lastNode[0]):
                    if(int(pointerNode[1])>int(lastNode[1])):
                        node.strand="plus"
                    else:
                        node.strand="minus"
                else:
                    node.strand="plus"
            elif(node.next == None):
                lastNode=node.prev.data.split("__")
                if(pointerNode[0] == lastNode[0]):
                    if(int(pointerNode[1])>int(lastNode[1])):
                        node.strand="plus"
                    else:
                        node.strand="minus"
                else:
                    node.strand="plus"
            elif(node.prev == None):
                nextNode=node.next.data.split("__")
                if(pointerNode[0] == nextNode[0]):
                    if(int(pointerNode[1])<int(nextNode[1])):
                        node.strand="plus"
                    else:
                        node.strand="minus"
                else:
                    node.strand="plus"
            else:
                node.strand="plus"

            node = node.next
            
    
    def getSize(self):
        return self.size

    def __str__( self ) :
        s = ""
        p = self.head
        if p != None :        
            while p.next != None :
                s += p.data
                p = p.next
            s += p.data
        return s



#####################################################################

def assignStrand(input_file,output_file):
    l = LinkedList()
    with open(input_file) as INP, open(output_file,"w") as OUT:
        count=0
        for line in INP:
            line=line.rstrip("\n")
            v=line.split("\t")
            l.add( v[0], v[1],count)
            count+=1
        l.reverse()
        sBef=l.getSize()
        l.assignStrand()
        sAft=l.getSize()
        l.printList(OUT)
    print("done! Size before"+str(sBef)+" Size after"+str(sAft))


#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    output_file = os.path.abspath(arguments.output)
    
    assignStrand(input_file,output_file)


#####################################################################
if __name__ == '__main__':
    main()

