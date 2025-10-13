#!/usr/bin/env python3
"""
Author: Jeroen Persoon
Description: makes a fasta file containing the protein sequences of the
gene-ids which are given as input file
Usage: python3 msa.py {input_file}
The input file needs to have one gene-id per line
"""

from sys import argv

def protein_file_number(gen_id):
    """
    based on the gene-id returns the protein number to find the right protein
    file

    :param gen_id: string of the gene-id of interest
    :return: string of number of the protein file in question
    """

    if "rna" in gen_id:
        return '1'
    elif "bro" in gen_id:
        return '2'
    elif "T02" in gen_id:
        return '3'
    elif "T07" in gen_id:
        return '4'
    elif "T13" in gen_id:
        return '5'
    elif "T06" in gen_id:
        return '6'
    elif "T24" in gen_id:
        return '7'
    elif "T19" in gen_id:
        return '8'
    elif "T12" in gen_id:
        return '9'
    elif "T10" in gen_id:
        return '10'
    elif "T08" in gen_id:
        return '11'
    elif "T17" in gen_id:
        return '12'
    elif "T21" in gen_id:
        return '13'
    elif "BolO_" in gen_id:
        return '14'
    elif "T22" in gen_id:
        return '15'
    else:
        return None

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
    :return:
    """
    protein_folder = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/pangenome/pangenome_15_DB/proteins"
    output = "/home/perso009/lustre/cauliflower_restart/cauliflower/T22species_oleracea15/msa_seqs.fasta"
    with open(output, 'w') as outf:
        with open(input_ids, 'r') as input:
            for gene in input:
                p_num = protein_file_number(gene)
                protein_file = f"{protein_folder}/proteins_{p_num}.fasta"
                header, seq = search_protein(protein_file, gene)
                outf.write(f"{header}\n{seq}\n")



def main():
    input_file = argv [1]
    make_seq_file(input_file)


if __name__ == '__main__':
    main()
