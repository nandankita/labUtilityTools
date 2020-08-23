#!/bin/bash
for i in `seq 0 87`; 
do
	mkdir "cluster"$i
	cd "cluster"$i
	../setCluster.sh $i
	cd ..
done