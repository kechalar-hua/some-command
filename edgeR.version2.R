library(edgeR)
countData <- as.matrix(read.csv("gene_count_matrix.csv", row.names="gene_id"))
row.names(countData) <- as.character(c(1:dim(countData)[1]))
Groups <-c('LL1','LL1','LL1','LL2','LL2','LL2','LL3','LL3','LL3','LS1','LS1','LS1','LS2','LS2','LS2','LS3','LS3','LS3','HL1','HL1','HL1','HL2','HL2','HL2','HL3','HL3','HL3','HS1','HS1','HS1','HS2','HS2','HS2','HS3','HS3','HS3')
degs <- DGEList(counts = countData, group = Groups);degs
#An object of class "DGEList"
#$counts
#BM_1_Le BM_2_Le BM_3_Le N57_1_Le N57_2_Le N57_3_Le NJ_1_Le NJ_3_Le
#1       0       0       0        3        1        3       2       0
#2       0       2       2        1        1        0       0       0
#3       0       1       0        3        0        0       2       1
#4       0       2       1        0        1        1      11       8
#5       0       2       1        0        1        1      10       7
#NJ_4_Le Y83_1_Le Y83_2_Le Y83_3_Le YBA_1_Le YBA_2_Le YBA_3_Le
#1       0        2        0        3        0        0        0
#2       1        2        0        1        1        0        0
#3       0        0        0        2        3        2        0
#4       4        0        0        0        1        4        2
#5       4        0        0        0        1        4        2
#ZZ1_1_Le ZZ1_2_Le ZZ1_3_Le
#1        5        0        0
#2        0        1        1
#3        1        1        1
#4        0        0        0
#5        0        0        0
#115 more rows ...

#$samples
#group lib.size norm.factors
#BM_1_Le     BM   106324            1
#BM_2_Le     BM   154457            1
#BM_3_Le     BM   217500            1
#N57_1_Le   N57    81634            1
#N57_2_Le   N57   239974            1
#13 more rows ...

countsPerMillion <- cpm(degs)
countCheck <- countsPerMillion > 1
keep <- which(rowSums(countCheck) >= 2)
degs.keep <- degs[keep,]
dim(degs.keep)
#[1] 119  18
degs.norm <- calcNormFactors(degs.keep, method = 'TMM')
plotMDS(degs.norm, col=as.numeric(degs.norm$samples$group)) 
#limma包中使用无监督聚类方法展示出了样品间的相似性（或差异）。
#可据此查看各样本是否能够很好地按照分组聚类，评估试验效果，判别离群点，追踪误差的来源等。
legend("bottomleft",as.character(unique(degs.norm$samples$group)), col=1:6, pch=20)
designMat <- model.matrix(~0+Groups);designMat
##GroupsBM GroupsN57 GroupsNJ GroupsY83 GroupsYBA GroupsZZ1
#1         1         0        0         0         0         0
#2         1         0        0         0         0         0
#3         1         0        0         0         0         0
#4         0         1        0         0         0         0
#5         0         1        0         0         0         0
#6         0         1        0         0         0         0
#7         0         0        1         0         0         0
#8         0         0        1         0         0         0
#9         0         0        1         0         0         0
#10        0         0        0         1         0         0
#11        0         0        0         1         0         0
#12        0         0        0         1         0         0
#13        0         0        0         0         1         0
#14        0         0        0         0         1         0
#15        0         0        0         0         1         0
#16        0         0        0         0         0         1
#17        0         0        0         0         0         1
#18        0         0        0         0         0         1
attr(,"assign")
#[1] 1 1 1 1 1 1
attr(,"contrasts")
attr(,"contrasts")$Groups
#[1] "contr.treatment"

degs.norm <- estimateGLMCommonDisp(degs.norm,design=designMat)
degs.norm <- estimateGLMTrendedDisp(degs.norm, design=designMat)
degs.norm <- estimateGLMTagwiseDisp(degs.norm, design=designMat)
plotBCV(degs.norm)
fit <- glmFit(degs.norm, designMat)

lrt.1vs3 <- glmLRT(fit, contrast = c(1,0,-1,0,0,0))
degs.res.1vs3 <- topTags(lrt.1vs3, n = Inf, adjust.method = 'BH', sort.by = 'PValue')
degs.res.1vs3[1:5, ]
#Coefficient:  1*GroupsBM -1*GroupsNJ 
#logFC   logCPM       LR       PValue          FDR
#32   3.637361 9.722601 81.21872 2.020690e-19 2.404622e-17
#109 -4.041356 8.668427 64.34040 1.046773e-15 6.228297e-14
#95  -4.041748 8.653532 62.99162 2.075880e-15 8.234323e-14
#68   3.055712 9.214590 58.60722 1.925091e-14 5.727146e-13
#33   2.747704 9.616616 51.01191 9.180733e-13 2.185014e-11
deGenes.1vs3 <- decideTestsDGE(lrt.1vs3, p=0.05, lfc = 1)
summary(deGenes.1vs3)
#1*GroupsBM -1*GroupsNJ
#Down                       22
#NotSig                     81
#Up                         16
detag <- rownames(lrt.1vs3)[as.logical(deGenes.1vs3)]
plotSmear(lrt.1vs3, de.tags=detag)
abline(h=c(-1, 1), col='blue')
write.table(degs.res.1vs3,file="./degs.res.1vs3",sep="\t",quote =FALSE,row.names=FALSE)