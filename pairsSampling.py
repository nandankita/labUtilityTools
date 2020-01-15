'''
Created on Aug 8, 2019

@author: nanda
'''
import sys
import numpy
import argparse
import textwrap
import os
import gzip
import random

#####################################################################

def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    sampling from pairs file, by removing lines from original
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_pairs-gz_file' ,
                        help = "Input pairs-gz file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    parser.add_argument("-n" ,
                        metavar = 'number of lines to be removed' ,
                        help = "number of lines to be removed" ,
                        dest = "lines",
                        required = True ,
                        type = str)
    

    return parser.parse_args()

#####################################################################
def sampling(input_file, linesNo):
    
    with gzip.open(input_file, "r") as pairsFH:
        c=0
        for lin in pairsFH:
            if not(lin.startswith('#')):
                c+=1
        print("Total lines ",c)
    
    linesToRemoveList=[]
    for x in range(linesNo):
        linesToRemoveList.append(random.randint(1,c))
    
    
    while(len(linesToRemoveList) != len(set(linesToRemoveList))):
        moreEntry=len(linesToRemoveList)-len(set(linesToRemoveList))
        linesToRemoveList=list(set(linesToRemoveList))
        for x in range(moreEntry):
            linesToRemoveList.append(random.randint(1,c))
            
    sampleLines=c-linesNo
    
    ouputFile=input_file.split(".gz")[0]+"_sampled_"+str(sampleLines)+".gz"
    with gzip.open(input_file, "r") as pairsFH, gzip.open(ouputFile, "w") as sampleFH:
        countLineNo=1
        for lin in pairsFH:
            if (not(lin.startswith('#'))) and (countLineNo not in linesToRemoveList):
                sampleFH.write(lin)
            if (not(lin.startswith('#'))):
                countLineNo+=1
    
         

#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    linesNo = int(arguments.lines)

    
    
    sampling(input_file, linesNo)


#####################################################################
if __name__ == '__main__':
    main()