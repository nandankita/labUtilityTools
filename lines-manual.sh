#!/bin/bash
echo "setting up cluster" $1 "with line cluster" $2
cluster=$1
((var=$1+1))
chr="chr"$var
line=$2
less "/nl/umw_job_dekker/users/an27w/dinoflagellets/analysis/lines-manualAssembly-4/headerschr"  | awk '{split($1,a,"__");{if(a[1]=="'${chr}'"){print $1"\t""'${cluster}'"}}}' > h1
less "/nl/umw_job_dekker/users/an27w/dinoflagellets/analysis/lines-manualAssembly-4/Karyotype_40000_large_clusters_LinesSorted.tab" | awk '{if($4=="'${line}'"){print $1"__"$2"__"$3"\t""'${cluster}'"}}' > h2
cat h1 h2 > "selectedOrder"$cluster
rm h1 h2
python ~/aTools/utilities/extractCisInteractions.py -i "/nl/umw_job_dekker/users/an27w/dinoflagellets/analysis/lines-manualAssembly-4/Dino-HiC-Dplus.40000.rearranged.scaled-100000000.matrix" -o "rearranged_cluster"$cluster".matrix" -f "selectedOrder"${cluster} -n ${cluster}
cp ../drawHeatmap.sh .
cp ../extract.R  .
