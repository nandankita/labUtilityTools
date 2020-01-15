'''
Created on Apr 13, 2017

@author: nanda
'''
import argparse
import textwrap
import os
import gzip

#####################################################################


def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Remove the valid pairs which are not in the contig list
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_gz_validpairitx_file' ,
                        help = "Input gzipped tab file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-o" ,
                        metavar = 'output_gz_validpairitx_file' ,
                        help = "output gzipped tab file" ,
                        dest = "output",
                        required = True ,
                        type = str)
    
    parser.add_argument("-r" ,
                        metavar = 'input_restriction_file' ,
                        help = "input restriction file" ,
                        dest = "restriction",
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
def filteritx(input_file,output_file,contig_file,res_file):
    contigList=[]
    resList=[]
    with gzip.open(input_file, "rt") as PAIRFH, open(res_file) as RESFH, open(contig_file) as CONTIGFH, gzip.open(output_file, "wt") as OUTFH:
        for c in CONTIGFH:
            cN = c.rstrip("\n")
            cS=cN.split(">")
            contigList.append(cS[1])
        for r in RESFH:
            rN = r.rstrip("\n")
            rS = rN.split("\t")
            if(rS[0] in contigList):
                resList.append(rS[4])
        lengRes=len(resList)
        for pair in PAIRFH:
            line=pair.split("\t")
            fg1=binarySerch(resList, line[0],lengRes-1,0)
            fg2=binarySerch(resList, line[1],lengRes-1,0)
            if(fg1 and fg2):
                OUTFH.write(pair)


   
#####################################################################
def binarySerch(resList, fragmentIndex,lastIndex,firstIndex):
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
    output_file = os.path.abspath(arguments.output)
    contig_file = os.path.abspath(arguments.contig)
    res_file = os.path.abspath(arguments.restriction)
    
    filteritx(input_file,output_file,contig_file,res_file)


#####################################################################
if __name__ == '__main__':
    main()