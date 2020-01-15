'''
Created on May 18, 2017

@author: nanda
'''
import argparse
import textwrap
import os
import gzip
from _collections import defaultdict

#####################################################################



def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    extract each row trans interactions
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_tab_matrix_file' ,
                        help = "Input tab matrix file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-f" ,
                        metavar = 'cluster file' ,
                        help = "Input cluster file" ,
                        dest = "cluster",
                        required = True ,
                        type = str)

    return parser.parse_args()

#####################################################################
def extractTransInteractions(input_file, cluster_file):
    clustHeaders=defaultdict(list)
    clustNumbers=dict()
    count = 0
    with open(input_file, "r") as MATRIXFH, open(cluster_file, "r") as clusFH, open("cisRemoved.matrix", "w") as removedMatrixFH:
        for c in clusFH:
            c=c.rstrip("\n")
            sC = c.split("\t")
            key=sC[3]
            value="__".join(sC[0:3])
            clustHeaders[key].append(value)
            clustNumbers[value]=key
        i=1
        headerindices=dict()
        for line in MATRIXFH:
            line=line.rstrip("\n")
            line=line.rstrip()
            if(count == 0):
                header=line.split("\t")
                ind=0
                for he in header:
                    headerindices[he]=ind
                    ind+=1
                count+=1
            else:
                interactions=line.split("\t")
                rowCluster=clustNumbers[header[i]]
                j=1
                appendSumRow = []
                appendColClus = []
                while(j<len(header)):
                    columnCluster=clustNumbers[header[j]]
                    headersInSameCluster=clustHeaders[columnCluster]
                    noOfColumns=len(headersInSameCluster)
                    hIndexSum = []
                    for h in headersInSameCluster:
                        indexH=headerindices[h]
                        hIndexSum.append(float(interactions[indexH]))
                    sumRow=str(sum(hIndexSum)/noOfColumns)
                    if(rowCluster==columnCluster):
                        sumRow=str(0.0)
                    j+=len(headersInSameCluster)
                    appendSumRow.append(sumRow)
                    if(count == 1):
                        appendColClus.append(columnCluster)
                i+=1
                if(count == 1):
                    appendColClus.insert(0, "18468x"+str(len(appendColClus)))
                    removedMatrixFH.write("\t".join(appendColClus))
                    removedMatrixFH.write("\n")
                    count+=1
                appendSumRow.insert(0, interactions[0])
                removedMatrixFH.write("\t".join(appendSumRow))
                removedMatrixFH.write("\n")
                
   


#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    cluster_file = os.path.abspath(arguments.cluster)
    
    extractTransInteractions(input_file, cluster_file)


#####################################################################
if __name__ == '__main__':
    main()
    