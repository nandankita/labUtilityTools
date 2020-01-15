'''
Created on Mar 23, 2018

@author: nanda
'''
import argparse
import textwrap
import os
from _collections import defaultdict
from botocore.vendored.requests.packages.urllib3.connectionpool import xrange


#####################################################################

def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    It will add remaining scaffolds to the fasta file
    python ~/aTools/utilities/pairs2Scaffold.py -i added40kbBinsListWithPos -p pacbio.nodups.pairs.leng  -o pacbio.nodups.pairs.scaffolds
    python ~/aTools/utilities/pairs2Scaffold.py -i added40kbBinsListWithPos -p mapping-mappedReads-graphmap-pacbio -o mapping-mappedReads-graphmap-pacbio-scaffolds
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_scaffold position file' ,
                        help = "input scaffold position file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-p" ,
                        metavar = 'input pairs file' ,
                        help = "input pairs file" ,
                        dest = "pos",
                        required = True ,
                        type = str)
    
    parser.add_argument("-o" ,
                        metavar = 'output file' ,
                        help = "output file" ,
                        dest = "out",
                        required = True ,
                        type = str)
    
    
    return parser.parse_args()


#####################################################################
class Node :
    def __init__( self, scName, chrom, pos1, pos2 ) :
        self.scaffold = scName
        self.chromosome = chrom
        self.start = int(pos1)
        self.end = int(pos2)
        self.next = None
        

class ScaffoldList :
    def __init__( self ):
        self.head = None
        self.tail = None
        self.size = 0        

    def add( self, scName, chrom, pos1, pos2, count, scDict ) :
        node = Node(scName, chrom, pos1, pos2 )
        self.size+=1
        scDict[chrom].append(node)
        if self.head == None :    
            self.head = node
            if(count==0):
                self.tail = node
        else :
            node.next = self.head
            node.next.prev = node                        
            self.head = node
    
    def printList( self):
        node = self.head
        while node != None:
            print(node.scaffold, node.chromosome,node.start,node.end)
            #FH.write(node.data+"\t"+node.cluster+"\t"+node.strand+"\n")
            node = node.next
            
    def search( self, k, scDictChrom ) :
        d=k.split("-")
        for p in scDictChrom:
            if ( p.chromosome == d[0] ) and (int(d[1])>=p.start) and (int(d[1])<=p.end):
                return p
                break
        
    
    def getSize(self):
        return self.size
       
            
    


#####################################################################
def assignScaffold(input_file,output_file,pos):
    scDict=defaultdict(list)
    s=ScaffoldList()
    count=0
    with open(input_file,"r") as INP, open(output_file,"w") as OUT, open(pos,"r") as PAR:
        for line in INP:
            line=line.rstrip("\n")
            v=line.split("\t")
            a=v[3].split(":")
            b=a[1].split("-")
            s.add(v[0],a[0],b[0],b[1],count,scDict)
            count+=1
#         for line in PAR:
#             line=line.rstrip("\n")
#             v=line.split("\t")
#             b=v[1].split(" ")
#             pos1=b[1]
#             pos2=b[3]
#             side1=b[0]+"-"+pos1
#             side2=b[2]+"-"+pos2
#             side1Sc=s.search(side1,scDict[b[0]])
#             side2Sc=s.search(side2,scDict[b[2]])
#             OUT.write(line+"\t"+side1Sc.scaffold+"\t"+side2Sc.scaffold+"\n")
        for line in PAR:
            line=line.rstrip("\n")
            v=line.split(" ")
            pos1=v[4]
            pos2=v[5]
            side1=v[2]+"-"+pos1
            side2=v[2]+"-"+pos2
            print("read",v[0])
            print("side1",side1)
            print("side2",side2)
            
            side1Sc=s.search(side1,scDict[v[2]])
            side2Sc=s.search(side2,scDict[v[2]])
            OUT.write(line+"\t"+side1Sc.scaffold+"\t"+side2Sc.scaffold+"\n")
             



#####################################################################


def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    output_file= os.path.abspath(arguments.out)
    pos = os.path.abspath(arguments.pos)
    assignScaffold(input_file,output_file,pos)
    

#####################################################################

if __name__ == '__main__':
    main()