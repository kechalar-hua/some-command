#!/bin/bash
# file_name:extract_gene_cols.sh
# sh extract_gene_cols.sh 2.salmon_express/       ###(2.salmon_express/是salmon结果文件夹的总文件夹)
for i in `ls $1`
do
    sample_name=$i
    awk '{print$1,$4}' $1$i/quant.sf | grep -v 'Name' | sed 's/ /\t/' > $1/$i/${i}.tpms
done

