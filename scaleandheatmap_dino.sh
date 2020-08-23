#!/bin/bash
for i in `seq 1 88`; 
do
	matrix="Dino-HiC-Dplus-R1_chr"$i"_8000_dino_iced"
	F=$matrix".matrix.gz"
	H=$matrix".scaled-100000000.matrix.gz"
	echo item: $matrix
	perl ~/cworld/cworld/scripts/perl/scaleMatrix.pl -v -i $F --st 100000000
	perl ~/cworld/cworld/scripts/perl/heatmap.pl -i $H -v --dl --start 0 --end 700
done
