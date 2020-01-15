'''
Created on Aug 11, 2018

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
    check that output lines are at 1kb 
    python ~/aTools/utilities/check1kbFileOutput.py -i testFinal
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_selected_order_file' ,
                        help = "Input order file" ,
                        dest = "input",
                        required = True ,
                        type = str)

    
    return parser.parse_args()


# #########################################################
# def check1kb(input_file):
#     checkLines = defaultdict(list)
#     with open(input_file) as inFH:
#         for line in inFH:
#             totalCount=0
#             line=line.rstrip("\n")
#             scaffoldBlock=line.split(",")
#             for i in scaffoldBlock:
#                 values=i.split("\t")
#                 scaffoldLoc=values[0].split("__")
#                 totalCount+=int(scaffoldLoc[2])-int(scaffoldLoc[1])+1
#             if (totalCount != 1000):
#                 v=scaffoldBlock[0].split("\t")
#                 print(v)
#                # checkLines[v[1]].append(line)
#             
#         #print(checkLines)
# #         for k,v in checkLines.items():
# #             print(k,v)
# #             if (len(v)>1):
# #                 print(v)
#         
#         print("File Processed")

#########################################################
def check1kb(input_file):
    with open(input_file) as inFH:
        lastCluster='0'
        totalCount=0
        for line in inFH:
            line=line.rstrip("\n")
            scaffoldBlock=line.split(",")
            scB=scaffoldBlock[0].split("\t")
            if(lastCluster!=scB[1]):
                print(lastCluster,totalCount)
                totalCount=0
            
            for i in scaffoldBlock:
                values=i.split("\t")
                scaffoldLoc=values[0].split("__")
                totalCount+=int(scaffoldLoc[2])-int(scaffoldLoc[1])+1
                
                
            lastCluster=scB[1]
#             if (totalCount != 1000):
#                 v=scaffoldBlock[0].split("\t")
#                 print(v)
               # checkLines[v[1]].append(line)
            
        #print(checkLines)
#         for k,v in checkLines.items():
#             print(k,v)
#             if (len(v)>1):
#                 print(v)
        
        print("File Processed")


#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    
    check1kb(input_file)


#####################################################################
if __name__ == '__main__':
    main()
