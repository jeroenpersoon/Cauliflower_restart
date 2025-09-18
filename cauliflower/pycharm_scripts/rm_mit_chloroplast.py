#!/bin/bash
"""
Author: Jeroen Persoon
Description: Removes the last sequence from a FASTA file based on the header
"""

def rm_MT_C(file, header):
    '''
    checks if there are sequences shorter than 49 characters in a file in
    FASTA format.

    :param file: path to the FASTA file
    :param header: header of the sequence which need to be removed as string
    :return: dictionary with the FASTA headers as key and the sequence, if
    shorter than 49 characters, as value.
    '''
    new_lines = []
    #opens file and goes through it line by line
    with open(file, 'r') as f:
        lines = f.readlines()

        for line in lines:

            #if header is found stops going over the lines
            if line.startswith(header):
                print('found it!')
                break

            else:
                #if header is not found appends the list new_lines with the line
                new_lines.append(line)

    #writes every line up until the header of interest (which is excluded)
    with open(file, 'w') as fo:
        fo.writelines(new_lines)


def main():
    #file paths
    dummy = "/home/perso009/lustre/cauliflower/brassica_all/QC/proteins/dummy.txt"
    BOL = "/home/perso009/lustre/cauliflower/brassica_oleracea15/genomes/GCF_000695525.1_BOL_genomic.fna"
    remove_header_BOL = ">NC_016118.1 Brassica oleracea mitochondrion, complete genome"

    remove_header_CAAS = ">NC_015139.1 Brassica rapa subsp. pekinensis chloroplast, complete genome"
    CAAS = "/home/perso009/lustre/cauliflower/genus_diploid8/genomes/GCF_000309985.2_CAAS_Brap_v3.01_genomic.fna"

    araport11 = "/home/perso009/lustre/cauliflower/araport11/genomes/GCF_000001735.4_TAIR10.1_genomic.fna"

    #sequence header to be removed
    sequence_header = '>NC_037304.1 Arabidopsis thaliana ecotype Col-0 mitochondrion, complete genome'

    rm_MT_C(araport11, sequence_header)

if __name__ == '__main__':
    main()
