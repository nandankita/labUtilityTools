'''
Created on Mar 8, 2018

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
    Given a cooler file create a begraph file of Cis only Hi-C interactions
    #python ~/aTools/utilities/createPairedEndfastq.py -f /nl/umw_job_dekker/users/an27w/dinoflagellets/nanopore -o nanopore_S10_L004
    ''') )
    
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-f" ,
                        help = "Input fastq folder" ,
                        dest = "folder")
    
    group.add_argument("-i" ,
                        help = "Input fastq file" ,
                        dest = "file")
    
    parser.add_argument("-o" ,
                        metavar = 'output_fastq_file' ,
                        help = "output fastq file" ,
                        dest = "out",
                        required = True ,
                        type = str)
    
    
    return parser.parse_args()

#####################################################################
def createpairedEnd(input_folder,input_file,output_file):
    file1=output_file+"_R1_000.fastq"
    file2=output_file+"_R2_000.fastq"
    with open(file1,"w") as outFastq1, open(file2, "w") as outFastq2:
        if(input_folder!=""):
            for filename in sorted(os.listdir(input_folder)):
                if filename.endswith(".fastq"):
                    input_file=os.path.join(input_folder, filename)
                    print(input_file)
                    with open(input_file, "r") as inFastq:
                        c=0
                        for line in inFastq:
                            c+=1
                            line=line.rstrip("\n\r")
                            if(c==2 or c==4):
                                outFastq1.write(line[0:100]+"\n")
                                outFastq2.write(line[len(line)-100:len(line)]+"\n")
                            else:
                                outFastq1.write(line+"\n")
                                outFastq2.write(line+"\n")
                            if(c==4):
                                c=0
        else:
            with gzip.open(input_file, "rt") as inFastq:
                c=0
                for line in inFastq:
                    c+=1
                    line=line.rstrip("\n\r")
                    if(c==2 or c==4):
                        outFastq1.write(line[0:100]+"\n")
                        outFastq2.write(line[len(line)-100:len(line)]+"\n")
                    else:
                        outFastq1.write(line+"\n")
                        outFastq2.write(line+"\n")
                    if(c==4):
                        c=0
                            
    print("done")


#####################################################################
def main():
    arguments = get_arguments()
    input_folder=""
    input_file =""
    if(arguments.folder):
        input_folder = os.path.abspath(arguments.folder)
    else:
        input_file = os.path.abspath(arguments.file)
    output_file = os.path.abspath(arguments.out)
    createpairedEnd(input_folder,input_file,output_file)
    

#####################################################################

if __name__ == '__main__':
    main()