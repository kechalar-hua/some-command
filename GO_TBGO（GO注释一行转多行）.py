import sys


def usage():
    print('Usage: python GO_TBGO.py [*.GO] [*.TBGO]')

def main():
    lines = open(sys.argv[1]).readlines()
    new = open(sys.argv[2], "w")
    for line in lines:
        list0 = line.strip().split("\t")
        tag = list0[0]
        line_extent = len(list0) - 1
        for i in range(0,line_extent):
            new.write(tag + "\t" + list0[i+1] + "\n")
try:
    main()
except IndexError:
    usage()