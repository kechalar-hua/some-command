# -*- coding:utf-8 -*-
import sys

"""
fasta文件GC含量测定
"""


def usage():
    print('Usage: python GC_content.py [fasta_file]')


def main():
    gc_content = open(sys.argv[1], "r")
    # set the the values to 0
    a = 0
    g = 0
    c = 0
    t = 0
    gc_content.readline()
    for line in gc_content:
        line = line.lower()
        if line.startswith(">"):
            pass
        else:
            for gc in line.lower():
                if gc == "a":
                    a += 1
                if gc == "c":
                    c += 1
                if gc == "g":
                    g += 1
                if gc == "t":
                    t += 1
    # print("number of a's " + str(a))
    # print("number of c's " + str(c))
    # print("number of g's " + str(g))
    # print("number of t's " + str(t))
    gc = (g + c + 0.) / (a + t + g + c + 0.)
    print("gc content:" + str(gc))


try:
    main()
except IndexError:
    usage()
