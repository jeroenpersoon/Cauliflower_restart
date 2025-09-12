#!/usr/bin/env python3
"""
Author: Jeroen Persoon
Description:
"""

import pandas as pd
from subprocess import run

def do_pangenome_blast(pangenome_path, query):
    # cmd = f"pantools blast {pangenome_path} {query}"
    cmd = ["pantools", "blast", pangenome_path, query]
    run(cmd, check=True)

    blast_results = "/home/perso009/lustre/cauliflower/T22species_oleracea15/pangenome/pangenome_15_DB/BLAST/blast_results.tsv"

    with open(blast_results) as f:
        f.readline()
        f.readline()
        columns = f.readline().strip()
    columns = list(columns.split('\t'))


    df = pd.read_csv(blast_results, sep='\t', skiprows=5, header=None, names=columns)

    df_filtered = df[(df["PASS minimum identity"] == "PASS") & (df["PASS minimum alignment length"] == "PASS")]

    blast_IDs = df_filtered["subject"].values.tolist()

    return blast_IDs


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

def get_query_seqs(blast_IDs_queries, queries_output):
    queries = {}
    for query in blast_IDs_queries:
        query_split = query.split("_genome_")
        queries[query_split[0]] = query_split[-1]

    protein_files_path = "/lustre/BIF/nobackup/perso009/cauliflower/T22species_oleracea15/pangenome/pangenome_15_DB/proteins"


    queries_file = []
    for item in queries.keys():
        path = f"{protein_files_path}/proteins_{queries[item]}.fasta"
        protein_ID = item
        f_header, prot_seq = search_protein(path, protein_ID)

        queries_file.append(f"{f_header}\n{prot_seq}\n")

    with open(queries_output, 'w') as outfile:
        for item in queries_file:
            outfile.write(item)

    return queries

def blast_queries_back(proteome, queries_seqs, query_genomes):

    mk_db_cmd = [ "makeblastdb", "-in", proteome, "-dbtype", "prot", "-out", "Araport11_prot_db"]
    run(mk_db_cmd, check=True)

    cmd = ["blastp", "-query", queries_seqs, "-db", "Araport11_prot_db", "-out", "blast_back_results.tsv", "-outfmt", "7"]
    run(cmd, check=True)

    blast_back_results = "/home/perso009/lustre/cauliflower/T22species_oleracea15/pangenome/blast_back_results.tsv"

    print(query_genomes)

    best_hits = {}
    with open(blast_back_results, 'r') as bbr:
        value = 4
        for i, line in enumerate(bbr):

            if i == value:
                to_add = line.split(" ")[1]
                continue

            elif i > value:

                if query_genomes[line.split("\t")[0]] in best_hits.keys():
                    best_hits[query_genomes[line.split("\t")[0]]].append(line)

                else:
                    best_hits[query_genomes[line.split("\t")[0]]] = [line]
                value += (int(to_add)+5)
                continue

        return best_hits


def write_best_hits(best_hits_dir, outputfile):
    with open(outputfile, 'w') as outfile:
        for key in best_hits_dir.keys():
            outfile.write(f"{key}\n")
            for item in best_hits_dir[key]:
                outfile.write(item)



def main():
    pangenome_location = "pangenome_15_DB"
    protein_query = "AT5G10140_FLC_protein.faa"

    blast_IDs = do_pangenome_blast(pangenome_location, protein_query)
    queries_RBH = "/home/perso009/lustre/cauliflower/T22species_oleracea15/pangenome/queries_forRBHblast.fasta"

    query_pergenome = get_query_seqs(blast_IDs, queries_RBH)

    Araport11 = "/home/perso009/lustre/cauliflower/T22species_oleracea15/pangenome/proteins_Araport11.fasta"
    best_hits_pergenome = blast_queries_back(Araport11, queries_RBH, query_pergenome)

    final_outfile = "/home/perso009/lustre/cauliflower/T22species_oleracea15/pangenome/best_hits_pergenome.txt"
    write_best_hits(best_hits_pergenome, final_outfile)

if __name__ == '__main__':
    main()