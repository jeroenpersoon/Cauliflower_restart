#!/bin/bash

def find_mini(file):
    '''
    checks if there are sequences shorter than 49 characters in a file in
    FASTA format.

    :param file: path to the FASTA file
    :return: dictionary with the FASTA headers as key and the sequence, if
    shorter than 49 characters, as value.
    '''
    seq_dic = {}
    seqs = []
    key = None
    #opens file and goes through it line by line
    with open(file, 'r') as fo:
        for line in fo:
            if line.startswith('>'):
                #if line is the first header checks if sequence is shorter than
                #49 if so puts it in the dictionary otherwise puts the next
                #header as new key
                if key:
                    if len(seqs[0]) < 49:
                        seq_dic[key] = seqs
                        #empties seqs list after sequence is added to dictionary
                        seqs = []
                    else:
                        #also empties seqs list if sequence is longer than 49
                        seqs = []
                key = line
            else:
                #if line is not a header extents the seqs list with the line
                #and makes it one single string
                seqs.append(line.strip('\n'))
                seqs = [''.join(seqs)]
    #if last sequence is shorter than 49 adds it to the dictionary
    if len(seqs[0]) < 49:
        seq_dic[key] = seqs

    return seq_dic

def main():
    #file paths
    CAAS = "/home/perso009/lustre/cauliflower/brassica_all/QC/proteins/GCF_000309985.2_CAAS_Brap_v3.01_genomic.filtered.pep.faa"
    BOL = "/home/perso009/lustre/cauliflower/brassica_all/QC/proteins/GCF_000695525.1_BOL_genomic.filtered.pep.faa"
    Da_Ae = "/home/perso009/lustre/cauliflower/brassica_all/QC/proteins/GCF_020379485.1_Da-Ae_genomic.filtered.pep.faa"
    dummy = "/home/perso009/lustre/cauliflower/brassica_all/QC/proteins/dummy.txt"

    #prints dictionaries with sequences shoter than 49
    print("sequences with a length shorter than 49 aa")
    print("CAAS protein file")
    print(find_mini(CAAS))
    print("BOL protein file")
    print(find_mini(BOL))
    print("Da-Ae protein file")
    print(find_mini(Da_Ae))

if __name__ == '__main__':
    main()
