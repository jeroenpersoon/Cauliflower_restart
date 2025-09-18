#!/usr/bin/env python3
"""
Author: Jeroen Persoon
Description:
"""

import pandas as pd
from subprocess import run

def do_pangenome_blast(pangenome_path, query):
    cmd = ["pantools", "blast", pangenome_path, query]
    run(cmd, check=True)

    blast_results = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/pangenome/pangenome_15_DB/BLAST/blast_results.tsv"

    with open(blast_results) as f:
        f.readline()
        f.readline()
        columns = f.readline().strip()
    columns = list(columns.split('\t'))


    df = pd.read_csv(blast_results, sep='\t', skiprows=5, header=None, names=columns)

    df_filtered = df[(df["PASS minimum identity"] == "PASS") & (df["PASS minimum alignment length"] == "PASS")]

    cp_cmd = ["cp", blast_results, "blast_results_AT.tsv"]
    run(cp_cmd, check=True)

    blast_ID = df_filtered["subject"].iloc()[0]

    blast_IDs = df_filtered["subject"].values.tolist()
    blast_IDs = list(set(blast_IDs))
    print(len(blast_IDs))

    return blast_ID


def search_protein(fasta_file, protein):
    header = None
    seq = []

    with open(fasta_file, 'r') as f:

        for line in f:
            line = line.strip()
            if line.startswith('>'):

                if header and protein in header:
                    return header, "".join(seq)
                else:
                    header = line
                    seq = []

            else:
                seq.append(line)

        if header and protein in header:

            return header, "".join(seq)

        return None, None


def extend_blast_list(best_ID, pangenome_path):
    ID, genome_num = best_ID.split('_genome_')

    protein_files_path = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/pangenome/pangenome_15_DB/proteins"

    protein_file = f"{protein_files_path}/proteins_{genome_num}.fasta"
    header, seq = search_protein(protein_file, ID)

    query_file = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/pangenome/best_blast_query.fasta"

    with open(query_file, 'w') as seqfile:
        seqfile.write(f"{header}\n{seq}")

    cmd = ["pantools", "blast", pangenome_path, query_file]
    run(cmd, check=True)

    blast_results = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/pangenome/pangenome_15_DB/BLAST/blast_results.tsv"

    # blast_results = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/pangenome/blast_results_AT.tsv"

    with open(blast_results, 'r') as f:
        f.readline()
        f.readline()
        columns = f.readline().strip()
    columns = list(columns.split('\t'))

    df = pd.read_csv(blast_results, sep='\t', skiprows=5, header=None,
                     names=columns)

    df_filtered = df[(df["PASS minimum identity"] == "PASS") & (
                df["PASS minimum alignment length"] == "PASS")]

    blast_IDs = df_filtered["subject"].values.tolist()
    blast_IDs = list(set(blast_IDs))
    print(len(blast_IDs))

    return blast_IDs


def check_hom_groups(grouping_file, best_IDs):
    blasted_ids = []

    search_terms = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/pangenome/search_terms.txt"
    with open(search_terms, 'w') as term_file:
        for item in best_IDs:
            id = item.split('_genome_')[0]
            # cmd.append(id)
            # cmd.append('-e')
            blasted_ids.append(id)
            term_file.write(id+'\n')

    id_dic = {}
    with open(search_terms, 'r') as terms:
        for line in terms:
            line = line.strip()
            cmd = ['grep', f'{line}', grouping_file]
            result = run(cmd, capture_output=True, text=True, check=True)
            id_dic[line] = result.stdout.split(': ')[0]

    all_groups = list(set(id_dic.values()))

    return id_dic, all_groups

def contamination(group_numbers, group_num_per_id, grouping_file):
    ids_in_groups = []
    for num in group_numbers:
        cmd = ['grep', num, grouping_file]
        result = run(cmd, capture_output=True, text=True, check=True)
        result = result.stdout.split(': ')[1]
        ids = result.strip().split(' ')
        for id in ids:
            ids_in_groups.append(id.split('#')[0])


    for key in group_num_per_id.keys():
        if key in ids_in_groups:
            ids_in_groups.remove(key)


    return ids_in_groups

