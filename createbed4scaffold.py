'''
Created on Jun 20, 2017

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
    Create a bed intermidiate file from scaffold position file . 
    python ~/aTools/utilities/createbed4scaffold.py -i singCorrectListHang4NMPos -o bedsingCorrectListHang4NMPos
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_scaffold_Pos_file' ,
                        help = "input scaffold pos file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-o" ,
                        metavar = 'output_scaffold_file' ,
                        help = "output scaffold file" ,
                        dest = "output",
                        required = True ,
                        type = str)

    return parser.parse_args()


#########################################################

class Node :
    def __init__( self, data, clusterNo, strand, chrmosome ) :
        self.data = data
        self.cluster = clusterNo
        self.strand = strand
        self.chrmosome = chrmosome
        self.next = None
        self.prev = None

class LinkedList :
    def __init__( self ) :
        self.head = None
        self.tail = None
        self.size = 0        

    def add( self, data, clusterNo, strand, chrmosome, count) :
        node = Node( data, clusterNo, strand, chrmosome)
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
    
    def merge(self,outFH):
        p = self.head
        endloc=""
        stLoc=""
        stchLoc=""
        currentSc=""
        while p != None:
            #print(p.data, p.cluster, p.strand, p.chrmosome)
            sc=p.data.split("__")
            chrm=p.chrmosome.split(":")
            chrmLoc=chrm[1].split("-")
            if (currentSc==""):
                endloc=sc[2]
                stLoc=sc[1]
                stchLoc=chrmLoc[0]
                currentSc=sc[0]
            if(p.next != None):
                if (not (p.next.data.split("__")[0]==p.data.split("__")[0])):
                    if((p.strand=="minus") ):
                            outFH.write("__".join([sc[0],endloc,sc[1]])+"\t"+"__".join([chrm[0],stchLoc,chrmLoc[1]])+"\t"+p.strand+"\n")
                            currentSc=""
                    elif((p.strand=="plus") and (p.next!= None)):
                        if not (p.next.data.split("__")[0]==p.data.split("__")[0]):
                            outFH.write("__".join([sc[0],stLoc,sc[2]])+"\t"+"__".join([chrm[0],stchLoc,chrmLoc[1]])+"\t"+p.strand+"\n")
                            currentSc=""
                elif (p.next.data.split("__")[0]==p.data.split("__")[0]):
                    if((p.strand=="minus") and (not (int(p.data.split("__")[1])-1)==int(p.next.data.split("__")[2]))):
                            outFH.write("__".join([sc[0],endloc,sc[1]])+"\t"+"__".join([chrm[0],stchLoc,chrmLoc[1]])+"\t"+p.strand+"\n")
                            currentSc=""
                    elif((p.strand=="plus") and (not (int(p.data.split("__")[2])+1)==int(p.next.data.split("__")[1]))):
                        if not (p.next.data.split("__")[0]==p.data.split("__")[0]):
                            outFH.write("__".join([sc[0],stLoc,sc[2]])+"\t"+"__".join([chrm[0],stchLoc,chrmLoc[1]])+"\t"+p.strand+"\n")
                            currentSc=""
            else:
                outFH.write("__".join([sc[0],endloc,sc[1]])+"\t"+"__".join([chrm[0],stchLoc,chrmLoc[1]])+"\t"+p.strand+"\n")
                currentSc=""
            
                    
            p = p.next
    
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
def createList(input_file, output_file):
    l = LinkedList()
    with open(input_file) as inFH, open(output_file, "w") as outFH:
        count=0
        for line in inFH:
            line=line.rstrip("\n")
            v=line.split("\t")
            l.add( v[0], v[1], v[2], v[3], count)
            count+=1
        l.reverse()
        l.merge(outFH)
        
            
            
#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    output_file = os.path.abspath(arguments.output)

    createList(input_file, output_file)


#####################################################################
if __name__ == '__main__':
    main()
    