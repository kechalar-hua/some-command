#!/usr/local/bin/python
# -*- coding:utf-8 -*-
# file_name:generate_count_matrix.py
# python generate_count_matrix.py 2.salmon_express/ gene_count_matrix.csv     ###(2.salmon_express/ salmon结果文件夹的总文件夹；gene_count_matrix.csv是转录本表达矩阵)
import sys
import pandas as pd
from glob import iglob

sample_path = iglob(sys.argv[1] + "/*/*.count")
dfs = []

for df in sample_path:
    fn = df.split('/')[-1]
    sample_name = fn[:-6]
    dfs.append(pd.read_table(df, header=None, index_col=0,sep='\t', names=["geneid", sample_name]))

matrix = pd.concat(dfs, axis=1)
matrix.to_csv(sys.argv[2])

