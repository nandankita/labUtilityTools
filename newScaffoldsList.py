'''
Created on Jun 20, 2017

@author: nanda
'''
import argparse
import textwrap
import os
import gzip
from Bio import SeqIO
from _collections import defaultdict

#####################################################################
def get_arguments():
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
    '''
    Make a new scaffold list based on removed bins. 
    python ~/aTools/utilities/newScaffoldsList.py -i totalMissingBinsth300lt40kbsorted -o mergedtotalMissingBinsth300lt40kb
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_scaffold_file' ,
                        help = "input scaffold file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-o" ,
                        metavar = 'output_scaffold_file' ,
                        help = "output scaffold file" ,
                        dest = "output",
                        required = True ,
                        type = str)

    return parser.parse_args()

#####################################################################
def createList(input_file, output_file):
    with open(input_file) as inFH, open(output_file, "w") as outFH:
        scfDict=defaultdict(list)
        for line in inFH:
            line=line.rstrip("\n")
            line=line.rstrip()
            iValues=line.split("__")
            scfDict[iValues[0]].append([iValues[1],iValues[2]])
        newscfDict=defaultdict(list)
        for k,v in scfDict.items():
            alp='a'
            vals=sorted(v, key=lambda x: int(x[0]))
            lstPos=0
            regionSt=0
            regionEnd=0
            newList=[]
            vals.append(['0','0'])
            for i in vals:
                if(lstPos+1==int(i[0])):
                    regionEnd=int(i[1])
                else:
                    newList.append(str(regionSt)+"-"+str(regionEnd))
                    regionSt=int(i[0])
                    regionEnd=int(i[1])
                lstPos=int(i[1])
            if(newList[0]=='0-0'):
                del newList[0]
            newscfDict[k].append(newList)
        keylist = newscfDict.keys()
        s=sorted(keylist)
        for key in s:
            val=newscfDict[key]
            #alp="a"
            for i in val:
                for a in i:
                    outFH.write(key+"\t"+a+"\n")
                    #outFH.write(key+alp+"\t"+a+"\n")
                    #alp=chr(ord(alp) + 1)
            
#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    output_file = os.path.abspath(arguments.output)

    createList(input_file, output_file)


#####################################################################
if __name__ == '__main__':
    main()
    