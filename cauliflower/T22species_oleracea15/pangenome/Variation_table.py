#!/usr/bin/env python3
"""
Author: Jeroen Persoon
Description:
"""

import pandas as pd
from subprocess import run
from sys import argv

def do_pangenome_blast(pangenome_path, query):
    """
    Does a first pangenomic blast with a GOI, for example an Arabidopsis gene

    :param pangenome_path: path to pangenome_DB
    :param query: file containing the GOI in fasta format
    :return: the gen name of one of the genomes in the pangenome which was on
    top of the blast results table
    """

    # runs the blast using pantools
    # cmd = ["pantools", "blast", pangenome_path, query]
    # run(cmd, check=True)

    blast_results = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/pangenome/pangenome_15_DB/BLAST/blast_results.tsv"

    # get the columns to make a pd.df of the blast results
    with open(blast_results) as f:
        f.readline()
        f.readline()
        columns = f.readline().strip()
    columns = list(columns.split('\t'))

    # makes a pd.df from the blast results.
    df = pd.read_csv(blast_results, sep='\t', skiprows=5, header=None, names=columns)

    # only keeps the entries which PASS the minimum identity and alignment length
    df_filtered = df[(df["PASS minimum identity"] == "PASS") & (df["PASS minimum alignment length"] == "PASS")]

    # copies the results to other location so the blast_results.tsv can be
    # overwritten
    # cp_cmd = ["cp", blast_results, "blast_results_AT.tsv"]
    # run(cp_cmd, check=True)

    # takes the best id to blast back to the pangenome
    blast_ID = df_filtered["subject"].iloc()[0]

    # saves all the blasted ids in a list to check whether the blast_back with
    # the best pangenomic hit would result in more hits.
    # blast_IDs = df_filtered["subject"].values.tolist()
    # blast_IDs = list(set(blast_IDs))
    # print(len(blast_IDs))

    return blast_ID


def search_protein(fasta_file, protein):
    """
    Goes through a fasta file to return a fasta header and sequence based on a
    search term

    :param fasta_file: fasta file
    :param protein: search term which is in the header
    :return: string, header. string, sequence
    """
    header = None
    seq = []

    with open(fasta_file, 'r') as f:

    # goes through all the lines and checks if it is a header
        for line in f:
            line = line.strip()
            if line.startswith('>'):

    # if there is a header and the gen id is in the header returns the header
    # and sequence
                if header and protein in header:
                    return header, "".join(seq)
    # if not reset the header and sequence
                else:
                    header = line
                    seq = []
    # if line is not a header put the sequence in a list (or append the seq)
            else:
                seq.append(line)

    # returns last header and sequence if the proteine is in there
        if header and protein in header:

            return header, "".join(seq)

    # if not found return None
        return None, None


def extend_blast_list(best_ID, pangenome_path):
    """
    Does another blast to the pangenome to extend the blast hits

    :param best_ID: best hit when blasting a known GOI
    :param pangenome_path: Path to the pangenome_DB
    :return: list of gen-ids which passed the blast.
    """

    #TODO: change the input to a single query in a file already gen-ids are useless in another case

    # ID, genome_num = best_ID.split('_genome_')
    #
    # protein_files_path = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/pangenome/pangenome_15_DB/proteins"
    #
    # protein_file = f"{protein_files_path}/proteins_{genome_num}.fasta"
    # header, seq = search_protein(protein_file, ID)
    #
    # query_file = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/pangenome/best_blast_query.fasta"
    #
    # with open(query_file, 'w') as seqfile:
    #     seqfile.write(f"{header}\n{seq}")
    #
    # cmd = ["pantools", "blast", pangenome_path, query_file]
    # run(cmd, check=True)
    #
    # blast_results = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/pangenome/pangenome_15_DB/BLAST/blast_results.tsv"

    blast_results = argv[1]
    #blast_results = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/pangenome/blast_results_AT.tsv"

    # makes a pd.df from the blast results just like earlier.
    with open(blast_results, 'r') as f:
        f.readline()
        f.readline()
        columns = f.readline().strip()
    columns = list(columns.split('\t'))

    df = pd.read_csv(blast_results, sep='\t', skiprows=5, header=None,
                     names=columns)

    # makes a list from all the gen-ids which pass the blast
    # TODO need to return something else
    df_filtered = df[(df["PASS minimum identity"] == "PASS") & (
                df["PASS minimum alignment length"] == "PASS")]

    blast_IDs = df_filtered["subject"].values.tolist()
    blast_IDs = list(set(blast_IDs))

    return blast_IDs, df_filtered


