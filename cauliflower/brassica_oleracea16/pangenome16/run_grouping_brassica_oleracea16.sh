#!/bin/bash

set -exuo pipefail

# Set variables
CPU=24
tmpdir="/dev/shm/perso009/brassica_oleracea16"


# make directory on RAM disc
mkdir -p ${tmpdir}


# copy pangenome to the tmpdir
cp -a pangenome_16_DB ${tmpdir}

#make new panproteome if previous attempt to do the grouping failed
#pantools build_pangenome -Xmx100g -Xms50g ${tmpdir}/pangenome_16_DB brassica_oleracea16_genomes.txt


# grouping after relaxation value is calculated with optimal grouping on the RAM disc
pantools -Xmx100g -Xms50g group --relaxation 3 --threads ${CPU} ${tmpdir}/pangenome_16_DB


# copy back for the RAM disc an overwrite my lustre folder
cp -aT ${tmpdir}/pangenome_16_DB .


# gene_classification
pantools gene_classification pangenome_16_DB
