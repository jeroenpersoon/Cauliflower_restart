Here a description of what is in which folder:

***
documentation/
- guideline.txt
This contains what I did from doing the QC of the genome assemblies up until running my script to mine genetic variation mainly to give a guideline to Dorota once she uses my data

- pipeline.txt
This contains the commands I used to map the reseq accessions to my genome accessions and to extract the reads of a certain region from a .bam file to map those reads to other genomes.

***
pangenomes/
- brassica_oleracea_15
This is the pangenome I used for the species level. Note that this includes OX_heart and 'broccoli' that have a high number of unique genes

- cauliflower_4
This is the pangenome for variety level including the correct annotation for Korso (named T22).

***
panproteomes/
Same as pangenomes but than these are the panproteomes

***
raw_sequence_data/
- annotations
These are all the raw gff files which are selected to do the QC for all evolutionary levels.

- genomes
These are all the genome assemblies which are selected to do the QC for all evolutionary levels. 

***
results/
- fastqc_reports/
This contains all the fastaqc reports an the multiqc report for all the reseq accessions

- mapping
	- DEG3
	All the files used to map the DEG3 reads in liria to T25
	- ELF3
	All the files used regarding the mapping of ELF3 reads in liria to all the genome assemblies
	- whole_genome_T22
	All the files used to get the results for mapping the reseq accessions to T22

- variant_calling
vcf files for calling the variants for all the resequenced accessions mapped to T22 and for the ELF3 reads mapped to T25

- variation_tables
	- cauliflower
	This folder includes all the variation tables I used using the cauliflower_4 pangenome
	- brassica_oleracea
	This folder includes all the variation tables I used using the brassica_oleracea_15 pangenome.

***
scripts/
- busco_validation.py
To see it 100 random busco's are grouped in the same homology group

- coverage.sh 
Used to write the average coverage for the reseq accessions mapped to T22

- Fasta_validation.py
Used to check if two FASTA files are identical to each other

- mapping_script.sh
script to map all the reseq accessions to T22 expect for liria

- mash_plot.R
Used to make the mash plot showing the sequence based distance between genome assemblies

- msa.py
Used to get a FASTA file with the GOI which can be used to contruct an MSA

- pantools_command.sh
All the PanTools commands I run to construct the panproteomes/pangenomes up until the optimal_grouping

- pantools_grouping.sh
All commands which I run after I determined the optimal relaxation to group the genes

- upset_c4.R
Used to make the upset plot showing the core, accessory, and unique genes in a panproteome/pangenome. The names of the accessions are changed when running this on a panproteome/pangenome with differen assemblies

- Variation_table.py
script to construct a variation table showing the variation in a gene of interest in the assemblies.
