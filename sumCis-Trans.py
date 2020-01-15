'''
Created on June 4, 2017

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
    remove the cis interactions in a given matrix
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
def removeCisInteractions(input_file, cluster_file):
    clustHeaders=defaultdict(list)
    clustNumbers=dict()
    count = 0
    with open(input_file, "r") as MATRIXFH, open(cluster_file, "r") as clusFH, open("cis-TransSum", "w") as removedMatrixFH:
        for c in clusFH:
            c=c.rstrip("\n")
            sC = c.split("\t")
            key=sC[3]
            value="__".join(sC[0:3])
            clustHeaders[key].append(value)
            clustNumbers[value]=key
        i=1
        for line in MATRIXFH:
            transSum=[]
            cisSum=[]
            line=line.rstrip("\n")
            line=line.rstrip()
            if(count == 0):
#                 header=line.split("\t")
#                 removedMatrixFH.write(line)
#                 removedMatrixFH.write("\n")
                count+=1
            else:
                interactions=line.split("\t")
                rowCluster=clustNumbers[header[i]]
                j=1
                for j in range(1,len(header)):
                    columnCluster=clustNumbers[header[j]]
                    #print(j, header[j])
                    if(rowCluster==columnCluster):
                        cisSum.append(float(interactions[j]))
                    else:
                        transSum.append(float(interactions[j]))
                    j+=1
                i+=1
                a=str(sum(cisSum))
                b=str(sum(transSum))
                removedMatrixFH.write(a+"\t"+b)
                removedMatrixFH.write("\n")
                
   
#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    cluster_file = os.path.abspath(arguments.cluster)
    
    removeCisInteractions(input_file, cluster_file)


#####################################################################
if __name__ == '__main__':
    main()
    