lines = open("LL.flnc.bam.txt").readlines()
new = open("LL.flnc.fasta", "w")
for line in lines:
    if line == "\n":
        pass
    else:
        tag1 = line.split("\t")[0]
        tag2 = line.split("\t")[9]
        new.write(">" + tag1 + "\n" + tag2 + "\n")
new.close()
