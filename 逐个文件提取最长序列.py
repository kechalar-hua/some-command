#!/usr/bin/env python
# -*- coding=utf-8 -*-

"""
提取序列文件中最长的转录本ID
"""

Fasta = open("Sspon.01G0000060.fasta", "r")
Sequence = {}
Sequence_seq = {}
## 1.创建ID和序列的字典，一个用于排序，一个用于存储序列
for line in Fasta.readlines():
    content = line.strip()
    if content.startswith(">"):
        name = content[1:]
        Sequence[name] = 0
        Sequence_seq[name] = ""
    else:
        Sequence[name] += len(content)
        Sequence_seq[name] += content
Fasta.close()

## 2.字典按照值从大到小排序
Sequences = sorted(Sequence.items(), key=lambda d: d[1], reverse=True)

## 3.提取最长的一条序列
longest_id = Sequences[1][0]
longest_seq = Sequence_seq[longest_id]
# print(longest_id)
# print(Sequence_seq[longest_id])
new = open("Sspon.01G0000060.longest.fasta", "w")
new.write(">" + longest_id + "\n")
new.write(longest_seq + "\n")
new.close()
