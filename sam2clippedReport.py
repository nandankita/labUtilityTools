'''
Created on Dec 26, 2019

@author: nanda
python ~/aTools/utilities/sam2clippedReport.py mD7.subreads.sam 
/nl/umw_job_dekker/users/an27w/rawPacBio/gapclosed/blasr
python ~/aTools/utilities/sam2clippedReport.py C01_1.2.subreads.sam
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
                if(t[0] in [4,5,1]):
                    pass
                else:
                    skipLoc+=int(t[1])
                    
            reverseCigar=r.cigartuples[::-1]
            
            c=0
            for tuples in reverseCigar:
                if(int(tuples[0])==7) or (int(tuples[0])==0):
                    if(int(tuples[1])>=12):
                        break
                c+=1
                
            skipLocRev=0

            for t in reverseCigar[0:c]:
                if(t[0] in [4,5,1]):
                    pass
                else:
                    skipLocRev+=int(t[1])
#                         if(r.query_name=="m160210_085804_42183_c100934322550000001823210305251655_s1_p0/72759/39517_40165"):
#                             print("hi",t[1],skipLocRev)
                     
#             if(r.query_name=="m160210_085804_42183_c100934322550000001823210305251655_s1_p0/72759/39517_40165"):
#                 print(r.cigartuples,r.reference_name,str(r.reference_start+1+skipLoc),str(r.reference_end+1-skipLocRev))
#                 s=0
#                 ins=0
#                 dele=0
#                 for i in r.cigartuples:
#                     s+=i[1]
#                     if(int(i[0])==1):
#                         ins+=i[1]
#                     if(int(i[0])==2):
#                         dele+=i[1]
                #print(r,r.cigartuples,s,r.reference_name,ins,dele,r.reference_start,r.reference_end,r.reference_length,r.query_alignment_start,r.query_alignment_end,r.query_alignment_length)
#             if(r.reference_name=="cluster48" and (r.reference_end+1-skipLocRev)<0):
#                 print(r.query_name)
#                 s=0
#                 for i in r.cigartuples:
#                     s+=i[0]
#                 print(s,r.reference_end,skipLocRev,len(r.cigar))
            #print(r.query_name,skipLoc,skipLocRev)                                          
            outFH.write("\t".join([r.reference_name,str(r.reference_start+1+skipLoc),str(r.reference_end+1-skipLocRev)]))
            outFH.write("\n")
        
        
    
            
            
                
            
            
                
                    