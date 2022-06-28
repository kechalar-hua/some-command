# use "-" add in "stem_gene_tpm.txt" blank place


lines = open("combine_and_unmatchcombine.txt").readlines()
stem = open("stem_gene_tpm.txt").readlines()
# make dict for gene-tpm
dict_tpm = {}
for i in stem:
    dict_tpm[i.strip().split("\t")[0]] = i.strip().split("\t")[1]
# dict_keys,for keys not in it leading to index out
key_list = []
for key in dict_tpm.keys():
    key_list.append(key)

# the list used for adding high_express_gene
target_high_express_gene = []
# each line and each gene
for line in lines:
    temp_line = ""
    new_tag = ""
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
        new_tag = gene + "\t" + dict_tpm[gene] + "\t"
        temp_line = temp_line + new_tag
    # sort and find the biggest value and key
    dic1SortList = sorted(dic1.items(), key=lambda d: d[1], reverse=True)
    max1_gene = dic1SortList[0][0]
    max1_gene_value = dic1SortList[0][1]
    max2_gene = dic1SortList[1][0]
    max2_gene_value = dic1SortList[1][1]
    # fold_change > 2 then the gene is target gene
    if max1_gene_value > max2_gene_value*2:
        target_high_express_gene.append(max1_gene)


# count for build high_express_gene table
dict_chr = {}
for i in target_high_express_gene:
    Chr = i.split("G")[0]
    allele = i.split("-")[1][1]
    Chr_tag = Chr + "-" + allele
    if Chr_tag not in dict_chr.keys():
        dict_chr[Chr_tag] = 1
    else:
        dict_chr[Chr_tag] += 1
print(dict_chr)

new = open("advantage.txt", "w")
for key in dict_chr.keys():
    new.write(key + "\t" + str(dict_chr[key]) + "\n")
new.close()
