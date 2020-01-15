'''
Created on Oct 10, 2019

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
    Given a scaffold list considering cluster number, strand and continuity.
    python3 ~/aTools/utilities/mergeSubScaffolds.py -i 1based.Smic1.0.sub-scaffoldList -o merged-1based.Smic1.0.sub-scaffoldList 
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_sub_scaffold_file' ,
                        help = "Input sub scaffold file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-o" ,
                        metavar = 'output_sub_scaffold_file.' ,
                        help = "output_sub_scaffold_file." ,
                        dest = "output",
                        required = True ,
                        type = str)
    
    
    return parser.parse_args()

#####################################################################
def merge(input_file,output_file):
    curSc="Smic.scaffold675"
    curLine=["chr1","1","113000","Smic.scaffold675__40001__153000","+"]
    lastLn =""
    with open(input_file) as inFH, open(output_file, "w") as outFH:
        for line in inFH:
            line=line.rstrip("\n")
            v=line.split("\t")
            lineSc=v[3].split("__")[0]
            if(lineSc != curSc):
                wr="\t".join([curLine[0],curLine[1],lastLn[2],curSc])
                curLine=v
                curSc=lineSc
                outFH.write(wr+"\n")
            lastLn=v   
                
            

#####################################################################


def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    output_file = os.path.abspath(arguments.output)
    merge(input_file,output_file)
    

#####################################################################

if __name__ == '__main__':
    main()