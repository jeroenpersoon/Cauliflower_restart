#!/bin/bash

set -exuo pipefail

# Set variables
CPU=40


# grouping after relaxation value is calculated with optimal grouping on the RAM disc
pantools -Xmx100g -Xms50g group --relaxation 2 --threads ${CPU} proteome_15_DB


# gene_classification
pantools gene_classification proteome_15_DB
