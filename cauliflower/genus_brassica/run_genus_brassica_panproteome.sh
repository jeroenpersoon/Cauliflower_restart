#!/bin/bash

#set variables
#CPU=24
#tmpdir="/dev/shm/perso009/brassica_oleracea"

#List Data
#realpath ../cauliflower4/genomes_filtered/* > genomes.txt
#realpath ../cauliflower4/annotations_filtered/* | awk '{print FNR,$1;}' > annotations.txt

#*.faa makes sure that the path to the logs dir will not be included
#protein sequence files need to end in .faa
realpath QC/proteins/*.faa > proteins.txt


#Build pangenome
#pantools -Xmx200g -Xms200g build_pangenome --threads ${CPU} --scratch-directory ${tmpdir}/scratch ${tmpdir}/pangenome_DB genomes.txt

#Build panproteome
pantools -Xmx200g -Xms200g build_panproteome proteome_DB proteins.txt

#Copy back
#cp -vr ${tmpdir}/proteome_DB ../cauliflower4

#Run Busco to estimate optimal grouping
pantools busco_protein --odb10=brassicales_odb10 proteome_DB/
