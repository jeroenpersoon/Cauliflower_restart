#!/bin/bash

set -exuo pipefail

# Set variables
#CPU=40
#tmpdir="/dev/shm/perso009/brassica_oleracea16"


# make directory on RAM disc
#mkdir -p ${tmpdir}


# copy pangenome to the tmpdir
#cp -a proteome_16_DB ${tmpdir}

#make new panproteome if previous attempt to do the grouping failed
#pantools build_panproteome -Xmx100g -Xms50g ${tmpdir}/proteome_16_DB brassica_oleracea16_proteomes.txt


# grouping after relaxation value is calculated with optimal grouping on the RAM disc
#pantools -Xmx100g -Xms50g group --relaxation 3 --threads ${CPU} ${tmpdir}/proteome_16_DB


# copy back for the RAM disc an overwrite my lustre folder
#cp -aT ${tmpdir}/proteome_16_DB .


# gene_classification
pantools gene_classification proteome_16_DB