def writer(id_genome_num, id_group_num):
    i = 0
    for key in id_group_num.keys():
        value = [id_group_num[key], id_genome_num[i].split('_genome_')[1]]
        id_group_num[key] = value
        i += 1

    return id_group_num


# def get_query_seqs(blast_IDs_queries, queries_output):
#     queries = {}
#     for query in blast_IDs_queries:
#         query_split = query.split("_genome_")
#         queries[query_split[0]] = query_split[-1]
#
#     protein_files_path = "/lustre/BIF/nobackup/perso009/cauliflower/T22species_oleracea15/pangenome/pangenome_15_DB/proteins"
#
#
#     queries_file = []
#     for item in queries.keys():
#         path = f"{protein_files_path}/proteins_{queries[item]}.fasta"
#         protein_ID = item
#         f_header, prot_seq = search_protein(path, protein_ID)
#
#         queries_file.append(f"{f_header}\n{prot_seq}\n")
#
#     with open(queries_output, 'w') as outfile:
#         for item in queries_file:
#             outfile.write(item)
#
#     return queries
#
# def blast_queries_back(proteome, queries_seqs, query_genomes):
#
#     mk_db_cmd = [ "makeblastdb", "-in", proteome, "-dbtype", "prot", "-out", "Araport11_prot_db"]
#     run(mk_db_cmd, check=True)
#
#     cmd = ["blastp", "-query", queries_seqs, "-db", "Araport11_prot_db", "-out", "blast_back_results.tsv", "-outfmt", "7"]
#     run(cmd, check=True)
#
#     blast_back_results = "/home/perso009/lustre/cauliflower/T22species_oleracea15/pangenome/blast_back_results.tsv"
#
#     print(query_genomes)
#
#     best_hits = {}
#     with open(blast_back_results, 'r') as bbr:
#         value = 4
#         for i, line in enumerate(bbr):
#
#             if i == value:
#                 to_add = line.split(" ")[1]
#                 continue
#
#             elif i > value:
#
#                 if query_genomes[line.split("\t")[0]] in best_hits.keys():
#                     best_hits[query_genomes[line.split("\t")[0]]].append(line)
#
#                 else:
#                     best_hits[query_genomes[line.split("\t")[0]]] = [line]
#                 value += (int(to_add)+5)
#                 continue
#
#         return best_hits
#
#
# def write_best_hits(best_hits_dir, outputfile):
#     with open(outputfile, 'w') as outfile:
#         for key in best_hits_dir.keys():
#             outfile.write(f"{key}\n")
#             for item in best_hits_dir[key]:
#                 outfile.write(item)



def main():
    pangenome_location = "pangenome_15_DB"
    protein_query = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/pangenome/AT5G10140_FLC_protein.faa"

    blast_ID = do_pangenome_blast(pangenome_location, protein_query)
    # blast_ID = ""

    blast_ids = extend_blast_list(blast_ID, pangenome_location)
    queries_RBH = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/pangenome/queries_forRBHblast.fasta"

    hom_groups = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/panproteome/proteome_15_DB/pantools_homology_groups.txt"

    # blast_hom_groups, group_nums = check_hom_groups(hom_groups, blast_ids)
    #
    # print(blast_ids)
    # print(blast_hom_groups)
    #
    # not_blasted = contamination(group_nums, blast_hom_groups, hom_groups)
    #
    # table_dic = writer(blast_ids, blast_hom_groups)

    # query_pergenome = get_query_seqs(blast_IDs, queries_RBH)
    #
    # Araport11 = "/home/perso009/lustre/cauliflower/T22species_oleracea15/pangenome/proteins_Araport11.fasta"
    # best_hits_pergenome = blast_queries_back(Araport11, queries_RBH, query_pergenome)
    #
    # final_outfile = "/home/perso009/lustre/cauliflower/T22species_oleracea15/pangenome/best_hits_pergenome.txt"
    # write_best_hits(best_hits_pergenome, final_outfile)

if __name__ == '__main__':
    main()