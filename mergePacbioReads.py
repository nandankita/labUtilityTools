'''
Created on Oct 29, 2018

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
    Merge Pacbio reads which overlaps into one. Neglect the score now.
    python3 ~/aTools/utilities/
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_pacbio_bed' ,
                        help = "Input pacbio bed file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-o" ,
                        metavar = 'output_pacbio_bed' ,
                        help = "output_pacbio_bed_file." ,
                        dest = "output",
                        required = True ,
                        type = str)
    
    
    return parser.parse_args()
#####################################################################

def inRange(last,v):
    if(last[0]==v[0]):
        if(((v[1]<=last[1]<=v[2]) or (last[1]<=v[1]<=last[2])) and ((v[1]<=last[2]<=v[2]) or (last[1]<=v[2]<=last[2]))):
            smallest=min(v[1],last[1])
            largest=max(v[2],last[2])
        else:
            pass
        


#####################################################################
def merge(input_file,output_file):
    with open(input_file) as inFH, open(output_file, "w") as outFH:
        last=""
        c=0
        for line in inFH:
            line=line.rstrip("\n")
            v=line.split("\t")
            if(c==0):
                last=v
            else:
                f=inRange(last,v)
            c+=1
            last=v
            
            

#####################################################################


def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    output_file = os.path.abspath(arguments.output)
    merge(input_file,output_file)
    

#####################################################################

if __name__ == '__main__':
    main()