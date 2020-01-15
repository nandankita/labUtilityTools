'''
Created on Aug 21, 2018

@author: nanda
'''

from Bio import SeqIO
from Bio.Seq import Seq
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
    Sorting scaffold list accoring to new chromosome list
    python ~/aTools/utilities/sortScaffoldListFile.py -i merged-cutSc-newScaffoldList1kb60percent -n mappingChr2sortedchromosomesizes
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_scaffold_file' ,
                        help = "Input scaffold file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-n" ,
                        metavar = 'input mapping file' ,
                        help = "input mapping  file" ,
                        dest = "mapping",
                        required = True ,
                        type = str)
    
    
    return parser.parse_args()

###################################################################
#####################################################################
def sortChr(input_file,mapping):
    output_file="scaffoldList-dino-v1.0-sorted"
    inDict=defaultdict(list)
    with open(input_file) as IN, open(mapping) as ORD, open(output_file, "w") as OUTFH:
        
        for line in IN:
            line=line.rstrip("\n")
            m=line.split("\t")
            inDict[m[1]].append(line)
        
#        print(inDict)
#         for i in inDict["1"]:
#             v=i.split("\t")
#             if(v[0]=="Smic.scaffold93__1122759__1160758"):
#                 print("Here")
                   
        print("Read scaffolds - mapping now")
        
        for l in ORD:
            l=l.rstrip("\n")
            p=l.split("\t")
            inChr=str(int(p[0][3:len(p[0])])-1)
            outChr=str(int(p[2][3:len(p[2])])-1)
            #print(l,p,inChr,outChr)
            print("Writing "+outChr+" mapped from "+inChr)
            for i in inDict[inChr]:
                v=i.split("\t")
                a="\t".join([v[0],outChr,v[2]])
                OUTFH.write(a+"\n")
                
            

#####################################################################


def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    mapping = os.path.abspath(arguments.mapping)
    sortChr(input_file,mapping)
    

#####################################################################

if __name__ == '__main__':
    main()
