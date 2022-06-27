library(ggplot2)
library(ggrepel)

data <- read.csv(file = "voca2.txt",sep = "\t")
data <- na.omit(data)

#data$change <- factor(ifelse(data$FDR < 0.05 & abs(data$Log2FC >= 2),
#                             ifelse(data$Log2FC >= 2,"up","down"),"stable"),
#                      levels = c("up","down","stable"))

#ggplot(data,aes(x=Log2FC,y=-log10(FDR),color = change)) + 
#  geom_point() + 
#  scale_color_manual(values = c("#2a9d8f","#f8961e","#8d99ae80")) +
#  xlim(-10,10) + ylim(0,25) + 
#  geom_hline(yintercept = -log10(0.05),linetype=4,size=0.8) +
#  geom_vline(xintercept = c(-2,2),linetype=4,size=0.8) + 
#  theme(title = element_text(size = 18),text = element_text(size = 18)) +
#  labs(x = "Log2FC",y="-log10(FDR)") + 
#  geom_text_repel(
#   data = data[data$FDR<0.05&abs(data$Log2FC)>2,],
#   aes(label = Gene),max.overlaps = 30,
#   size = 3)

data$change <- as.factor(ifelse(data$FDR < 0.05 & abs(data$Log2FC) >= 1,ifelse(data$Log2FC >= 1,'UP','DOWN'),'NORMAL'))
ggplot(data = data, aes(x = Log2FC, y = -log10(FDR), color = change)) + 
  geom_point(alpha=0.8, size = 1) +  
  theme_bw(base_size = 15) +  
  theme(panel.grid.minor = element_blank(),panel.grid.major = element_blank()) + 
  geom_hline(yintercept=1.5 ,linetype=4) +geom_vline(xintercept=c(-1,1) ,linetype=4 ) +
  scale_color_manual(name = "", values = c("#f8766d", "#00b0f6", "grey"), limits = c("UP", "DOWN", "NORMAL"))