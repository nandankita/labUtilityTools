'''
Created on Feb 21, 2017

@author: nanda
'''

import argparse
import textwrap
import os
import glob
from _collections import defaultdict, OrderedDict


#####################################################################


def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Check assembly with pacbio reads
    ''') )

    parser.add_argument("-p" ,
                        metavar = 'input_pacbio_report_file' ,
                        help = "Input Pacbio Report file" ,
                        dest = "pacbio",
                        required = True ,
                        type = str)
    
    parser.add_argument("-c" ,
                        metavar = 'input_cluster_folder' ,
                        help = "Input cluster folder" ,
                        dest = "cluster",
                        required = True ,
                        type = str)
    
    
    parser.add_argument("-o" ,
                        metavar = 'output_report_file' ,
                        help = "Output report file" ,
                        dest = "output",
                        required = False,
                        default = "matchReport.txt",
                        type = str)

    return parser.parse_args()

#####################################################################

def matchReads(input_pacbio,input_cluster,output_file):
    readsDict = defaultdict(list)
    clustersDict = defaultdict(list)
    with open(input_pacbio, "r") as pacbioIn:
        for line in pacbioIn:
            r = line.split(",")
            readsDict[r[0]].append(r[1])
            
    for name in glob.glob(input_cluster+"/cluster_*_*_order"):
        clusterNumber=name.split("_")
        with open(name, "r") as assemblyIn:
            for clstBin in assemblyIn:
                c=clstBin.rstrip('\n')
                clustersDict[clusterNumber[4]].append(c)
    
    with open(output_file,"w") as RepOUT:
        for readK, readV in readsDict.items():
            for clusK, clusV in clustersDict.items():
#                 if(all(x in clusV for x in readV)):
#                     RepOUT.write(readK+" maps to cluster "+clusK +" "+str(readV)+"\n")
                intersect=set(clusV).intersection(readV)
                if(len(intersect)>1):
                    RepOUT.write(readK+" maps to cluster "+clusK +" "+str(intersect)+"\n")
#             for contig in readV:
#                 if(contig in clusV):
#                     mappingDict[clusK].append("R"+str(count))
#         count+=1
    
#     print(len(readsDict))
    print("Done")



#####################################################################

def main():
    arguments = get_arguments()
    input_pacbio = os.path.abspath(arguments.pacbio)
    input_cluster = os.path.abspath(arguments.cluster)
    output_file = os.path.abspath(arguments.output)
    
    matchReads(input_pacbio,input_cluster,output_file)


#####################################################################
if __name__ == '__main__':
    main()
