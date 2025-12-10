#! /usr/bin/env RScript

#Assuming the R libraries were installed via Conda, the next line can be ignored. If not, use it to manually install the required package
#install.packages("UpSetR", "~/local/R_libs/", "https://cran.us.r-project.org")
library(UpSetR)

allowed_sets <- 50
allowed_intersects <- NA # NA visualizes all intersections. Include a number to limit intersections in plot
font_size <- 1.5
plot_width <- 25
plot_height <- 5

df1 <- read.csv(file = '/lustre/BIF/nobackup/perso009/cauliflower/T22panproteome/panproteome/proteome_4_DB/gene_classification/upset/input/genomes.txt', sep = ',', header = TRUE, check.names=FALSE)
plot1 <-upset(df1, nsets = allowed_sets, nintersects = allowed_intersects, text.scale = font_size)
pdf(file = "/lustre/BIF/nobackup/perso009/cauliflower/T22panproteome/panproteome/proteome_4_DB/gene_classification/upset/output/genomes.pdf", width = plot_width, height = plot_height)
plot1
dev.off()

cat("\nOutput written to: /lustre/BIF/nobackup/perso009/cauliflower/T22panproteome/panproteome/proteome_4_DB/gene_classification/upset/output/genomes.pdf\n\n")