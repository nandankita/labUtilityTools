'''
Created on Apr 16, 2019

@author: nanda

less merged.combined.min2.report | awk '{print $1"\t"$2"\t"$3"\t"$1":"$2"-"$3}' > tmp
 mv tmp merged.combined.min2.report 
python ~/aTools/utilities/findOverlapsWithDomains.py -i /nl/umw_job_dekker/users/an27w/sing-distiller/gapclosed/it6-results/gap-it6-manuallycorr-boundaries -r 10000 -n merged.combined.min2.report
python ~/aTools/utilities/findOverlapsWithDomains.py -i 10kbInsulation-filtered.bed -n merged.sorted.pacbio-chr94.bed -r 10000
less overlap_file | sort -k1,1 -k2,2 -k3,3 -V > tmp
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
    find out the overlapping reads given the domain boundaries 
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_domain_ boundary_file' ,
                        help = "Input domain boundary file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-n" ,
                        metavar = 'reads to find out the overlaps' ,
                        help = "reads to find out the overlaps" ,
                        dest = "reads",
                        required = True ,
                        type = str)
    
    parser.add_argument("-r" ,
                        metavar = 'domain_ boundary_file_resolution' ,
                        help = "domain_ boundary_file_resolution" ,
                        dest = "resolution",
                        required = True ,
                        type = str)
    

    return parser.parse_args()

#####################################################################
def findOverlaps(input_file, reads_file, resolution):
    bounadyList=defaultdict(list)
    readList=defaultdict(list)
    with open(input_file, "r") as lineFH, open(reads_file, "r") as readsFH, open("overlap_file", "w") as overFH:
        for line in lineFH:
            line=line.rstrip("\n")
            indV=line.split("\t")
            chrom=indV[0]
            bodStart=indV[1]
            bondEnd=indV[2] 
            bounadyList[chrom].append([bodStart,bondEnd])
        for read in readsFH:
            read=read.rstrip("\n")
            rd=read.split("\t")
            chrom=rd[0]
            rdStart=rd[1]
            rdEnd=rd[2]
            readList[chrom].append([rdStart,rdEnd,rd[3]])
        
#         print(readList["chr1"])
#         print("\n")
#         print(bounadyList["chr1"])
#   chromosome    boundarySt    boundaryEnd    readSt    readEnd
        
        for chrKeys,boundValues in sorted(bounadyList.items()):
            for boundValue in boundValues:
                for reads in readList[chrKeys]:
                    if(int(boundValue[0])-4>int(reads[0]) and int(boundValue[1])+4<int(reads[1])):
                        overFH.write("\t".join([chrKeys,boundValue[0],boundValue[1],reads[0],reads[1],reads[2]]))
                        overFH.write("\n")
            

#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    reads_file = os.path.abspath(arguments.reads)
    resolution = int(arguments.resolution)
    
    
    findOverlaps(input_file, reads_file, resolution)


#####################################################################
if __name__ == '__main__':
    main()
