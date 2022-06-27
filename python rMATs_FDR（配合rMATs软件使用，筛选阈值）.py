import sys


def usage():
    print('Usage: python rMATs_FDR.py [*.MATS.JC.txt] [*.MATS.JC.filter.txt]')


def main():
    box = []
    lines = open(sys.argv[1], 'r').readlines()
    for line in lines:
        if line.startswith("ID"):
            box.append(line)
        else:
            tag_FDR = line.strip().split("\t")[-4]
            tag_IncLevelDifference = line.strip().split("\t")[-1]
            if float(tag_FDR) < 0.05 and abs(float(tag_IncLevelDifference)) > 0.1:
                box.append(line)
    new = open(sys.argv[2], 'w')
    for i in box:
        new.write(i)
    new.close()


try:
    main()
except IndexError:
    usage()
