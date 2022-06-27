library(tidyverse)

length <- read_tsv("Length.txt") %>% group_by(length) %>%
  summarise(Count = n())
length$length <- as.character(length$length)
sum <- sum(length$Count)
ggplot(length) + geom_col(aes(length, Count), width = 0.8) + 
  geom_line(aes(length, Count), group = 1) + geom_point(aes(length, Count)) + 
  scale_y_continuous(sec.axis = sec_axis(~.*100/sum, name = "% Relative Abundance")) + xlab("Length") +
  theme_bw() + theme(panel.grid = element_blank(), 
                     axis.title = element_text(size = 15))

data <- read.table("Length.txt", header = F)
# 设置插入片段长度的阈值，过滤掉太长的片段
length_cutoff <- 15000
fragment <- data$V1[data$V1 <= length_cutoff]
# 利用直方图统计频数分布，设置柱子个数
breaks_num <- 2000
res <- hist(fragment, breaks = breaks_num, plot = FALSE)
# 添加坐标原点
plot(x = c(0, res$breaks),
     y = c(0, 0, res$counts) / 10^2,
     type = "l", col = "red",
     xlab = "Fragment length(bp)",
     ylab = expression(Normalized ~ read ~ density ~ 10^2),
     main = "Sample Fragment sizes")
ggsave("Length.png", height = 5, width = 8)
ggsave("Length.pdf", height = 5, width = 8)