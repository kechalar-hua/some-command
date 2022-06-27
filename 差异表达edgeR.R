library(edgeR)
countData <- as.matrix(read.csv("gene_count_matrix_fix_name_sort.csv", row.names="gene_id"))
row.names(countData) <- as.character(c(1:dim(countData)[1]))
Groups <-c('LL','LL','LL','LL','LL','LL','LL','LL','LL','LS','LS','LS','LS','LS','LS','LS','LS','LS','HL','HL','HL','HL','HL','HL','HL','HL','HL','HS','HS','HS','HS','HS','HS','HS','HS','HS')
degs <- DGEList(counts = countData, group = Groups);degs

# An object of class "DGEList"
# $counts
# LL1.1 LL1.2 LL1.3 LL2.1 LL2.2 LL2.3 LL3.1 LL3.2 LL3.3 LS1.1 LS1.2 LS1.3 LS2.1 LS2.2 LS2.3 LS3.1 LS3.2 LS3.3 HL1.1 HL1.2 HL1.3 HL2.1 HL2.2 HL2.3
# 1    29    30    49    13    14    33    34    30    37     9    11     9    12    10    14     6    10    10    21    14    36    12    11    35
# 2    11    10    15     8    10    11    17    16    12    37    44    25    27    37    24    35    23    39     8     4     8     9    10    14
# 3     3     3     6     4    15    10     3     6     5     5     4     6     9    20     1     9     5    12     4     3     3     5     9     3
# 4     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0     0
# 5     6     5     5     4     0     2     9    16     7     8    15    17     2     3     1     2     9     4     7     3     1     6     5     6
# HL3.1 HL3.2 HL3.3 HS1.1 HS1.2 HS1.3 HS2.1 HS2.2 HS2.3 HS3.1 HS3.2 HS3.3
# 1    27    17    43     8    12    10    10    13     4     7    19    17
# 2     3     6     7    12    23    18    25    22    20    12    14    16
# 3     3     0     3    15     2    12     8     7    13     5     1    10
# 4     0     0     0     0     0     0     0     0     0     0     0     0
# 5     2     0     4     2     2     1     2     2     3     2     2     4
# 32994 more rows ...

# $samples
# group lib.size norm.factors
# LL1.1    LL  5269508            1
# LL1.2    LL  6556770            1
# LL1.3    LL  5907401            1
# LL2.1    LL  4554300            1
# LL2.2    LL  6213252            1
# 31 more rows ...

countsPerMillion <- cpm(degs)
countCheck <- countsPerMillion > 1
keep <- which(rowSums(countCheck) >= 2)
degs.keep <- degs[keep,]
dim(degs.keep)
#[1] 27122    36
degs.norm <- calcNormFactors(degs.keep, method = 'TMM')
plotMDS(degs.norm, col=as.numeric(degs.norm$samples$group)) 
#limma包中使用无监督聚类方法展示出了样品间的相似性（或差异）。
#可据此查看各样本是否能够很好地按照分组聚类，评估试验效果，判别离群点，追踪误差的来源等。
legend("bottomleft",as.character(unique(degs.norm$samples$group)), col=1:36, pch=20)
designMat <- model.matrix(~0+Groups);designMat
# GroupsHL GroupsHS GroupsLL GroupsLS
# 1         0        0        1        0
# 2         0        0        1        0
# 3         0        0        1        0
# 4         0        0        1        0
# 5         0        0        1        0
# 6         0        0        1        0
# 7         0        0        1        0
# 8         0        0        1        0
# 9         0        0        1        0
# 10        0        0        0        1
# 11        0        0        0        1
# 12        0        0        0        1
# 13        0        0        0        1
# 14        0        0        0        1
# 15        0        0        0        1
# 16        0        0        0        1
# 17        0        0        0        1
# 18        0        0        0        1
# 19        1        0        0        0
# 20        1        0        0        0
# 21        1        0        0        0
# 22        1        0        0        0
# 23        1        0        0        0
# 24        1        0        0        0
# 25        1        0        0        0
# 26        1        0        0        0
# 27        1        0        0        0
# 28        0        1        0        0
# 29        0        1        0        0
# 30        0        1        0        0
# 31        0        1        0        0
# 32        0        1        0        0
# 33        0        1        0        0
# 34        0        1        0        0
# 35        0        1        0        0
# 36        0        1        0        0
# attr(,"assign")
# [1] 1 1 1 1
# attr(,"contrasts")
# attr(,"contrasts")$Groups
# [1] "contr.treatment"

degs.norm <- estimateGLMCommonDisp(degs.norm,design=designMat)
degs.norm <- estimateGLMTrendedDisp(degs.norm, design=designMat)
degs.norm <- estimateGLMTagwiseDisp(degs.norm, design=designMat)
plotBCV(degs.norm)
fit <- glmFit(degs.norm, designMat)

lrt.1vs3 <- glmLRT(fit, contrast = c(0,1,0,-1))
degs.res.1vs3 <- topTags(lrt.1vs3, n = Inf, adjust.method = 'BH', sort.by = 'PValue')
degs.res.1vs3[1:10, ]
#Coefficient:  1*GroupsBM -1*GroupsNJ 
#logFC   logCPM       LR       PValue          FDR
#32   3.637361 9.722601 81.21872 2.020690e-19 2.404622e-17
#109 -4.041356 8.668427 64.34040 1.046773e-15 6.228297e-14
#95  -4.041748 8.653532 62.99162 2.075880e-15 8.234323e-14
#68   3.055712 9.214590 58.60722 1.925091e-14 5.727146e-13
#33   2.747704 9.616616 51.01191 9.180733e-13 2.185014e-11
deGenes.2vs4 <- decideTestsDGE(lrt.1vs3, p=0.05, lfc = 2)
summary(deGenes.2vs4)
#1*GroupsBM -1*GroupsNJ
#Down                       22
#NotSig                     81
#Up                         16
detag <- rownames(lrt.1vs3)[as.logical(deGenes.2vs4)]
plotSmear(lrt.1vs3, de.tags=detag)
abline(h=c(-2, 2), col='blue')
write.table(degs.res.1vs3,file="./degs.res.1vs3",sep="\t",quote =FALSE,row.names=FALSE)