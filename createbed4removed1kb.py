'''
Created on Jul 24, 2018

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
    Create a bed intermediate file by spliting the scaffold, bins and removed 1kb bins 
    python ~/aTools/utilities/createbed4removed1kb.py -i bedsingCorrectListHang4NMPos-40kb  -n unselectedIndexLocation1kb -o bed1kbremovedsingCorrectListHang4NMPos-40kb
    ''') )

    parser.add_argument("-i" ,
                        metavar = 'input_scaffold_bin_map file' ,
                        help = "input scaffold bin_map file" ,
                        dest = "input",
                        required = True ,
                        type = str)
    
    parser.add_argument("-n" ,
                        metavar = 'unselected 1kb bins list' ,
                        help = "unselected 1kb bins list" ,
                        dest = "unselect",
                        required = True ,
                        type = str)
    
    
    parser.add_argument("-o" ,
                        metavar = 'output_intermediate_bed file' ,
                        help = "output_intermediate_bed file" ,
                        dest = "output",
                        required = True ,
                        type = str)

    return parser.parse_args()

########################################################
class scaffold:
    def __init__(self,scf=None,chrm=None,st=0,en=0,strand=None):
        self.scf=scf
        self.chrm=chrm
        self.st=int(st)
        self.en=int(en)
        self.strand=strand


#########################################################
def findIndex(finalList,scaffold):
    c=0
    for i in finalList:
        n=i.split("\t")
        if(n[0]==scaffold):
            return c
        c+=1


#########################################################

def createList(input_file, unselect_file, output_file):
    scFileList=defaultdict(list)
    finalList=[]
    scList=defaultdict(list)
    with open(input_file) as inFH, open(unselect_file) as kbFile, open(output_file, "w") as outFH:
        for line in inFH:
            line=line.rstrip("\n")
            v=line.split("\t")
            c=v[1].split("__")
            p=scaffold(v[0],c[0],c[1],c[2],v[2])
            scFileList[c[0]].append(p)
            finalList.append(line)
#         for k,v in scFileList.items():
#             for s in v:
#                 print(k,s.scf,s.chrm,s.st,s.en,s.strand)
        #print(finalList)
        for f in kbFile:
            f=f.rstrip("\n")
            ch=f.split(":")
            loc=ch[1].split("-")
            start=int(loc[0])
            end=int(loc[1])
            chrom=ch[0]
            stScf=scaffold()
            enScf=scaffold()
            for s in scFileList[chrom]:
                if(s.st <= start <= s.en):
                    stScf=s
                if(s.st <= end <= s.en):
                    enScf=s
                if(stScf.scf==enScf.scf) and (stScf.scf != None):
                    a=s.scf.split("__")
                    if(s.strand=="plus"):
                        chSt1=s.st
                        chEnd1=start-1
                        chSt2=end+1
                        chEnd2=s.en
                        scSt1=int(a[1])
                        scEnd1=scSt1+chEnd1-chSt1
                        scEnd2=int(a[2])
                        scSt2=scEnd2-(chEnd2-chSt2)
                        if(scSt1 !=0) and (scEnd1 !=0):
                            #finalList.keys().index(s.scf)
                            scList[s.scf].append(a[0]+"__"+str(scSt1)+"__"+str(scEnd1)+"\t"+s.chrm+"__"+str(chSt1)+"__"+str(chEnd1)+"\t"+s.strand)
                            #outFH.write(a[0]+"__"+str(scSt1)+"__"+str(scEnd1)+"\t"+s.chrm+"__"+str(chSt1)+"__"+str(chEnd1)+"\t"+s.strand+"\n")
                        if(scSt2 !=0) and (scEnd2 !=0):
                            scList[s.scf].append(a[0]+"__"+str(scSt2)+"__"+str(scEnd2)+"\t"+s.chrm+"__"+str(chSt2)+"__"+str(chEnd2)+"\t"+s.strand)
                        break
