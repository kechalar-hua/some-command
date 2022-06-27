lines = open("Final_trans_oneline.fasta", "r").readlines()
new = open("Final_trans_oneline_shortname.fasta", "w")
for line in lines:
    if line.startswith(">PB"):
        tag = ">" + line.strip().split(":")[0].split("|")[1] + "\n"
        new.write(tag)
    elif line.startswith(">m"):
        tag = ">" + "Ref_" + line.strip().split("/")[1] + "/" + line.strip().split("/")[2] + "\n"
        new.write(tag)
    else:
        tag = line
        new.write(tag)
new.close()
