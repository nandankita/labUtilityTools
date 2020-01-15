'''
Created on Apr 16, 2019

@author: nanda
python ~/aTools/utilities/findOverlapsWithScaffolds.py -s 10kbInsulation-filtered-manuallyCorrected.bed -r col.merged.combined.pacbio.blasr.bed 
python ~/aTools/utilities/findOverlapsWithScaffolds.py -s merged-1based.Smic1.0.sub-scaffoldList -r pacbio.minimap2.combined.merged.1based.bed
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
    ''') )

    parser.add_argument("-s" ,
                        metavar = 'merged scaffolds file' ,
                        help = "merged scaffolds file" ,
                        dest = "scaffolds",
                        required = True ,
                        type = str)
    
    
    parser.add_argument("-r" ,
                        metavar = 'reads to find out the overlaps' ,
                        help = "reads to find out the overlaps" ,
                        dest = "reads",
                        required = True ,
                        type = str)
    

    return parser.parse_args()

#####################################################################
def findOverlaps(scaffolds, reads_file):
    scaffoldList=defaultdict(list)
    readList=defaultdict(list)
    with open(scaffolds, "r") as lineFH, open(reads_file, "r") as readsFH, open("scaffolds_overlap_file", "w") as overFH:
        for line in lineFH:
            line=line.rstrip("\n")
            indV=line.split("\t")
            chrom=indV[0]
            scStart=indV[1]
            scEnd=indV[2]
            sc=indV[3] 
            scaffoldList[chrom].append([scStart,scEnd,sc])
        for read in readsFH:
            read=read.rstrip("\n")
            rd=read.split("\t")
            chrom=rd[0]
            rdStart=rd[1]
            rdEnd=rd[2]
            readList[chrom].append([rdStart,rdEnd,rd[3]])
        

        for chrKeys, scValues in sorted(scaffoldList.items()):
            for scValue in scValues:
                i=scValues.index(scValue)
                if(i<len(scValues)-1):
                    for reads in readList[chrKeys]:
                        if(int(scValue[1])-4>int(reads[0])) and (int(scValue[1])+4<int(reads[1])):
                            overFH.write("\t".join([chrKeys,reads[0],reads[1],scValue[2]+":"+scValue[0]+"-"+scValue[1]+"__"+scValues[i+1][2]+":"+scValues[i+1][0]+"-"+scValues[i+1][1]]))
                            overFH.write("\n")
                
                
                                                            
          

#####################################################################

def main():
    arguments = get_arguments()
    scaffolds = os.path.abspath(arguments.scaffolds)
    reads_file = os.path.abspath(arguments.reads)
    
    
    findOverlaps(scaffolds, reads_file)


#####################################################################
if __name__ == '__main__':
    main()