def check_hom_groups(grouping_file, best_IDs):
    """
    Makes a file with gen-ids from all the blast ids and searches their homology
    group numbers

    :param grouping_file: file containing the homology groups
    :param best_IDs: list, id+genome# which passed the blast
    :return: dic, with gen-id as key and homology group number as value
    list, of all the different group numbers represented in the dic
    """

    blasted_ids = []

    # makes search_terms.txt and puts all the blasted ids in it (without genome
    # number) to search the homology groups
    search_terms = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/pangenome/search_terms.txt"
    with open(search_terms, 'w') as term_file:
        for item in best_IDs:
            id = item.split('_genome_')[0]
            blasted_ids.append(id)
            term_file.write(id+'\n')

    id_dic = {}
    # goes through all the gen-ids and finds them in the homology grouping
    # file with a grep command. The homology group number is saved in a
    # dictionary with the gen-id as key and the group number as value
    with open(search_terms, 'r') as terms:
        for line in terms:
            line = line.strip()
            cmd = ['grep', f'{line}', grouping_file]
            result = run(cmd, capture_output=True, text=True, check=True)
            id_dic[line] = result.stdout.split(': ')[0]

    # makes a list of all the group number represented.
    all_groups = list(set(id_dic.values()))

    return id_dic, all_groups


def contamination(group_numbers, group_num_per_id, grouping_file):
    """
    makes a list of gen-ids which are in the same hom groups as blasted ids
    but were not blasted themselves.

    :param group_numbers: list of all different group numbers of blasted ids
    :param group_num_per_id: dic, with blasted id and group number
    :param grouping_file: homology grouping file
    :return:
    """

    ids_in_groups = []

    # goes through every homology group number and adds all the gen-ids of
    # the genes in those groups to a list
    for num in group_numbers:
        cmd = ['grep', num, grouping_file]
        result = run(cmd, capture_output=True, text=True, check=True)
        result = result.stdout.split(': ')[1]
        ids = result.strip().split(' ')
        for id in ids:
            ids_in_groups.append(id.split('#')[0])

    # goes through all the blasted gen-ids and all the gen-ids which are in
    # the represented group. Saves all the gen-ids which are in the homology
    # groups but were not blasted.
    for key in group_num_per_id.keys():
        if key in ids_in_groups:
            ids_in_groups.remove(key)

    return ids_in_groups


def writer(id_genome_num, id_group_num_dic, df_filtered):
    """
    makes a dic with gen-id as key and a list of homology group and
    genome number as values

    :param id_genome_num: list of gen-id+genome#
    :param id_group_num_dic: dic with gen id and hom group number
    :param df_filtered:
    :return: dic with gen-id as key and a list of homology group and
    genome number as values
    """

    start_pos = df_filtered["start coordinate"].values.tolist()
    end_pos = df_filtered["end coordinate"].values.tolist()

    # goes over every gen-id in de dic and extents every value with the
    # corresponding group number
    for i, key in enumerate(id_group_num_dic.keys()):
        value = [id_group_num_dic[key], id_genome_num[i].split('_genome_')[1]]
        value.append(start_pos[i])
        value.append(end_pos[i])
        id_group_num_dic[key] = value

    return id_group_num_dic


def best_hit(blast_ids, arabidopsis_path, cauliflower_path, ara_hits, cau_hits):
    """
    Makes a query file of the blasted gen-ids and does the blast on arabidopsis
    and cauliflower

    :param blast_ids: list of gen-ids+genome#
    :param arabidopsis_path: path to arabidopsis genome fasta file
    :param cauliflower_path: path to cauliflower genome fasta file
    :return:
    """
    queries = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/pangenome/queries.fasta"
    protein_files = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/pangenome/pangenome_15_DB/proteins"

    # for every gen-id+genome# finds the protein file and finds the fasta
    # header and sequence. Writes these fasta headers and sequences to a file
    with open(queries, 'w') as q_out:
        for item in blast_ids:
            id, genome = item.split("_genome_")
            protein_file = f"{protein_files}/proteins_{genome}.fasta"

            header, sequence = search_protein(protein_file, id)

            q_out.write(header+'\n'+sequence+'\n')


    # makes blast database for arabidopsis and does the blast
    mk_db_cmd = ["makeblastdb", "-in", arabidopsis_path, "-dbtype", "prot", "-out", "Araport11_prot_db"]
    run(mk_db_cmd, check=True)

    cmd = ["blastp", "-query", queries, "-db", "Araport11_prot_db", "-out",
           ara_hits, "-outfmt", "7"]
    run(cmd, check=True)

    # makes blast database for cauliflower and does the blast
    mk_db_cmd = ["makeblastdb", "-in", cauliflower_path, "-dbtype", "prot", "-out", "cauliflower_prot_db"]
    run(mk_db_cmd, check=True)

    cmd = ["blastp", "-query", queries, "-db", "cauliflower_prot_db", "-out", cau_hits, "-outfmt", "7"]
    run(cmd, check=True)


