#!/usr/bin/env python3
"""
Author: Jeroen Persoon
Description:
"""

import pandas as pd


def grep_first(homology_groups, busco_ID):
    with open(homology_groups, 'r') as f:
        for line in f:
            if busco_ID in line:
                return line
    return None

def GOI_hom_group(homology_groups, GOI_ID):

    hom_group = grep_first(homology_groups, GOI_ID)
    group_num = hom_group.split(':')[0]

    return hom_group, group_num

def blast_parser(blast_results):

    with open(blast_results) as f:
        f.readline()
        f.readline()
        columns = f.readline().strip()
    columns = list(columns.split('\t'))


    df = pd.read_csv(blast_results, sep='\t', skiprows=5, header=None, names=columns)

    df_filtered = df[(df["PASS minimum identity"] == "PASS") & (df["PASS minimum alignment length"] == "PASS")]

    IDs_blasted = df_filtered["mRNA identifier"].values.tolist()

    return IDs_blasted

def GOI_in_blast(homology_group, IDs_blasted):
    ID_blasted = []

    homologous = homology_group.split(": ")[1].split(" ")

    for hom in homologous:
        hom_ID = hom.split("#")[0]

        if hom_ID in IDs_blasted:
            ID_blasted.append(f"{hom_ID}: True")
        else:
            ID_blasted.append(f"{hom_ID}: False")

    return ID_blasted


def main():
    homology_groups = "/home/perso009/lustre/cauliflower/T22species_oleracea15/panproteome/proteome_15_DB/pantools_homology_groups.txt"
    GOI = "BolO_3g04880"
    homology_group, hom_group_num = GOI_hom_group(homology_groups, GOI)
    print(f"Homology group of {GOI}:")
    print(homology_group)


    blast_file = "/home/perso009/lustre/cauliflower/T22species_oleracea15/pangenome/blast_results/blastp_results_AT510140_FLC.tsv"
    blasted_IDs = blast_parser(blast_file)
    print('All the IDs which PASS the BLAST')
    print(blasted_IDs, '\n')

    IDs_in_blast = GOI_in_blast(homology_group, blasted_IDs)
    print("Are the homology ID also in the BLAST results?")
    print(IDs_in_blast)

if __name__ == '__main__':
    main()