# #                         print(s.scf,s.chrm,s.st,s.en,s.strand)
# #                         print(f)
# #                         print(chSt1,chEnd1,chSt2,chEnd2,scSt1,scEnd1,scSt2,scEnd2)
                    elif(s.strand=="minus"):
                        chSt1=s.st
                        chEnd1=start-1
                        chSt2=end+1
                        chEnd2=s.en
                        scSt1=int(a[1])
                        scEnd1=scSt1-(chEnd1-chSt1)
                        scEnd2=int(a[2])
                        scSt2=abs(scEnd2+(chEnd2-chSt2))
#                         print(s.scf,s.chrm,s.st,s.en,s.strand)
#                         print(f)
                        #print(chSt1,chEnd1,chSt2,chEnd2,scSt1,scEnd1,scSt2,scEnd2)
                        if(scSt1 !=0) and (scEnd1 !=0):
                            scList[s.scf].append(a[0]+"__"+str(scSt1)+"__"+str(scEnd1)+"\t"+s.chrm+"__"+str(chSt1)+"__"+str(chEnd1)+"\t"+s.strand)
                        if(scSt2 !=0) and (scEnd2 !=0):
                            scList[s.scf].append(a[0]+"__"+str(scSt2)+"__"+str(scEnd2)+"\t"+s.chrm+"__"+str(chSt2)+"__"+str(chEnd2)+"\t"+s.strand)
                        break
                    else:
                        print("NOne")
                        break
                elif(stScf.scf!=enScf.scf) and (stScf.scf != None) and (enScf.scf != None):
                    #print(f, stScf.scf, enScf.scf)
                    if (stScf.strand=="plus") and (enScf.strand=="plus"):
                        chSt1=stScf.st
                        chEnd1=start-1
                        chSt2=end+1
                        chEnd2=s.en
                        a=stScf.scf.split("__")
                        b=enScf.scf.split("__")
                        scSt1=int(a[1])
                        scEnd1=scSt1+chEnd1-chSt1
                        scEnd2=int(b[2])
                        scSt2=abs(scEnd2-(chEnd2-chSt2))
                        #print(chSt1,chEnd1,chSt2,chEnd2,stScf.scf,scSt1,scEnd1,enScf.scf,scSt2,scEnd2)
                        if(scSt1 !=0) and (scEnd1 !=0):
                            scList[stScf.scf].append(a[0]+"__"+str(scSt1)+"__"+str(scEnd1)+"\t"+s.chrm+"__"+str(chSt1)+"__"+str(chEnd1)+"\t"+stScf.strand)
                        if(scSt2 !=0) and (scEnd2 !=0):
                            scList[enScf.scf].append(b[0]+"__"+str(scSt2)+"__"+str(scEnd2)+"\t"+s.chrm+"__"+str(chSt2)+"__"+str(chEnd2)+"\t"+enScf.strand)
                        break
            
                    elif (stScf.strand=="minus") and (enScf.strand=="minus"):
                        chSt1=stScf.st
                        chEnd1=start-1
                        chSt2=end+1
                        chEnd2=s.en
                        a=stScf.scf.split("__")
                        b=enScf.scf.split("__")
                        scSt1=int(a[1])
                        scEnd1=scSt1-(chEnd1-chSt1)
                        scEnd2=int(b[2])
                        scSt2=abs(scEnd2+(chEnd2-chSt2))
                        #print(chSt1,chEnd1,chSt2,chEnd2,stScf.scf,scSt1,scEnd1,enScf.scf,scSt2,scEnd2)
                        if(scSt1 !=0) and (scEnd1 !=0):
                            scList[stScf.scf].append(a[0]+"__"+str(scSt1)+"__"+str(scEnd1)+"\t"+s.chrm+"__"+str(chSt1)+"__"+str(chEnd1)+"\t"+stScf.strand)
                        if(scSt2 !=0) and (scEnd2 !=0):
                            scList[enScf.scf].append(b[0]+"__"+str(scSt2)+"__"+str(scEnd2)+"\t"+s.chrm+"__"+str(chSt2)+"__"+str(chEnd2)+"\t"+enScf.strand)
                        
                        break
                    
                    elif (stScf.strand=="plus") and (enScf.strand=="minus"):
                        #print("Plus minus Cond", f)
                        chSt1=stScf.st
                        chEnd1=start-1
                        chSt2=end+1
                        chEnd2=s.en
                        a=stScf.scf.split("__")
                        b=enScf.scf.split("__")
                        scSt1=int(a[1])
                        scEnd1=scSt1+chEnd1-chSt1
                        scEnd2=int(b[2])
                        scSt2=abs(scEnd2+(chEnd2-chSt2))
                        #print(chSt1,chEnd1,chSt2,chEnd2,stScf.scf,scSt1,scEnd1,enScf.scf,scSt2,scEnd2)
                        if(scSt1 !=0) and (scEnd1 !=0):
                            scList[stScf.scf].append(a[0]+"__"+str(scSt1)+"__"+str(scEnd1)+"\t"+s.chrm+"__"+str(chSt1)+"__"+str(chEnd1)+"\t"+stScf.strand)
                            #print((a[0]+"__"+str(scSt1)+"__"+str(scEnd1)+"\t"+s.chrm+"__"+str(chSt1)+"__"+str(chEnd1)+"\t"+stScf.strand+"\n"))
                        if(scSt2 !=0) and (scEnd2 !=0):
                            scList[enScf.scf].append(b[0]+"__"+str(scSt2)+"__"+str(scEnd2)+"\t"+s.chrm+"__"+str(chSt2)+"__"+str(chEnd2)+"\t"+enScf.strand)
                            #print((b[0]+"__"+str(scSt2)+"__"+str(scEnd2)+"\t"+s.chrm+"__"+str(chSt2)+"__"+str(chEnd2)+"\t"+enScf.strand+"\n"))
                        
                        break
                    
                    elif (stScf.strand=="minus") and (enScf.strand=="plus"):
                        #print("minus plus Cond", f)
                        chSt1=stScf.st
                        chEnd1=start-1
                        chSt2=end+1
                        chEnd2=s.en
                        a=stScf.scf.split("__")
                        b=enScf.scf.split("__")
                        scSt1=int(a[1])
                        scEnd1=scSt1-(chEnd1-chSt1)
                        scEnd2=int(b[2])
                        scSt2=abs(scEnd2-(chEnd2-chSt2))
                        #print(chSt1,chEnd1,chSt2,chEnd2,stScf.scf,scSt1,scEnd1,enScf.scf,scSt2,scEnd2)
                        if(scSt1 !=0) and (scEnd1 !=0):
                            scList[stScf.scf].append(a[0]+"__"+str(scSt1)+"__"+str(scEnd1)+"\t"+s.chrm+"__"+str(chSt1)+"__"+str(chEnd1)+"\t"+stScf.strand)
                            #print((a[0]+"__"+str(scSt1)+"__"+str(scEnd1)+"\t"+s.chrm+"__"+str(chSt1)+"__"+str(chEnd1)+"\t"+stScf.strand+"\n"))
                        if(scSt2 !=0) and (scEnd2 !=0):
                            scList[enScf.scf].append(b[0]+"__"+str(scSt2)+"__"+str(scEnd2)+"\t"+s.chrm+"__"+str(chSt2)+"__"+str(chEnd2)+"\t"+enScf.strand)
                            #print((b[0]+"__"+str(scSt2)+"__"+str(scEnd2)+"\t"+s.chrm+"__"+str(chSt2)+"__"+str(chEnd2)+"\t"+enScf.strand+"\n"))
                        break
                    
        for k,v in scList.items():
            indx=findIndex(finalList,k)
            print(k,v)
            finalList[indx]='\n'.join(v)
            
        for i in finalList:
            outFH.write(i)
            outFH.write("\n")
        
            
            
            
#####################################################################

def main():
    arguments = get_arguments()
    input_file = os.path.abspath(arguments.input)
    unselect_file = os.path.abspath(arguments.unselect)
    output_file = os.path.abspath(arguments.output)

    createList(input_file, unselect_file, output_file)


#####################################################################
if __name__ == '__main__':
    main()
    