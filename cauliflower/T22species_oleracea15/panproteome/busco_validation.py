#!/usr/bin/env python3
"""
Author: Jeroen Persoon
Description: give you the gen id plus homology group for a busco per genome
Usage: python3 busco_validation.py {busco_id}
"""

from pathlib import Path
from sys import argv
import pandas as pd
import os

def proteomes_names(proteomes_file):
    """
    Takes the proteomes.txt file to connect the genome number to the genome name

    :param proteomes_file: proteomes.txt file from the panproteome database
    directory
    :return: dic containing the genome number as key and the genome name as
    value
    """
    #open the file and skips the first three lines
    with open(proteomes_file, 'r') as proteomes:
        lines = proteomes.readlines()[3:]

    #makes a dictionary and puts the genome number as key and takes the genome name form the file path to put it as value
    proteomes_dic = {}
    for line in lines:
        proteomes_dic[line.split(',')[0]] = (
            line.split(',')[1].split('/')[-1].split('.'))[0]

    return proteomes_dic


def busco_IDs(proteomes_numbers, busco_results_folder, full_table_example):
    """
    Creates a pd dataframe of the gen-ids for every busco in every genome

    :param proteomes_numbers: dic contain the genome number and the genome name
    :param busco_results_folder: folder were all the full_table.tsv's are
    :param full_table_example: 1 full_table.tsv to initiate busco names
    :return: pd df including gen-id for every busco for every genome
    """

    #make a df from the example full_table.tsv
    ex_full_table = pd.read_csv(full_table_example, sep='\t', skiprows=2)

    # Makes a df of all the busco names which are NOT duplicated
    busco_df = ex_full_table.loc[ex_full_table["Status"].isin(["Complete", "Missing"]), ["# Busco id"]]#.head(10)

    #gets to all the full_table.tsv for every genome
    folder = Path(busco_results_folder)
    for genome in folder.iterdir():
        table_path = str(genome)+"/run_brassicales_odb10/full_table.tsv"

        #make a df of each file and change the Sequence column name
        df = pd.read_csv(table_path, sep='\t', skiprows=2)

        df = df.rename(columns={"Sequence":f"{genome.name}"})

        #Merge the column with gen-id's with the df containing the busco names
        busco_df = busco_df.merge(df[["# Busco id", f"{genome.name}"]], on="# Busco id", how="left")

    #renames the column of the df to the genome names instead of the genome nums
    for column in busco_df.columns[1:]:
        busco_df = busco_df.rename(columns={f"{column}" : f"{proteomes_numbers[column]}"})

    #remove the duplicated column so that every busco id has one row in the df
    busco_df = busco_df.drop_duplicates(subset=["# Busco id"])


    return busco_df


def grep_first(homology_groups, busco_ID):
    """
    search the homology group where the gen id is in

    :param homology_groups: file, containing all the gen-id per hom group
    :param busco_ID: the id you want to find
    :return: the homology group number when found otherwise returns None
    """
    with open(homology_groups, 'r') as f:
        for line in f:
            if busco_ID in line:
                group_num = line.split(': ')[0]
                return group_num
    return None


def print_cnv(busco_df, busco_id, homology_groups):
    """
    Makes a pd df containing statistics per busco gene

    :param busco_df: df with all the gen-ids for all the busco's for all genomes
    :param busco_id: busco id of interest
    :param homology_groups: file with all the gen-id per homology group
    :return: A data frame contain the gen id for the busco and the homology
    group where this id is in for every genome
    """

    #make a new df of the row containing the busco id
    buscoid_df = busco_df.loc[busco_df["# Busco id"] == busco_id].copy()

    #search the homology group number for each gen-id and makes a list of it
    row = []
    for item in buscoid_df.iloc[0, 1:]:
        if pd.isna(item):
            row.append('non')
        else:
            row.append(grep_first(homology_groups, item))

    row.insert(0, busco_id)
    #adds the list to the df
    buscoid_df.loc[len(buscoid_df)] = row

    return buscoid_df


def print_100busco(busco_df, homology_groups, output):
    """
    Makes a pd df containing statistics per busco gene

    :param busco_df: df with all the gen-ids for all the busco's for all genomes
    :param busco_id: busco id of interest
    :param homology_groups: file with all the gen-id per homology group
    :return: A data frame contain the gen id for the busco and the homology
    group where this id is in for every genome
    """

    #make a new df of the row containing the busco id
    random_buscos = busco_df["# Busco id"].copy()

    #search the homology group number for each gen-id and makes a list of it
    row = []

    for busco in random_buscos:
        buscoids_df = print_cnv(busco_df, busco, homology_groups)
        buscoids_df = buscoids_df.iloc[[1]]

        if len(buscoids_df.iloc[0]) != len(set(buscoids_df.iloc[0])):
            buscoids_df["In 1 Hom. group?"] = "True"
        else:
            buscoids_df["In 1 Hom. group?"] = "False"

        row.append(buscoids_df)

    buscoids_df = pd.concat(row)

    buscoids_df.to_csv(output, sep='\t', index=False)


def main():
    proteome = os.path.abspath(argv[1])
    # full_table_dir = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/panproteome/proteome_15_DB/busco/brassicales_odb10/protein/results"
    # proteomes = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/panproteome/proteome_15_DB/databases/proteomes.txt"
    full_table_dir = proteome+"/busco/brassicales_odb10/protein/results"
    proteomes = proteome+"/databases/proteomes.txt"

    proteomes_table = proteomes_names(proteomes)

    # OX_Heart_full_table = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/panproteome/proteome_15_DB/busco/brassicales_odb10/protein/results/14/run_brassicales_odb10/full_table.tsv"
    ex_full_table = proteome+"/busco/brassicales_odb10/protein/results/1/run_brassicales_odb10/full_table.tsv"
    busco_df = busco_IDs(proteomes_table, full_table_dir, ex_full_table)

    # homology_groups = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/panproteome/proteome_15_DB/pantools_homology_groups.txt"
    homology_groups = proteome+"/pantools_homology_groups.txt"

    # ID = "2at3699"
    # ID = argv[1]

    # TODO: use argv as path to proteome_DB and link the for files needed like that so that only this is needed as input

    # buscoid_df = print_cnv(busco_df, ID, homology_groups)
    # print(buscoid_df)
    output_file = argv[2]

    print_100busco(busco_df, homology_groups, output_file)




if __name__ == '__main__':
    main()
