'''
Created on Dec 26, 2019

@author: nanda
python ~/aTools/utilities/sam2clippedReport.py mD7.subreads.sam 
'''
import sys
import os
import pysam


filenameSam=os.path.abspath(sys.argv[1])
outfilenameRep=(sys.argv[1].split(".sam")[0])+".clipped.report"


with open(filenameSam, "r") as lineFH, open(outfilenameRep, "w") as outFH:
    samInFH = pysam.AlignmentFile(filenameSam)
    for r in samInFH.fetch(until_eof=True):
        #position = r.get_reference_positions()
        #print(r.query_name,r.reference_start,r.reference_end)
        
        ##1 based positions
        #print([r.query_name, r.reference_name, str(position[0]+1), str(position[-1]+1)])
        
        #print(r,r.query_name,r.cigartuples,r.cigar,r.cigarstring)
        if not(r.is_unmapped):
            c=0
            for tuples in r.cigartuples:
                if(int(tuples[0])==7) or (int(tuples[0])==0):
                    if(int(tuples[1])>=12):
                        break
                c+=1
                
            skipLoc=0
            num=0
            for t in r.cigartuples[0:c]:
                if (num==0):
                    if(r.cigartuples[0][0] in [3,4,5]):
                        pass
                    else:
                        skipLoc+=int(t[1])
                else:
                    skipLoc+=int(t[1])
                num+=1
                    
             
            reverseCigar=r.cigartuples[::-1]
            
            c=0
            for tuples in reverseCigar:
                if(int(tuples[0])==7) or (int(tuples[0])==0):
                    if(int(tuples[1])>=12):
                        break
                c+=1
                
            skipLocRev=0
            num=0
            for t in reverseCigar[0:c]:
                if (num==0):
                    if(reverseCigar[0][0] in [3,4,5]):
                        pass
                    else:
                        skipLocRev+=int(t[1])
                else:
                    skipLocRev+=int(t[1])
                num+=1
            
    
            #print(r.query_name,skipLoc,skipLocRev)                                          
            outFH.write("\t".join([r.reference_name,str(r.reference_start+1+skipLoc),str(r.reference_end+1-skipLocRev)]))
            outFH.write("\n")
        
        
    
            
            
                
            
            
                
                    