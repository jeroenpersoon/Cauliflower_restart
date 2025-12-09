#!/bin/bash

# This is a bash script which can be run to do the grouping and gene_classification
# Make sure to run it with nice -n 19, because this uses many threads
set -exuo pipefail

# Set variables; set number of threads accordingly
CPU=40


# grouping after relaxation value is calculated with optimal grouping, change relaxation setting, panproteome and pangenome name accordingly
pantools -Xmx100g -Xms50g group --relaxation 3 --threads ${CPU} proteome_DB

pantools -Xmx100g -Xms50g group --relaxation 3 --threads ${CPU} pangenome_DB


# gene_classification; set pangenome name accordingly
pantools gene_classification pangenome_DB

# other PanTools functions are run separately, because input data needs to be set specifically
# my advice is to run these commands separately in-line in a screen session.



