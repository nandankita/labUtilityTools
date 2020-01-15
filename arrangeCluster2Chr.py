'''
Created on Jan 8, 2019

@author: nanda
'''
import argparse
import textwrap
import os
import gzip
from _collections import defaultdict
import operator

#####################################################################
def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Find to where to place a cluster bin within a chromosome
    Find most interacting bin in a chr
    python ~/aTools/utilities/getInteractingCluster.py -i selectedOrderWithLines.txt -m afterLineAssembRearranged.matrix -l 1
    
    python ~/aTools/utilities/arrangeCluster2Chr.py -m test.matrix 
    ''') )

    parser.add_argument("-m" ,
                        metavar = 'Matrix file' ,
                        help = "Matrix file" ,
                        dest = "matrix",
                        required = True ,
                        type = str)
 
    return parser.parse_args()

#####################################################################
def magicArrange(matrix_file):
    count = 0
    headerList=[]
    rearrangedList=[]
    headerRow = []
    clusterCount=0
    chrCount = 0
    with open(matrix_file, "r") as matrixFH, open("out-header", "w") as clusFH:
        for line in matrixFH:
            line=line.rstrip("\n")
            interactions=line.split("\t")
            Z=[]
            if(count==0):
                rearrangedList=range(len(interactions[1:]))
                for rowIndx in interactions[1:]:
                    row=rowIndx.split("|")[2]
                    headerRow.append(row)
                    if(row.startswith( 'cluster' )):
                        clusterCount+=1
                    else:
                        chrCount+=1
            else:
                
                headerColumn=interactions[0].split("|")[2]
                headerList.append(headerColumn)
                del interactions[0]
                
                for i in rearrangedList:
                    Z.append(interactions[i])
                    
                if(headerColumn.startswith( 'cluster' )):
                    index, rowMost = max(enumerate([float(i) for i in Z[0:chrCount]]), key=operator.itemgetter(1))
                    rearrangedList.insert(index,rearrangedList[count-1])
                    del rearrangedList[count]
                    chrCount+=1
                    
            count+=1
        
        for i in rearrangedList:
            clusFH.write(headerRow[i]+"\n")
            

            
#####################################################################

def main():
    arguments = get_arguments()
    matrix_file = os.path.abspath(arguments.matrix)

    magicArrange(matrix_file)


#####################################################################
if __name__ == '__main__':
    main()