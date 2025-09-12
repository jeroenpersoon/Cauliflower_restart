#!/bin/bash

echo "Downloading genome and annotation files..."
mkdir -p genomes
cd genomes

wget -i ../genomes_genus_brassica20.txt
for file in *.gz; do
        gunzip "$file"
done

cd ..
mkdir -p annotations
cd annotations

wget -i ../annotations_genus_brassica20.txt
for file in *.gz; do
        gunzip "$file"
done
cd ..
