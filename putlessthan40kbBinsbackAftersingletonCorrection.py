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
    put the less than 40 kb bin back in order after singleton correction
    python ~/aTools/utilities/putlessthan40kbBinsbackAftersingletonCorrection.py -i combinedSelectedWithStrand -b listofBinsLessThan40kb -o added40kbBinsList
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_selected_order_file' ,
                        help = "Input order file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-b" ,
                        metavar = 'list_bins_less_than_40kb_file' ,
                        help = "list bins less than 40kb file" ,
                        dest = "bins",
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
    def __init__( self, data, clusterNo, strand ) :
        self.data = data
        self.cluster = clusterNo
        self.next = None
        self.prev = None
        self.strand = strand

class LinkedList :
    def __init__( self ) :
        self.head = None
        self.tail = None
        self.size = 0        

    def add( self, data, clusterNo, count, strand ) :
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
            bins = Node(binToBeInserted, p.cluster, p.strand)
            if(pSC != rSC):
                if (right != None) and (p.strand == "plus"):
                    p.next = bins
                    bins.prev = p
                    bins.next = right
                    right.prev = bins
                
                elif (right != None) and (p.strand == "minus"):
                    print(p.data,bins.data)
                    p.prev=bins
                    bins.next=p
                    bins.prev=left
                    left.next=bins
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

def putback(input_file,bins_file,output_file):
    l = LinkedList()
    maximum=defaultdict()
    with open(input_file) as INP, open(bins_file) as BIN, open(output_file,"w") as OUT, open("binsNotAddedList","w") as NHOUT:
        count=0
        for line in INP:
            line=line.rstrip("\n")
            v=line.split("\t")
            l.add( v[0],v[1],count,v[2])
            count+=1
            scValues=v[0].split("__")
            if(scValues[0] not in maximum):
                maximum[scValues[0]]="0__0__0"
            if(int(maximum[scValues[0]].split("__")[1])<int(scValues[1])):
                maximum[scValues[0]]=v[0]
        l.reverse()
        sBef=l.getSize()
        for b in BIN:
            b=b.rstrip("\n")
            s=b.split("__")
            if(s[0] in maximum):
                b_cons=int(b.split("__")[1])-1
                max_cons=int(maximum[s[0]].split("__")[2])
                if(b_cons == max_cons):
                    l.insert(b, maximum[s[0]])
                else:
                    print("Consecutive not found for "+b)
                    NHOUT.write(b+"\n")
            else:
                NHOUT.write(b+"\n")
        sAft=l.getSize()
        l.printList(OUT)
    print("done! Size before"+str(sBef)+" Size after"+str(sAft))


#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    bins_file = os.path.abspath(arguments.bins)
    output_file = os.path.abspath(arguments.output)
    
    putback(input_file,bins_file,output_file)


#####################################################################
if __name__ == '__main__':
    main()

