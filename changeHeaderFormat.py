'''
Created on Jan 2, 2018

@author: nanda
'''
import argparse
import textwrap
import os
import gzip

#####################################################################


def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    put the less than 40 kb bin back in order
    python ~/aTools/utilities/putlessthan40kbBinsback.py -i combinedSelectedOrderWithclusterNumber-part2.txt -b listofBinsLessThan40kb -o added40kbBinsList
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_matrix_file' ,
                        help = "Input matrix file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-o" ,
                        metavar = 'output_matrix_file' ,
                        help = "output matrix file" ,
                        dest = "output",
                        required = True ,
                        type = str)
    

    
    return parser.parse_args()


#########################################################
def change(input_file,output_file):
    with gzip.open(input_file) as INFH, gzip.open(output_file, "w") as OUTFH:
        c=0
        offset=0
        for line in INFH:
            l=[]
            line=line.rstrip("\n")
            v=line.split("\t")
            if(c==0):
                for values in v:
                    if("__" in values):
                        s=values.split("__")
                        n=str(offset)+"|Symbiodinium_microadriaticum|"+s[0]+":"+s[1]+"-"+s[2]
                        l.append(n)
                        offset+=1
                    else:
                        l.append(values)
                OUTFH.write("\t".join(l))
                OUTFH.write("\n")
                offset=0
                c+=1
            else:
                s=v[0].split("__")
                n=str(offset)+"|Symbiodinium_microadriaticum|"+s[0]+":"+s[1]+"-"+s[2]
                v[0]=n
                OUTFH.write("\t".join(v))
                OUTFH.write("\n")
                offset+=1
            


#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    output_file = os.path.abspath(arguments.output)
    
    change(input_file,output_file)


#####################################################################
if __name__ == '__main__':
    main()