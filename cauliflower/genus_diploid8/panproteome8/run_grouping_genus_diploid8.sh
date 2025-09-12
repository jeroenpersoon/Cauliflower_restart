#!/bin/bash

set -exuo pipefail

# Set variables
CPU=40



#make new panproteome if previous attempt to do the grouping failed
#pantools build_panproteome -Xmx100g -Xms50g proteome_8_DB genus_diploid8_proteomes.txt



# grouping after relaxation value is calculated with optimal grouping on the RAM disc
pantools -Xmx100g -Xms50g group --relaxation 3 --threads ${CPU} ${tmpdir}/proteome_8_DB



# gene_classification
pantools gene_classification proteome_8_DB