def hit_parser(best_hits):
    """
    goes through a blast results file to take the best hit for each input query

    :param best_hits: blast results file where multiple queries were used.
    :return: string with the gen-id of the best hit
    string with the identity percentage.
    """
    best_hits_ids = []
    percentages = []

    with open(best_hits, 'r') as hits:
        value = 4
        for i, line in enumerate(hits):

    # when arrived at the fourth line add the amount of hits for this query to
    # the to_add variable
            if i == value:
                to_add = line.split(" ")[1]
                continue

    # after the line with the amount of hits the best hit comes, so saves the
    # gen-id and identity percentage to a list.
            elif i > value:
                best_hits_ids.append(line.split('\t')[1])
                percentages.append(line.split('\t')[2])
                value += (int(to_add) + 5)
                continue

        return best_hits_ids, percentages


def get_description(gene):
    """
    returns the full_name of the gene from the gff file.

    :param gene: gene id of interest
    :return: full_name of the gene from the gff file
    Note: gff description needs to be complete.
    """
    gff_file = "/home/perso009/lustre/cauliflower_restart/cauliflower/brassica_oleracea16/QC/annotations_filtered/Araport11_GFF3_genes_transposons.current.filtered.gff"

    # cmd = ["grep", gene, gff_file, "|", "grep", "gene"]
    cmd = f"grep {gene} {gff_file} | grep gene"
    result = run(cmd, capture_output=True, text=True, shell=True, check=True)
    description = result.stdout.split('\t')[-1]

    # return the full name if that is in the gff file otherwise tries to return
    # the symbol otherwise returns None
    try:
        return description.split('full_name=')[1].split(';')[0]
    except IndexError:
        try:
            return description.split('symbol=')[1]
        except IndexError:
            return "None"

def output_writer(table_dic, output_file, best_ara_hits, best_cau_hits):
    """
    writes all the information about the blasted genes to an output file

    :param table_dic: dic with gen-id as key and a list of homology group and
    genome number as values
    :param output_file: desired output location
    :param best_ara_hits: best hits in arabidopsis
    :param best_cau_hits: best hits in cauliflower
    :return:
    """
    # takes all the gen-id as list and puts them as value in a new dic
    data = {}
    data['Gen-id'] = list(table_dic.keys())
    group_numbers = []
    genomes = []
    start_pos = []
    end_pos = []

    # makes a list of homology group numbers and genome numbers in order of the
    # gen-ids
    for key in table_dic.keys():
        group_numbers.append(table_dic[key][0])
        genomes.append(table_dic[key][1])
        start_pos.append(table_dic[key][2])
        end_pos.append(table_dic[key][3])

    # extents the dic with the lists of hom group numbers and genome numbers
    data['Homology_group'] = group_numbers
    data['Genome_numbers'] = genomes
    data['start coordinate'] = start_pos
    data['end coordinate'] = end_pos

    # makes a pd.df from the dic
    df = pd.DataFrame(data)

    # find the best hits and identity percentage in arabidopsis and cauliflower
    # for every gen-id
    ara_hits, ara_percentages = hit_parser(best_ara_hits)
    cau_hits, cau_percentages = hit_parser(best_cau_hits)

    # extents the pd.df with the best hits and identity percentages
    df["Best Arabidopsis Thaliana hit"] = ara_hits
    df["% identity Arabidopsis Thaliana hit"] = ara_percentages

    # gets the full name from the gff file for every arabidopsis best hit
    full_names = []
    for hit in ara_hits:
        hit_search_term = hit.split('.')[0]
        full_names.append(get_description(hit_search_term))

    # extents the pd.df with the gene names and the cauliflower best hits + id
    df["full_name best hit Arabidopsis"] = full_names
    df["Best cauliflower hit"] = cau_hits
    df["% identity cauliflower hit"] = cau_percentages

    df.to_csv(output_file, sep='\t', index=False)


