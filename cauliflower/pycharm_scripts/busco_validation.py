#!/usr/bin/env python3
"""
Author: Jeroen Persoon
Description:
"""

from pathlib import Path
from sys import argv
import pandas as pd

def proteomes_names(proteomes_file):

    with open(proteomes_file, 'r') as proteomes:
        lines = proteomes.readlines()[3:]

    proteomes_dic = {}
    for line in lines:
        proteomes_dic[line.split(',')[0]] = line.split(',')[1].split('/')[-1].split('.')[0]

    return proteomes_dic

def busco_IDs(proteomes_numbers, busco_results_folder, full_table_example):

    ex_full_table = pd.read_csv(full_table_example, sep='\t', skiprows=2)

    # complete busco can be missed when they are not 'Complete' in the example full_table
    busco_df = ex_full_table.loc[ex_full_table["Status"] == "Complete", ["# Busco id"]]#.head(10)

    folder = Path(busco_results_folder)
    for genome in folder.iterdir():
        table_path = str(genome)+"/run_brassicales_odb10/full_table.tsv"

        df = pd.read_csv(table_path, sep='\t', skiprows=2)

        df = df.rename(columns={"Sequence":f"{genome.name}"})

        busco_df = busco_df.merge(df[["# Busco id", f"{genome.name}"]], on="# Busco id", how="left")

    for column in busco_df.columns[1:]:
        busco_df = busco_df.rename(columns={f"{column}" : f"{proteomes_numbers[column]}"})

    busco_df = busco_df.drop_duplicates(subset=["# Busco id"])
    return busco_df


def grep_first(homolohy_groups, busco_IS):
    with open(homolohy_groups, 'r') as f:
        for line in f:
            if busco_IS in line:
                return line
    return None

def busco_groups_numbering(homology_groups, busco_df, busco_ID):

    hom_group = grep_first(homology_groups, busco_ID)
    group_num = hom_group.split(':')[0]

    group = []

    for id in hom_group.split(": ")[1].split(" "):
        id = id.split("#")[0]

        mask = (busco_df == id).any(axis=1)
        busco_id = busco_df[mask]["# Busco id"].iloc[0]

        group.append(busco_id)

    group.insert(0, group_num+": ")


    return hom_group, group



def main():
    full_table_dir = "/home/perso009/lustre/cauliflower/T22species_oleracea15/panproteome/proteome_15_DB/busco/brassicales_odb10/protein/results"
    proteomes = "/home/perso009/lustre/cauliflower/T22species_oleracea15/panproteome/proteome_15_DB/databases/proteomes.txt"


    proteomes_table = proteomes_names(proteomes)

    OX_Heart_full_table = "/home/perso009/lustre/cauliflower/T22species_oleracea15/panproteome/proteome_15_DB/busco/brassicales_odb10/protein/results/14/run_brassicales_odb10/full_table.tsv"
    busco_df = busco_IDs(proteomes_table, full_table_dir, OX_Heart_full_table)

    homology_groups = "/home/perso009/lustre/cauliflower/T22species_oleracea15/panproteome/proteome_15_DB/pantools_homology_groups.txt"

    ID = argv[1]

    hom_group, busco_hom_group = busco_groups_numbering(homology_groups, busco_df, ID)

    print(hom_group)
    print(busco_hom_group)

if __name__ == '__main__':
    main()