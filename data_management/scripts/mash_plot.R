#!/usr/bin/Rscript
#install.packages("pheatmap")
library(pheatmap)
require(pheatmap)

#TODO: set the working directory to the folder where selected_distances.tsv is in
setwd("C:/Users/jeroe/DocumentenPC/Jeroen/Master Bioinformatics/Thesis/Data/mash_classification_c4_panproteome")

distances <- read.table("selected_distances.tsv", header = FALSE, stringsAsFactors = FALSE)
colnames(distances) <- c("Genome1", "Genome2", "Distance", "p-value", "SharedHashes")

genomes <- unique(c(distances$Genome1, distances$Genome2))
genomes


distance_matrix <- matrix(0, nrow = length(genomes), ncol = length(genomes))
rownames(distance_matrix) <- genomes
colnames(distance_matrix) <- genomes

for (i in 1:nrow(distances)){
  accession1 <- distances$Genome1[i]
  accession2 <- distances$Genome2[i]
  distance_value <- distances$Distance[i]
  distance_matrix[accession1, accession2] <- distance_value
  distance_matrix[accession1, accession2] <- distance_value
}

#change the names of the accessions and make sure that the accessions are corresponding to the 
#correct columns. 
genomes <- c("B. O. botrytis (Korso)", "B. nigra (C2)", "B. nigra (NI100)", "B. napus (ASM38)", "B. carinata (C4012)", "B. carinata (ASM4058)", 
             "B. rapa (CAAS)", "B. O. oleracea (BOL)", "B. napus (Da-Ae)", "B. O. botrytis (Cauliflower)", "B. O. italica (broccoli)", 
             "B. O. capitata (T02)", "B. O. gongylodes (T07)", "B. Oleracea (T13)", "B. O. capitata (T06)", "B. O. italica (T24)", 
             "B. O. alboglabra (T19)", "B. O. botrytis (T25)", "B. O. palmifolia (T12)", "B. oleracea (T10)", "B. O. gemmifera (T08)",
             "B. O. viridis (T17)", "B. O. botrytis (T21)", "B. rapa (AiBai)", "B. juncea (PM)", "B. juncea (HJ)", "B. oleracea (OX-Heart)")

colnames(distance_matrix) <- genomes
rownames(distance_matrix) <- genomes

distance_matrix <- distance_matrix[order(rownames(distance_matrix)), 
                                   order(colnames(distance_matrix))]

pheatmap(distance_matrix, clustering_distance_rows = "euclidean", clustering_distance_cols = "euclidean")

