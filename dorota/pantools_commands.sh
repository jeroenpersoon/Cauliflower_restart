#!/bin/bash

# This is a bash script which can be run after specififying input data etc.
set -exuo pipefail


# Set variables; replace tmpdir with your own folder on the RAM-disc
CPU=40
tmpdir="/dev/shm/perso009/cauliflower"


# List data; check the location of the QC output or change it and change the output file name if you want
realpath QC/genomes_filtered/*.fna > cauliflower_genomes.txt
realpath QC/annotations_filtered/*.gff | awk '{print FNR,$1;}' > cauliflower_annotations.txt
realpath QC/proteins/*.faa > cauliflower_proteins.txt


# Build panproteome; change name of panproteome or input protein accordingly
pantools -Xmx50g -Xms10g build_panproteome proteome_DB cauliflower_proteins.txt


# Build pangenome; change pangenome name and input genomes accordingly
pantools -Xmx50g -Xms10g build_pangenome --threads ${CPU} --scratch-directory ${tmpdir}/scratch ${tmpdir}/pangenome_DB cauliflower_genomes.txt


# Add annotations; change pangenome name and input annotation accordingly
pantools -Xmx50g -Xms10g add_annotations --connect ${tmpdir}/pangenome_DB cauliflower_annotations.txt


# Copy back; change pangenome name accordingly
cp -vr ${tmpdir}/pangenome_DB .


# BUSCO; change odb dataset and pangenome name accordingly. To find the best BUSCO set run busco --list-datasets
#to get a list of all available datasets and choose the one which is the closest to your species of interest
pantools busco_protein --threads ${CPU} -Xmx50g --odb10=brassicales_odb10 pangenome_DB


# optimal grouping; change name and name of the BUSCO set accordingly
pantools optimal_grouping --threads ${CPU} -Xmx50g pangenome_DB pangenome_DB/busco/brassicales_odb10
