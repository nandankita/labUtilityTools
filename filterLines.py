'''
Created on May 29, 2017

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
    extract each row trans interactions
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_tab_matrix_file' ,
                        help = "Input tab matrix file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    

    return parser.parse_args()

#####################################################################
def filterLines(input_file):
    count = 0
    with open(input_file, "r") as MATRIXFH, open("filteredIndices1", "w") as filterFH:
        hSet = set()
        for line in MATRIXFH:
            line=line.rstrip("\n")
            line=line.rstrip()
            if(count == 0):
                count+=1
            else:
                interactions=line.split("\t")
                rowname=interactions[0]
                del interactions[0]
                for i in interactions:
                    roundV=round_up(i,2)
                    #print(i,roundV)
                    if(roundV>=8):
                        print(rowname)
                        if(rowname not in hSet):
                            hSet.add(rowname)
                            #filterFH.write(rowname+"\t"+str(count))
                            #filterFH.write("\n")
                count+=1
            


#####################################################################               

def round_up(x, base):
    return int(base * round(float(x)/base))

#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    
    filterLines(input_file)


#####################################################################
if __name__ == '__main__':
    main()
    
    