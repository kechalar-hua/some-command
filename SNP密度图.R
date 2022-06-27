library(CMplot)
mydata<-read.table("ASpos.csv",header=TRUE,sep=",")
head(mydata)
# snp         chr       pos
# snp1_1    1        2041
# snp1_2    1        2062
# snp1_3    1        2190
CMplot(mydata,plot.type="d",bin.size=1e6,col=c("darkgreen","yellow", "red"),file="pdf",memo="snp_density",dpi=300) 