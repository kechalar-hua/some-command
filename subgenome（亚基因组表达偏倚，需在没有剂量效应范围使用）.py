# -*- coding=utf-8 -*-
import sys


# use "-" add in "stem_gene_tpm.txt" blank place


def usage():
    print('Usage: python sub_genome_bias.py [Allele.match.txt] [TPM.txt] [up1] [down1]')


def main():
    lines = open(sys.argv[1]).readlines()
    stem = open(sys.argv[2]).readlines()
    # make dict for gene-tpm
    dict_tpm = {}
    for i in stem:
        dict_tpm[i.strip().split("\t")[0]] = i.strip().split("\t")[1]

    # dict_keys,for keys not in it leading to index out
    key_list = []
    for key in dict_tpm.keys():
        key_list.append(key)

    # the list used for adding high_express_gene
    # target_high_express_gene = []

    # count signal
    a = 0
    # each line and each gene
    all_level_up1 = []
    all_level_0 = []
    all_level_down1 = []
    dic1Sort_box = []
    for line in lines:
        # temp_line = ""
        # new_tag = ""
        # this dict used for sort
        dic1 = {}
        for lie in range(0, 12):
            tag = line.strip().split("\t")[lie]
            if "|" in tag:
                gene = tag.split("|")[0]
            else:
                gene = tag
            if gene not in key_list:
                dict_tpm[gene] = "0"
            dic1[gene] = float(dict_tpm[gene])
            # new_tag = gene + "\t" + dict_tpm[gene] + "\t"
            # temp_line = temp_line + new_tag
        # sort and find the biggest value and key
        dic1SortList = sorted(dic1.items(), key=lambda d: d[1], reverse=True)
        # if express of one allele in Soff bigger than Sspon, then output it
        dic1Sort_box.append(dic1SortList)
        # use dict
        Soff = {}
        Sspon = {}
        for sample in dic1SortList:
            if sample[0].startswith("-"):
                pass
            elif sample[0].startswith("Soff"):
                Soff[sample[0]] = sample[1]
            elif sample[0].startswith("Sspon"):
                Sspon[sample[0]] = sample[1]
        # compare each Soff allele to each Sspon allele
        level_up1 = []
        level_0 = []
        level_down1 = []
        for x in Soff.keys():
            flag = 1
            for y in Sspon.keys():
                if Soff[x] <= Sspon[y]:
                    flag = 0
            if flag == 1:
                level_up1.append(x)
            else:
                level_0.append(x)
        for xx in Sspon.keys():
            flag = 1
            for yy in Soff.keys():
                if Sspon[xx] <= Soff[yy]:
                    flag = 0
            if flag == 1:
                level_down1.append(xx)
            else:
                level_0.append(xx)
        for i in level_up1:
            all_level_up1.append(i)
        for i in level_0:
            all_level_0.append(i)
        for i in level_down1:
            all_level_down1.append(i)
        a += 1
        print(a)

    new1 = open(sys.argv[3], "w")
    for i in all_level_up1:
        new1.write(i + "\n")
    new1.close()

    # new2 = open(sys.argv[4], "w")
    # for i in all_level_0:
    #     new2.write(i + "\n")
    # new2.close()

    new3 = open(sys.argv[4], "w")
    for i in all_level_down1:
        new3.write(i + "\n")
    new3.close()


    # new4 = open(sys.argv[5], "w")
    # for i in dic1Sort_box:
    #     new4.write(i + "\n")
    # new3.close()

try:
    main()
except IndexError:
    usage()
# count for build high_express_gene table
# dict_chr = {}
# for i in target_high_express_gene:
#     Chr = i.split("G")[0]
#     allele = i.split("-")[1][1]
#     Chr_tag = Chr + "-" + allele
#     if Chr_tag not in dict_chr.keys():
#         dict_chr[Chr_tag] = 1
#     else:
#         dict_chr[Chr_tag] += 1
# new.txt = open("./HS3/advantage.txt", "w")
# for key in dict_chr.keys():
#     new.txt.write(key + "\t" + str(dict_chr[key]) + "\n")
# new.txt.close()
