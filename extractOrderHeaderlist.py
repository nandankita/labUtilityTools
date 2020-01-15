'''
Created on May 4, 2017

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
    extract the order of header given an unordered list
    file A has input as orderedFile header B is unordered, Arrange B as given order in A
    
    ''') )

    parser.add_argument("-u" ,
                        metavar = 'input_unordered_file' ,
                        help = "Input unordered file" ,
                        dest = "unordered",
                        required = True ,
                        type = str)
    
    parser.add_argument("-l" ,
                        metavar = 'input_ordered_file' ,
                        help = "Input ordered file" ,
                        dest = "ordered",
                        required = True ,
                        type = str)
    
    
    return parser.parse_args()

#####################################################################
def arrangeList(unordered_file,ordered_file):
    with open (unordered_file, "r") as UnFH, open (ordered_file, "r") as oFH,open ("OrderedHeaderList", "w") as OutFH:
        unList = []
        for unLine in UnFH:
            unLine=unLine.rstrip("\n")
            unList.append(unLine)
        for oLine in oFH:
            oLine= oLine.rstrip("\n")
            if(oLine in unList):
                OutFH.write(oLine)
                OutFH.write("\n")
    

#####################################################################


def main():
    arguments = get_arguments()
    unordered_file = os.path.abspath(arguments.unordered)
    ordered_file = os.path.abspath(arguments.ordered)

    arrangeList(unordered_file,ordered_file)
    

#####################################################################

if __name__ == '__main__':
    main()
