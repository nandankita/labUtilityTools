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
    find bins postions
    python ~/aTools/utilities/findBinPostions.py -i added40kbBinsList -o added40kbBinsListWithPos
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
    def __init__( self, data, clusterNo, strand, pos ) :
        self.data = data
        self.cluster = clusterNo
        self.pos = pos
        self.next = None
        self.prev = None
        self.strand = strand

class LinkedList :
    def __init__( self ) :
        self.head = None
        self.tail = None
        self.size = 0        

    def add( self, data, clusterNo, strand, count, pos ) :
        node = Node( data, clusterNo, strand, pos )
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
    
    def printList( self,FH ):
        node = self.head
        while node != None:
            #print(node.data, node.strand)
            FH.write(node.data+"\t"+node.cluster+"\t"+node.strand+"\t"+node.pos+"\n")
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

def findPos(input_file,output_file):
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
            l.add( v[0], v[1], v[2], count, pos)
            count+=1
            currentChr=v[1]
        l.reverse()
        l.printList(OUT)
        print("done!")


#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    output_file = os.path.abspath(arguments.output)
    
    findPos(input_file,output_file)


#####################################################################
if __name__ == '__main__':
    main()

