'''
Created on Mar 28, 2018

@author: nanda
python ~/aTools/utilities/addReadEndToSamBam.py graphmap-pacbio.sam > graphmap-pacbio-endPos.sam
'''
import pysam
import sys

insam= sys.argv[1]
samfile = pysam.AlignmentFile(insam, "r")
outfile = pysam.AlignmentFile("-", "w", template=samfile)

for aln in samfile:
    ys= aln.reference_end
    if not ys:
        ys= -1
    aln.setTag('YS', ys)
    outfile.write(aln)

samfile.close()
outfile.close()
sys.exit()