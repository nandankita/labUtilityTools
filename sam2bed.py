'''
Created on Apr 12, 2017

@author: nanda
'''

import argparse
import textwrap
import os
import pysam
import re
from _collections import defaultdict

#####################################################################
def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Read Sam file and give a bed file with sequences which are multimapped
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_sam_file' ,
                        help = "Input sam file" ,
                        dest = "input",
                        required = True ,
                        type = str)

    return parser.parse_args()

#####################################################################

def processSam(input_file):
    samInFH = pysam.AlignmentFile(input_file)
    bedFileFH = open("borisMultimapped.bed","w")
    listMapped = []
    for r in samInFH.fetch(until_eof=True):
        if (not(r.is_unmapped)):
            listMapped.append(r.query_name)
    samInFH.close()
    listMultiMapped,listUniqueMapped = countMulti(listMapped)
    multimappedPos=[x.split(":")[1] for x in listMultiMapped]
    multimappedPos=sorted(multimappedPos, key=lambda x:x.split("-")[0], reverse=False)
    lstPos=0
    regionSt=0
    regionEnd=0
    newList=[]
    multimappedPos.append("0-0")
    for i in multimappedPos:
        pos=i.split("-")
        if(lstPos+1==int(pos[0])):
            regionEnd=int(pos[1])
        else:
            newList.append(str(regionSt)+"-"+str(regionEnd))
            regionSt=int(pos[0])
            regionEnd=int(pos[1])
        lstPos=int(pos[1])
    del newList[0]
    bedFileFH.write("browser position chr20:56087636-56099306\ntrack name=\"BorisMultimappedRegions\" itemRgb=\"On\"\n")
    for r in newList:
        p=r.split("-")
        bedFileFH.write("chr20\t"+str(p[0])+"\t"+str(p[1])+"\n")
    print("Done Bed File")



#####################################################################
def countMulti(L):
    seen = set()
    seen2 = set()
    seen_add = seen.add
    seen2_add = seen2.add
    for item in L:
        if item in seen:
            seen2_add(item)
        else:
            seen_add(item)
    unique = seen - seen2
    return list(seen2),list(unique)



#####################################################################


def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    processSam(input_file)          

#####################################################################
if __name__ == '__main__':
    main()

    
    