from collections import Counter
from numpy import *
import sys


def usage():
    print('Usage: python gmap_gff3_count.py [gmap_fmt2.gff3] ')


def main():
    lines = open(sys.argv[1], 'r').readlines()
    name = []
    for line in lines:
        if line.startswith("#"):
            pass
        elif line.strip().split("\t")[2] == "mRNA":
            tag_1 = line.strip().split("\t")[0]
            # tag_2 = line.strip().split("\t")[8].split(";")[1][5:]
            name.append(tag_1)

    list_1 = name
    list_1.sort()

    counter = Counter(list_1)
    new_counter = dict(counter)
    box = []
    for i in counter.keys():
        box.append(new_counter[i])

    final_box = box
    max_num = max(final_box)
    min_num = min(final_box)
    ave_num = mean(final_box)
    print(max_num)
    print(min_num)
    print(ave_num)


try:
    main()
except IndexError:
    usage()
