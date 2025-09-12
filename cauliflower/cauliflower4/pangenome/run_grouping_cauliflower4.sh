#!/bin/bash

set -exuo pipefail

# Set variables
#CPU=24
#tmpdir="/dev/shm/perso009/cauliflower4"


# make directory on RAM disc
#mkdir -p ${tmpdir}


# copy pangenome to the tmpdir
#cp -a pangenome_4_DB ${tmpdir}


#make new panproteome if previous attempt to do the grouping failed
#pantools build_panproteome -Xmx100g -Xms50g ${tmpdir}/proteome_16_DB brassica_oleracea16_proteomes.txt


# grouping after relaxation value is calculated with optimal grouping on the RAM disc
#pantools -Xmx100g -Xms50g group --relaxation 2 --threads ${CPU} ${tmpdir}/pangenome_4_DB


# copy back for the RAM disc an overwrite my lustre folder
#cp -aT ${tmpdir}/pangenome_4_DB pangenome_4_DB


# gene classification
pantools gene_classification pangenome_4_DB
