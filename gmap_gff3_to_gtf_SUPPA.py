# -*- coding: utf-8 -*-
import sys


def usage():
    print('Usage: python gff2gtf.py [gmap.fmt2.gff3] [output.gtf]')


def main():
    box = []
    with open(sys.argv[1], 'r') as f:
        for line in f:
            if line.startswith("#"):
                pass
            else:
                lin = line.strip().split('\t')
                if lin[2] == 'gene':
                    box.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\ttranscript_id \"%s\"; gene_id \"%s\"" % \
                               (lin[0], lin[1], "transcript", lin[3], lin[4], lin[5], lin[6], lin[7],
                                lin[8].split(';')[0][3:-6] + ".1",
                                lin[0]))
                if lin[2] == 'exon':
                    exon = lin[8].split(';')[0]
                    exon1 = exon.split('exon')[-1]
                    box.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\ttranscript_id \"%s\"; gene_id \"%s\"" % \
                               (lin[0], lin[1], lin[2], lin[3], lin[4], lin[5], lin[6], lin[7],
                                lin[8].split(';')[0][3:-12].strip(".") + ".1",
                                lin[0]))

    new = open(sys.argv[2], "w")
    for i in box:
        new.write(i + "\n")
    new.close()
    print("Done")


try:
    main()
except IndexError:
    usage()
