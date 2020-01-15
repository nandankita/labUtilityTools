'''
Created on Dec 6, 2017

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
    change a matrix header from chr to scaffold given a list of corresponding sc list and rearranged_cluster--.matrix 
    python ~/aTools/utilities/changeheader2scaffold.py -i rearranged_cluster66.matrix -s scfOrder66 -o rearranged_cluster66.matrix2
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_matrix' ,
                        help = "input_matrix" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-s" ,
                        metavar = 'scaffold order' ,
                        help = "scaffold order" ,
                        dest = "sc",
                        required = True ,
                        type = str)
    
    parser.add_argument("-o" ,
                        metavar = 'output_matrix' ,
                        help = "output matrix" ,
                        dest = "output",
                        required = True ,
                        type = str)
    

    
    return parser.parse_args()





#####################################################################

def change(input_file,sc_file,output_file):
    with open(input_file) as INP, open(sc_file) as SC, open(output_file,"w") as OUT:
        scList=[]
        for line in SC:
            line=line.rstrip("\n")
            scList.append(line)
        scList = [w.replace('-', '_') for w in scList]
        c=0
        for b in INP:
            b=b.rstrip("\n")
            if(c==0):
                lng=len(scList)
                scList.insert(0,(str(lng)+"x"+str(lng)))
                fl="\t".join(scList)
                OUT.write(fl+"\n")
                c+=1
            else:
                v=b.split("\t")
                del(v[0])
                v.insert(0,scList[c])
                nl="\t".join(v)
                OUT.write(nl+"\n")
                c+=1

       

#####################################################################
def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    sc_file = os.path.abspath(arguments.sc)
    output_file = os.path.abspath(arguments.output)
    
    change(input_file,sc_file,output_file)


#####################################################################
if __name__ == '__main__':
    main()

