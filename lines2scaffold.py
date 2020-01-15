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
    change a line header name to corresponding scaffold name
    python ~/aTools/utilities/lines2scaffold.py -i /nl/umw_job_dekker/users/an27w/dinoflagellets/analysis/lines-manualAssembly-4/assembly/removedBins300headergt80kb -s h2 -o h4
    python ~/aTools/utilities/lines2scaffold.py -i /nl/umw_job_dekker/users/an27w/dinoflagellets/analysis/lines-manualAssembly-4/assembly/removedBins300headergt80kb 
    -s Karyotype_clusters_withNs.tab -o scaffoldh3
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_sc_list' ,
                        help = "input_sc_list" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-s" ,
                        metavar = 'lines header' ,
                        help = "lines header" ,
                        dest = "line",
                        required = True ,
                        type = str)
    
    parser.add_argument("-o" ,
                        metavar = 'output_line_scaffoldheader' ,
                        help = "output_line_scaffoldheader" ,
                        dest = "output",
                        required = True ,
                        type = str)
    

    
    return parser.parse_args()





#####################################################################

def change(input_file,line_file,output_file):
    keyDict=defaultdict(list)
    with open(input_file) as INP, open(line_file) as LI, open(output_file,"w") as OUT:
        scList=[]
        for line in INP:
            line=line.rstrip("\n")
            v=line.split(".")
            scList.append(v[1])
        for s in scList:
            a=s.split("__")
            aSt=int(a[1])
            aEnd=int(a[2])
            lSt=1
            lEnd=40000
            while(lEnd<=aEnd):
                k=a[0]+"__"+str(lSt)+"__"+str(lEnd)
                n=a[0][0:-1]+"__"+str(aSt)+"__"+str(aSt+39999)
                lSt+=40000
                lEnd+=40000
                aSt+=40000
                keyDict[k]=n
        for line in LI:
            line=line.rstrip("\n")
            c=line.split("\t")
            v=c[0].split("-")
            print(v)
            OUT.write("Lines.Smic."+keyDict[v[2]]+"\n")


       

#####################################################################
def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    line_file = os.path.abspath(arguments.line)
    output_file = os.path.abspath(arguments.output)
    
    change(input_file,line_file,output_file)


#####################################################################
if __name__ == '__main__':
    main()

