#!/usr/bin/env python3
"""
Author: Jeroen Persoon
Description:
"""
import pandas as pd
from subprocess import run

def get_description(gene):
    """
    returns the full_name of the gene from the gff file.

    :param gene: gene id of interest
    :return: full_name of the gene from the gff file
    """

    gff_file = "/home/perso009/lustre/cauliflower_restart/cauliflower/brassica_oleracea16/QC/annotations_filtered/Araport11_GFF3_genes_transposons.current.filtered.gff"

    cmd = f"grep {gene} {gff_file}"
    result = run(cmd, capture_output=True, text=True, shell=True, check=True)
    gff_lines = result.stdout.split('\n')

    # print(gff_lines)
    for line in gff_lines:
        if line.split('\t')[2] == 'gene':
            description = line.split('\t')[-1]
            try:
                return description.split('full_name=')[1].split(';')[0]
            except IndexError:
                try:
                    return description.split('symbol=')[1]
                except IndexError:
                    try:
                        print('im here')
                        print(result)
                        rna_description = result.stdout.split('\n')[1]
                        print(rna_description)
                        rna_description = rna_description.split('\t')[-1]
                        return rna_description.split('Note=')[1].split(';')[0]
                    except IndexError:
                        return 'None'

def main():
    gene = "AT5G10140"
    print(get_description(gene))

if __name__ == '__main__':
    main()
