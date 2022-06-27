install.packages("VennDiagram")
library(VennDiagram)
data = read.table("fourioe.txt",header = T,sep="\t")
head(data)
venn.plot <- venn.diagram(
  x = list(
    LL = data$LLevent,
    LS = data$LSevent,
    HL = data$HLevent,
    HS = data$HSevent
  ),
  filename = "ioe.4quadruple_Venn.tiff",
  col = "black",
  lty = "dotted", #边框线型改为"dotted"虚线
  lwd = 3, # 边框线的宽度
  fill = c("cornflowerblue", "green", "yellow", "darkorchid1"),
  alpha = 0.50,
  label.col = c("orange", "white", "darkorchid4", "white", "white", "white",
                "white", "white", "darkblue", "white",
                "white", "white", "white", "darkgreen", "white"),
  cex = 1.5,
  fontfamily = "serif",
  fontface = "bold",
  cat.col = c("darkblue", "darkgreen", "orange", "darkorchid4"),
  cat.cex = 1.5,
  cat.fontface = "bold",
  cat.fontfamily = "serif"
)