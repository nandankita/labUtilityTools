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
    put bins back which are filtered during Noam's assembly of Ns.
    python ~/aTools/utilities/putbackNoamFilteredBinsNs.py -i Karyotype_lines -b headerFileteredNoam -o rearrangedHeader
    python ~/aTools/utilities/putbackNoamFilteredBinsNs.py -i r1 -b headerFileteredNoam -o Karyotype_clusters_withNs.tab
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_selected_order_file' ,
                        help = "Input order file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-b" ,
                        metavar = 'filtered_bins' ,
                        help = "filtered bins" ,
                        dest = "bins",
                        required = True ,
                        type = str)
    
    parser.add_argument("-o" ,
                        metavar = 'output_file' ,
                        help = "output file" ,
                        dest = "output",
                        required = True ,
                        type = str)
    

    
    return parser.parse_args()





#####################################################################

def putback(input_file,bins_file,output_file):
    inputD=defaultdict(list)
    with open(input_file) as INP, open(bins_file) as BIN, open(output_file,"w") as OUT:
        oneList=[]
        inputList=[]
        for line in INP:
            line=line.rstrip("\n")
            val=line.split("\t")
            inputList.append(val[0])
            inputD[val[0]]=val[1]
        for b in BIN:
            b=b.rstrip("\n")
            v=b.split("__")
            if(int(v[1]) != 1):
                vPrev=v[0]+"__"+str(int(v[1])-40000)+"__"+str(int(v[1])-1)
                if(vPrev in inputList):
                    ind=inputList.index(vPrev)+1
                    inputD[b]=inputD[vPrev]
                else:
                    vNext=v[0]+"__"+str(int(v[2])+1)+"__"+str(int(v[2])+40000)
                    ind=inputList.index(vNext)
                    inputD[b]=inputD[vNext]
                inputList.insert(ind,b)
            else:
                oneList.append(b)
        for o in oneList:
            v=o.split("__")
            vNext=v[0]+"__"+str(int(v[2])+1)+"__"+str(int(v[2])+40000)
            ind=(inputList.index(vNext))
            inputD[o]=inputD[vNext]
            inputList.insert(ind,o)
        for n in inputList:
            OUT.write(n+"\t"+str(inputD[n])+"\n")
       

#####################################################################
def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    bins_file = os.path.abspath(arguments.bins)
    output_file = os.path.abspath(arguments.output)
    
    putback(input_file,bins_file,output_file)


#####################################################################
if __name__ == '__main__':
    main()