def change_notblasted(not_blasted):
    not_blasted_id_genomes = []
    for item in not_blasted:
        if "rna" in item:
            not_blasted_id_genomes.append(item+'_genome_1')
            continue
        elif "bro" in item:
            not_blasted_id_genomes.append(item+'_genome_2')
            continue
        elif "T02" in item:
            not_blasted_id_genomes.append(item+'_genome_3')
            continue
        elif "T07" in item:
            not_blasted_id_genomes.append(item+'_genome_4')
            continue
        elif "T13" in item:
            not_blasted_id_genomes.append(item+'_genome_5')
            continue
        elif "T06" in item:
            not_blasted_id_genomes.append(item+'_genome_6')
            continue
        elif "T24" in item:
            not_blasted_id_genomes.append(item+'_genome_7')
            continue
        elif "T19" in item:
            not_blasted_id_genomes.append(item+'_genome_8')
            continue
        elif "T12" in item:
            not_blasted_id_genomes.append(item + '_genome_9')
            continue
        elif "T10" in item:
            not_blasted_id_genomes.append(item+'_genome_10')
            continue
        elif "T08" in item:
            not_blasted_id_genomes.append(item+'_genome_11')
            continue
        elif "T17" in item:
            not_blasted_id_genomes.append(item+'_genome_12')
            continue
        elif "T21" in item:
            not_blasted_id_genomes.append(item+'_genome_13')
            continue
        elif "BolO_" in item:
            not_blasted_id_genomes.append(item+'_genome_14')
            continue
        elif "T22" in item:
            not_blasted_id_genomes.append(item+'_genome_15')
            continue
    return not_blasted_id_genomes


def main():
    pangenome_location = "pangenome_15_DB"
    protein_query = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/pangenome/AT5G10140_FLC_protein.faa"

    # blast_ID = do_pangenome_blast(pangenome_location, protein_query)
    blast_ID = ""

    # gets all the gen-ids+genome# which passed the blast
    blast_ids, df_filtered = extend_blast_list(blast_ID, pangenome_location)
    #queries_RBH = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/pangenome/queries_forRBHblast.fasta"

    hom_groups = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/panproteome/proteome_15_DB/pantools_homology_groups.txt"

    # gets a dic with gen-id as key and hom group as value also gets list of
    # all different group numbers from the blasted ids.
    blast_homgroups_dic, group_nums = check_hom_groups(hom_groups, blast_ids)

    # gets all the gen-id which are in the homology groups but were not blasted
    not_blasted = contamination(group_nums, blast_homgroups_dic, hom_groups)

    # make a dic with gen-id as key and list of hom group num and genome num
    # as values
    id_group_genome_num_dic = writer(blast_ids, blast_homgroups_dic, df_filtered)

    arabidopsis = "/home/perso009/lustre/cauliflower_restart/cauliflower/brassica_oleracea16/QC/proteins/Araport11_GFF3_genes_transposons.current.filtered.pep.faa"
    cauliflower_T22 = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/pangenome/pangenome_15_DB/proteins/proteins_15.fasta"

    # performs the blasts on arabidopsis and cauliflower (to get the best hit in
    # arabidopsis and cauliflower in the end)
    blast_hits_ara = "best_hits_ara.tsv"
    blast_hits_cau = "best_hits_cau.tsv"

    best_hit(blast_ids, arabidopsis, cauliflower_T22, blast_hits_ara, blast_hits_cau)

    output_path = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/variation_table.tsv"

    # collects all the desired information for every gen-id in a pd.df and
    # writes it to an output file
    output_writer(id_group_genome_num_dic, output_path, blast_hits_ara, blast_hits_cau)

    # same variation_table but then for the not blasted sequences
    not_blasted = change_notblasted(not_blasted)
    not_blast_homgroups_dic, group_nums = check_hom_groups(hom_groups, not_blasted)

    not_blasted_id_group_genome_num_dic = writer(not_blasted, not_blast_homgroups_dic, df_filtered)

    not_blast_hits_ara = "best_hits_ara_notblasted.tsv"
    not_blast_hits_cau = "best_hits_cau_notblasted.tsv"

    best_hit(not_blasted, arabidopsis, cauliflower_T22, not_blast_hits_ara, not_blast_hits_cau)

    output_notblasted_path = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/variation_table_not_blasted.tsv"

    output_writer(not_blasted_id_group_genome_num_dic, output_notblasted_path, not_blast_hits_ara,
                  not_blast_hits_cau)

if __name__ == '__main__':
    main()
