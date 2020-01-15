'''
Created on Aug 20, 2018

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
    Given a scaffold list considering cluster number, strand and continuity.
    python3 ~/aTools/utilities/mergeScaffolds.py -i cutSc-newScaffoldList1kb60percent -o merged-cutSc-newScaffoldList1kb60percent 
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_scaffold_file' ,
                        help = "Input scaffold file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-o" ,
                        metavar = 'output_scaffold_file.' ,
                        help = "output_scaffold_file." ,
                        dest = "output",
                        required = True ,
                        type = str)
    
    
    return parser.parse_args()

#####################################################################

#####################################################################
class Node :
    def __init__( self, data, clusterNo,strand ) :
        self.data = data
        self.cluster = clusterNo
        self.strand = strand
        self.next = None
        self.prev = None
        
class LinkedList :
    def __init__( self ) :
        self.head = None
        self.tail = None
        self.size = 0        

    def add( self, data, clusterNo, strand, count ) :
        node = Node( data, clusterNo, strand )
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

def writeNode(pointNode,node,outFH):
    a=node.data.split("__")
    b=pointNode.data.split("__")
    if(node.prev==None):
        v="__".join([a[0],a[1],a[2]])
    else:
        previous=node.prev
        if(previous.strand=="minus") or (previous.strand=="+"):
            v="__".join([a[0],a[1],b[2]])
            
            
        if(previous.strand=="plus") or (previous.strand=="-"):
            v="__".join([a[0],b[1],a[2]])
            
        
    outFH.write("\t".join([v,node.cluster,node.strand]))
    outFH.write("\n")

#####################################################################
def merge(input_file,output_file):
    with open(input_file) as inFH, open(output_file, "w") as outFH:
        l = LinkedList()
        count=0
        for line in inFH:
            line=line.rstrip("\n")
            v=line.split("\t")
            l.add( v[0], v[1], v[2],count)
            count+=1
        l.reverse()
        
        print("Linked List Ready, processing..")
        finalList=[]
        node = l.head
        pointNode=l.head
        while node != None:
            current=node.data.split("__")
            if(node.next != None):
                
                nxt=node.next.data.split("__")
                current=node.data.split("__")
                
                
                if((node.strand==node.next.strand) and (node.cluster==node.next.cluster) and (current[0]==nxt[0]) and ((int(current[1])-1)==int(nxt[2]))) or ((node.strand==node.next.strand) and (node.cluster==node.next.cluster) and (current[0]==nxt[0]) and ((int(current[2])+1)==int(nxt[1]))):
                    pass
                
                    
                else:
                    writeNode(pointNode,node,outFH)
                    pointNode=node.next
            else:
                writeNode(pointNode,node,outFH)
                
            node=node.next
        
        for i in finalList:
            outFH.write(i+"\n")


#####################################################################


def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    output_file = os.path.abspath(arguments.output)
    merge(input_file,output_file)
    

#####################################################################

if __name__ == '__main__':
    main()