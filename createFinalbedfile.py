'''
Created on Jul 24, 2018

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
    Create a bed from intermediate bed file 
    python ~/aTools/utilities/createFinalbedfile.py -i scaffoldList-dino-v1.0-sorted-Pos -m fasta/mappingChr2sortedchromosomesizes  -o dino-v1.0-scaffolds.bed
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_scaffold Position file' ,
                        help = "input_scaffold Position file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-m" ,
                        metavar = 'input_chromosome_mapping_file' ,
                        help = "input_chromosome_mapping_file" ,
                        dest = "map",
                        required = True ,
                        type = str)
    
    
    parser.add_argument("-o" ,
                        metavar = 'output_bed file' ,
                        help = "output_bed file" ,
                        dest = "output",
                        required = True ,
                        type = str)

    return parser.parse_args()

########################################################
def createList(input_file,map_file, output_file):
    mapDict=defaultdict()
    with open(input_file) as inFH,  open(map_file) as mapFH, open(output_file, "w") as outFH:
        for l in mapFH:
            l=l.rstrip("\n")
            m=l.split("\t")
            inChr=m[0][3:]
            outChr=m[2][3:]
            mapDict[outChr]=inChr
        outFH.write("track name=\"dino-v1.0\" description=\"dino-1.0-Scaffolds\" visibility=2 itemRgb=\"On\"\n")
        for line in inFH:
            line=line.rstrip("\n")
            v=line.split("\t")
            c=v[3].split(":")
            loc=c[1].split("-")
            start=str(int(loc[0])-1)
            if(v[2]=="plus"):
                tmp="+"
                color="0,0,255"
            else:
                tmp="-"
                color="255,0,0"
                
            chrm=mapDict[str(int(v[1])+1)]
            a="\t".join([c[0],start,loc[1],v[0],str(chrm),tmp,start,loc[1],color])
            outFH.write(a+"\n")

#######################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    output_file = os.path.abspath(arguments.output)
    map_file = os.path.abspath(arguments.map)
    createList(input_file, map_file, output_file)


#####################################################################
if __name__ == '__main__':
    main()
    