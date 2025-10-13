#!/bin/bash

set -exuo pipefail


# Set variables
CPU=40
#tmpdir="/dev/shm/perso009/cauliflower5"


# List data
realpath ../QC/proteins/*.faa > genus_polyploid13_proteomes.txt
#realpath ../QC/annotations_filtered/*.gff | awk '{print FNR,$1;}' > genus_diploid8_annotations.txt


# Build pangenome
#pantools -Xmx50g -Xms10g build_pangenome --threads ${CPU} --scratch-directory ${tmpdir}/scratch ${tmpdir}/pangenome_5_DB cauliflower5_genomes.txt


# Build panproteome
pantools build_panproteome -Xmx50g -Xms10g proteome_13_DB genus_polyploid13_proteomes.txt


# Add annotations
#pantools -Xmx50g -Xms10g add_annotations --connect ${tmpdir}/proteome_5_DB cauliflower5_annotations.txt


# Group
#pantools -Xmx10g -Xms10g group --relaxation 3 --threads ${CPU} ${tmpdir}/pangenome_5_DB


# Copy back
#cp -vr ${tmpdir}/pangenome_4_DB .


# BUSCO
pantools busco_protein --threads ${CPU} -Xmx100g --odb10=brassicales_odb10 proteome_13_DB


# optimal grouping
pantools optimal_grouping --threads ${CPU} -Xmx100g proteome_13_DB proteome_13_DB/busco/brassicales_odb10


# Get region
#pantools-dev extract_region --genome-range "10#NC_001136.10:515000-545000" --output ENA_kmers pangenome_DB/
#pantools-dev extract_region --genome-range "10#NC_001136.10:515000-545000" --output ENA_homology pangenome_DB/ --no-use-kmers --use-homology


# Create minigraph-cactus pangenome for comparison
#[ -d "genomes_cleaned_for_mc" ] && rm -rd genomes_cleaned_for_mc
#mkdir genomes_cleaned_for_mc
#for fasta in $(ls genomes/)
#do
#    awk '/^[^>]/{gsub(/[^ACGTNacgtn]/,"N");} {print;}' genomes/${fasta} | seqkit seq -i > genomes_cleaned_for_mc/${fasta%fna}clean.fna
#done
#realpath genomes_cleaned_for_mc/* | awk 'BEGIN{OFS = "\t";} {n=split($1,a,"/"); split(a[n],b,"_genomic"); gsub(/\./,"_",b[1]); print b[1],$1;}' > genome_names.txt
#singularity exec -B $(pwd):$(pwd) /lustre/BIF/nobackup/worku005/singularity/cactus_v2.9.3-gpu.sif cactus-pangenome ./js ./genome_names.txt --reference GCF_000146045_2_R64 --vcfReference GCF_000146045_2_R64 --outDir minigraph_cactus --outName minigraph_cactus --vcf --giraffe --gbz --xg --gfa --odgi --chrom-vg --chrom-og --mgCores ${CPU} --mapCores ${CPU} --consCores ${CPU} --indexCores ${CPU}
#[ -d "js" ] && rm -rd ./js
