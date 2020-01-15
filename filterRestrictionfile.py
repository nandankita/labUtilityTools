'''
Created on Apr 19, 2017

@author: nanda
'''
import argparse
import textwrap
import os


#####################################################################


def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Remove the valid pairs which are not in the contig list
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_fragment_file' ,
                        help = "Input fragment file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    parser.add_argument("-c" ,
                        metavar = 'contig_list_file' ,
                        help = "contig list to be kept" ,
                        dest = "contig",
                        required = True ,
                        type = str)
    
    return parser.parse_args()

#####################################################################
def filterRes(input_file,contig_file):
    contigList=[]
    output_file="filteredRestrictionfile.txt"
    with open(input_file) as RESFH, open(contig_file) as CONTIGFH, open(output_file, "wt") as OUTFH:
        for c in CONTIGFH:
            cN = c.rstrip("\n")
            cS=cN.split(">")
            endNumber=cS.split("_")
            contigList.append(endNumber[-1])
        lenC=len(contigList)
        contigList=sorted(contigList)
        for res in RESFH:
            line=res.split("\t")
            n=line[0].split("_")
            fg1=binarySerch(contigList, n[-1],lenC-1,0)
            if(fg1):
                OUTFH.write(res)
   
#####################################################################

def binarySerch(resList, fragmentIndex,qq,firstIndex):
    found = False
    while firstIndex<=lastIndex and not found:
        midpoint=int((firstIndex+lastIndex)/2)
        if resList[midpoint] == fragmentIndex:
            found = True
        else:
            if fragmentIndex < resList[midpoint]:
                lastIndex = midpoint-1
            else:
                firstIndex = midpoint+1
    return found
    
#####################################################################    

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    contig_file = os.path.abspath(arguments.contig)
    
    
    filterRes(input_file,contig_file)


#####################################################################
if __name__ == '__main__':
    main()