'''
Created on May 10, 2017

@author: nanda
'''

import argparse
import textwrap
import os
import gzip
from _collections import defaultdict

#####################################################################
# python ~/aTools/utilities/extractCisInteractions.py -i Rearranged_ExpandedSubscaffold_Dino-HiC-D7plus-Comb8__Symbiodinium_microadriaticum__genome__C-40000-iced.matrix 
# -o rearranged_cluster7.matrix -f correctRearrangedbinsCluster -n 7
###

def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    extract cis interactions in a given matrix
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_tab_matrix_file' ,
                        help = "Input tab matrix file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    parser.add_argument("-o" ,
                        metavar = 'output_matrix_file' ,
                        help = "Output tab matrix file" ,
                        dest = "output",
                        required = True ,
                        type = str)
    parser.add_argument("-f" ,
                        metavar = 'cluster file' ,
                        help = "Input cluster file" ,
                        dest = "cluster",
                        required = True ,
                        type = str)
    parser.add_argument("-n" ,
                        metavar = 'cluster number' ,
                        help = "cluster number to be extracted" ,
                        dest = "number",
                        required = True ,
                        type = str)

    return parser.parse_args()

#####################################################################
def extractCisInteractions(input_file, output_file, cluster_file, number):
    clustHeaders=defaultdict(list)
    clustNumbers=dict()
    count = 0
    with open(input_file, "r") as MATRIXFH, open(cluster_file, "r") as clusFH, open(output_file, "w") as removedMatrixFH:
        for c in clusFH:
            c=c.rstrip("\n")
            sC = c.split("\t")
            cNum=sC[1]
            binName=sC[0]
            clustHeaders[cNum].append(binName)
            clustNumbers[binName]=cNum
        i=1
        
        for line in MATRIXFH:
            line=line.rstrip("\n")
            line=line.rstrip()
            if(count == 0):
                header=line.split("\t")
                header_cluster="\t".join(clustHeaders[number])
                l=len(clustHeaders[number])
                header_cluster=str(l)+"x"+str(l)+"\t"+header_cluster
                print(len(clustHeaders[number]))
                removedMatrixFH.write(header_cluster)
                removedMatrixFH.write("\n")
                count+=1
            else:
                interactions=line.split("\t")
                cisInteractions=[]
                if ((header[i]) in clustNumbers):
                    rowCluster=clustNumbers[header[i]]
                    if(rowCluster==number):
                        #j=1
                        for j in range(1,len(header)):
                            if ((header[j]) in clustNumbers):
                                columnCluster=clustNumbers[header[j]]
                                if(rowCluster==columnCluster):
                                    cisInteractions.append(interactions[j])
                            #j+=1
                        rowHeading=interactions[0]
                        cisInteractions.insert(0, rowHeading)
                        removedMatrixFH.write("\t".join(cisInteractions))
                        removedMatrixFH.write("\n")
                i+=1
                
   
#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    output_file = os.path.abspath(arguments.output)
    cluster_file = os.path.abspath(arguments.cluster)
    number = arguments.number
    extractCisInteractions(input_file, output_file, cluster_file, number)


#####################################################################
if __name__ == '__main__':
    main()
    