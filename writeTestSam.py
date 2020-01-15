'''
Created on Dec 29, 2019

@author: nanda
python ~/aTools/utilities/writeTestSam.py 
'''
import pysam
samfile = pysam.AlignmentFile("A01_1.1.subreads.sam", "r")
samfileTest = pysam.AlignmentFile("test.sam", "w", template=samfile)
c=0
for read in samfile.fetch():
    if not(read.is_unmapped):
        if c==0:
            samfileTest.write(read)
            break
        c+1

samfileTest.close()
samfile.close()