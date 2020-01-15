'''
Created on Apr 11, 2018

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
    It will add remaining scaffolds to the fasta file
    python ~/aTools/utilities/pacbio-reads-mapping.py -i gap0-mapping-mappedReads-sorted -j gapPenalty-mapping-mappedReads-sorted -o merge-pacbio-out
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_pacbio_mapping1' ,
                        help = "Input pacbio mapping1" ,
                        dest = "map1",
                        required = True ,
                        type = str)
    
    parser.add_argument("-j" ,
                        metavar = 'input_pacbio_mapping2' ,
                        help = "Input pacbio mapping2" ,
                        dest = "map2",
                        required = True ,
                        type = str)
    
    parser.add_argument("-o" ,
                        metavar = 'output file' ,
                        help = "output file" ,
                        dest = "out",
                        required = True ,
                        type = str)
    
    
    return parser.parse_args()

#####################################################################
def mergeF(map1,map2,output_file):
    gap0 = defaultdict(list)
    gapP = defaultdict(list)
    with open(map1, "r") as map1FH, open(map2, "r") as map2FH, open(output_file, "w") as outFH:
        for line in map1FH:
            line = line.rstrip("\n")
            v=line.split(" ")
            gap0[v[0]]= (v[1]+" "+v[2]+" "+v[3]+" "+v[4]+" "+v[5])
        for line in map2FH:
            line = line.rstrip("\n")
            v=line.split(" ")
            gapP[v[0]]= (v[1]+" "+v[2]+" "+v[3]+" "+v[4]+" "+v[5])
        for keys, value in gap0.items():
            if keys in gapP:
                outFH.write(keys+"\t"+value+"\t"+gapP[keys]+"\n")
            else:
                print(keys)




#####################################################################


def main():
    arguments = get_arguments()
    map1 = os.path.abspath(arguments.map1)
    map2 = os.path.abspath(arguments.map2)
    output_file= os.path.abspath(arguments.out)
    mergeF(map1,map2,output_file)
    

#####################################################################

if __name__ == '__main__':
    main()