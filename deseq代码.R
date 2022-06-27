library(DESeq2)
setwd("C:/Users/Administrator/Desktop/第三次作业/第三次作业")
database <- read.table(file = "genes.TMM.EXPR.matrix",sep = "\t", header = T, row.names = 1)
database <- round(as.matrix(database))
head(database) 
condition <- factor(c(rep("BLO_S1",3),rep("BLO_S3",3)))
coldata <- data.frame(row.names =colnames(database),condition)
#行名长度除了第一列只能有两个比较的样品，如果多了的话还没找到方法解决
coldata #查看表
dds <- DESeqDataSetFromMatrix(countData = database,colData = coldata,design = ~condition)
dds2 <- DESeq(dds)
res <- results(dds2,contrast = c("condition","BLO_S1","BLO_S3"))
res #查看结果
#log2 fold change (MLE): condition BLO_S1 vs BLO_S3 
#Wald test p-value: condition BLO_S1 vs BLO_S3 
#DataFrame with 44677 rows and 6 columns
#baseMean log2FoldChange     lfcSE      stat    pvalue      padj
#<numeric>      <numeric> <numeric> <numeric> <numeric> <numeric>
#HF36249    0.0000             NA        NA        NA        NA        NA
#HF06454    0.0000             NA        NA        NA        NA        NA
#HF31517   47.7741       0.684728   0.38713   1.76873 0.0769391    0.3295
#HF07207    0.0000             NA        NA        NA        NA        NA
#HF16138    0.0000             NA        NA        NA        NA        NA
#...           ...            ...       ...       ...       ...       ...
#HF43395  0.648156        1.46211  3.154348  0.463522 0.6429904        NA
#HF20064  0.975549       -2.23965  3.523859 -0.635568 0.5250580        NA
#HF28722  0.000000             NA        NA        NA        NA        NA
#HF28503  0.000000             NA        NA        NA        NA        NA
#HF07368 12.646258        1.06550  0.552114  1.929852 0.0536251  0.265009
summary(res)
#查看一下summary
#out of 27195 with nonzero total read count
#adjusted p-value < 0.1
#LFC > 0 (up)       : 1138, 4.2%
#LFC < 0 (down)     : 1448, 5.3%
#outliers [1]       : 0, 0%
#low counts [2]     : 7131, 26%
#(mean count < 2)
#[1] see 'cooksCutoff' argument of ?results
#[2] see 'independentFiltering' argument of ?results
table(res$padj<0.05) 
#查看一下padj小于0.05的
#FALSE  TRUE 
#17936  2128 
#筛选方法1.
diff_gene_deseq2 <-subset(res, padj < 0.05 & abs(log2FoldChange) > 1)
#或
diff_gene_deseq2 <-subset(res,padj < 0.05 & (log2FoldChange > 1 | log2FoldChange < -1))
dim(diff_gene_deseq2)
head(diff_gene_deseq2)
write.csv(diff_gene_deseq2,file= "DEG_treat_vs_control.csv")

res <- res[order(res$padj),]	
#将结果文件按照res文件中的padj这一列进行降序排列，其中$符号表示res中的padj这一列
resdata <- merge(as.data.frame(res),as.data.frame(counts(dds,normalized = TRUE)),by = "row.names",sort =FALSE)
write.csv(resdata,file = "results.csv")


#根据标签筛选
res1 <- res1[order(res1$padj, res1$log2FoldChange, decreasing = c(FALSE, TRUE)), ]
head(res1)
#log2 fold change (MLE): condition BLO_S3_LD vs KID_S3_LD 
#Wald test p-value: condition BLO_S3_LD vs KID_S3_LD 
#DataFrame with 6 rows and 7 columns
#         baseMean log2FoldChange     lfcSE      stat      pvalue        padj         sig
#        <numeric>      <numeric> <numeric> <numeric>   <numeric>   <numeric> <character>
#HF32109  149.1384      -6.121981  0.441695 -13.86019 1.10379e-43 2.14787e-39          NA
#HF08300   46.0276      -3.570646  0.425339  -8.39483 4.66570e-17 4.53950e-13          NA
#HF15405  332.0315       0.868097  0.130038   6.67570 2.46048e-11 1.59595e-07          NA
#HF13799   40.6525       2.606540  0.406940   6.40522 1.50148e-10 7.30434e-07          up
#HF41669   52.5065      -1.882131  0.297698  -6.32228 2.57724e-10 1.00301e-06          NA
#HF00723   48.6039      -2.281946  0.382487  -5.96607 2.43035e-09 7.88202e-06          NA
res1[which(res1$log2FoldChange >= 1 & res1$padj < 0.01),'sig'] <- 'up'
res1[which(res1$log2FoldChange <= -1 & res1$padj < 0.01),'sig'] <- 'down'
res1[which(abs(res1$log2FoldChange) <= 1 | res1$padj >= 0.01),'sig'] <- 'none'
res1_select <- subset(res1, sig %in% c('up', 'down'))
write.table(res1_select, file = 'BLO_S3_LD vs KID_S3_LD.DESeq2.select.txt', sep = '\t', col.names = NA, quote = FALSE)
res1_up <- subset(res1, sig == 'up')
res1_down <- subset(res1, sig == 'down')
write.table(res1_up, file = 'BLO_S3vsKID_S3.DESeq2.up.txt', sep = '\t', col.names = NA, quote = FALSE)
write.table(res1_down, file = 'BLO_S3vsKID_S3.DESeq2.down.txt', sep = '\t', col.names = NA, quote = FALSE)