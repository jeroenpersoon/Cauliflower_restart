#! /usr/bin/env RScript

# Use one of the following files
# /lustre/BIF/nobackup/perso009/cauliflower/brassica_oleracea16/panproteome16/proteome_16_DB/gene_classification/distances_for_tree/genome_distance_distinct_genes.csv
# /lustre/BIF/nobackup/perso009/cauliflower/brassica_oleracea16/panproteome16/proteome_16_DB/gene_classification/distances_for_tree/genome_distance_inf_distinct_genes.csv
# /lustre/BIF/nobackup/perso009/cauliflower/brassica_oleracea16/panproteome16/proteome_16_DB/gene_classification/distances_for_tree/genome_distance_all_genes.csv

#Assuming the R libraries were installed via Conda, the next line can be ignored. If not, use it to manually install the required package
#install.packages("ape", "~/local/R_libs/", "https://cran.us.r-project.org")
library(ape)

input = read.csv("/lustre/BIF/nobackup/perso009/cauliflower/brassica_oleracea16/panproteome16/proteome_16_DB/gene_classification/distances_for_tree/genome_distance_distinct_genes.csv", sep=",", header = TRUE)
dataframe = subset(input, select = -c(Genomes))
df.distance = as.matrix(dataframe, labels=TRUE)
colnames(df.distance) <- rownames(df.distance) <- input[['Genomes']]
NJ_tree <- nj(df.distance)
write.tree(NJ_tree, tree.names = TRUE, file="/lustre/BIF/nobackup/perso009/cauliflower/brassica_oleracea16/panproteome16/proteome_16_DB/gene_classification/genome_gene_distance.tree")
cat("\nGene distance tree written to: /lustre/BIF/nobackup/perso009/cauliflower/brassica_oleracea16/panproteome16/proteome_16_DB/gene_classification/genome_gene_distance.tree\n\n")