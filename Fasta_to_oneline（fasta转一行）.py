# -*- coding: utf-8 -*-
import sys


def usage():
    print('Usage: python script.py [fasta_file] [outfile_name]')


def main():
    outf = open(sys.argv[2], 'w')
    with open(sys.argv[1], 'r') as fastaf:
        for line in fastaf:
            if line.startswith('>'):
                outf.write("\n" + line)
            else:
                outf.write(line.strip())

    outf.close()


try:
    main()
except IndexError:
    usage()
