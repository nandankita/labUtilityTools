'''
Created on Jul 17, 2018

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
    Remove the lines from unselected Index and create new matrix without those lines.
    1 based index file
    python ~/aTools/utilities/extractMatrixRemoveBins.py  -i teset23.matrix -s testIndex
    
    python ~/aTools/utilities/extractMatrixRemoveBins.py  -i Dino-HiC-Dplus_chr7_1000_dino_iced.matrix.gz -s unselectedIndexchr7 -c 7
    
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_scaffold_file' ,
                        help = "input_scaffold_file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-s" ,
                        metavar = 'unselected 1 kb index file' ,
                        help = "unselected_1kb_index_file" ,
                        dest = "order",
                        required = True ,
                        type = str)
    
    return parser.parse_args()

#####################################################################
def mapBins(input_file,unselected_order):
    scMap = defaultdict(dict)
    with open(input_file) as SCIN, open(unselected_order) as ORD, open("scaffoldMap1kbBins","w") as scMapFH:
        for line in SCIN:
            line=line.rstrip("\n")
            val=line.split("\t")
            ch=val[3].split(":")
            scMap[ch[0]][val[0]]=ch[1]
        for line in ORD:
            line=line.rstrip("\n")
            val=line.split(":")
            loc=val[1].split("-")
            chrm=val[0]
            st=int(loc[0])
            end=int(loc[1])
            for k,v in scMap[chrm].items():
                bin4okb=v.split("-")
                if(int(bin4okb[0]) <= st <=int(bin4okb[1])):
                    stV=k
                if(int(bin4okb[0]) <= end <=int(bin4okb[1])):
                    enV=k
            if(stV==enV):
                scMapFH.write(line+"\t"+stV+"\n")
            else:
                scMapFH.write(line+"\t"+stV+"\t"+enV+"\n")

    
#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    unselected_order = os.path.abspath(arguments.order)
    
    mapBins(input_file,unselected_order)


#####################################################################
if __name__ == '__main__':
    main()
