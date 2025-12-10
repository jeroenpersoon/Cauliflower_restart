#!/usr/bin/env python3
"""
Author: Jeroen Persoon
Description: makes a fasta file containing the protein sequences of the
gene-ids which are given as input file
Usage: python3 msa.py {pangenome location} {input_file}
The input file needs to have one gene-id per line
"""

from sys import argv
from pathlib import Path

def protein_file_number(gene_id, labels):
    """
    takes a gene-id to get the protein sequence from the pangenome

    :param gene_id: gene id of interest
    :param labels: file, having a unique part in the first colum and
    _genome_{genome number} in the second
    :return:
    """
    with open(labels, 'r') as labs:
        lines = labs.readlines()

    for line in lines:
        line = line.strip().split('\t')
        if line[0] in gene_id:
            gene_num = line[1]
            return gene_num.split('_')[-1]

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
    protein = protein.strip()

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

    # returns last header and sequence if the protein is in there
        if header and protein in header:

            return header, "".join(seq)

    # if not found return None
        return None, None


def make_seq_file(input_ids):
    """
    search the protein sequence in the protein file in question and writes
    it to another file to create a fasta file with it.

    :param input_ids:
    :return: writes sequences to output file
    """
    pangenome_location = Path(argv[1]).resolve()
    protein_folder = pangenome_location / "proteins"
    output = pangenome_location.parent / "msa_sequences.fasta"
    with open(output, 'w') as outf:
        with open(input_ids, 'r') as input:
            for gene in input:
                p_num = protein_file_number(gene)
                protein_file = f"{protein_folder}/proteins_{p_num}.fasta"
                header, seq = search_protein(protein_file, gene)
                outf.write(f"{header}\n{seq}\n")



def main():
    input_file = argv [2]
    make_seq_file(input_file)


if __name__ == '__main__':
    main()
