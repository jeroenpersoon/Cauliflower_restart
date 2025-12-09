#!/bin/bash
"""
Author: Jeroen Persoon
Description: To validate if two FASTA files are identical. Was intended to
test if modifying a FASTA file with seqtk would change the information in the
FASTA file.
"""

def parser(file_name):
    '''
    Makes a list with the sequence header as string followed by the sequence
    itself as string. This for all the header-sequences there are

    :param file_name: Name of the Fasta file you wish to compare
    :return: list of strings containing header - sequence in order
    '''
    file = open(file_name, "r").read()
    seqs = []
    seq = []
    #goes over the lines and appends the list with the header name if it found
    #one or appends the sequence string if it did not found a new header
    for line in file.split("\n"):
        if line.startswith(">"):
            seqs.append("".join(seq))
            seq = []
            seqs.append(line)
        else:
            seq.append(line)
    #appends the last sequences string with the end of the last sequence
    seqs.append("".join(seq))

    #leaves out the first empty string
    return seqs[1:]

def seq_lengths(seqs1, seqs2):
    '''
    Checks if the length of the header and the sequence are the same

    :param seqs1: list of headers and sequence as strings in order
    :param seqs2: list of headers and sequence as strings in order
    :return: prints True of False
    '''

    #print True if strings in the lists have the same length
    for i in range((len(seqs1))):
        print(len(seqs1[i]) == len(seqs2[i]))
        if not seqs1[i] == seqs2[i]:
            print(seqs1[i])
            print(seqs2[i])
def amount_seqs(seqs):
    '''
    Counts the amount of headers

    :param seqs: list of headers and sequence as strings in order
    :return: number of headers
    '''

    count = 0
    for line in seqs:
        if line.startswith(">"):
            count += 1

    return count

def begin_end(seqs1, seqs2):
    '''
    Checks if first and last 200 nucleotides are identical

    :param seqs1: list of headers and sequence as strings in order
    :param seqs2: list of headers and sequence as strings in order
    :return:
    '''


    for seq in range(len(seqs1)):
        if not seqs1[seq].startswith(">"):

            #if string is not a header takes the first and last 200 nucleotides

            begin_seq1 = seqs1[seq][:200]
            end_seq1 = seqs1[seq][-200:]

            #also take first and last 200 nucleotides of the string from file 2
            begin_seq2 = seqs2[seq][:200]
            end_seq2 = seqs2[seq][-200:]

            #prints True if those 200 nucleotides are the same
            print("are first 200 nucl. the same", begin_seq1 == begin_seq2)
            print(begin_seq1)
            print(begin_seq2)

            print("are last 200 nucl. the same", end_seq1 == end_seq2)
            print(end_seq1)
            print(end_seq2)

        else:
            #if string is a header sets begin and end to 1 and 2 to prevent that
            #the same strings are going to be checked multiple times
            begin_seq1, end_seq1 = "1", "1"
            begin_seq2, end_seq2 = "2", "2"

def main():
    #dummy files
    #dfile1 = '/home/perso009/lustre/cauliflower/brassica_all/QC/proteins/dummy.txt'
    #dfile2 = '/home/perso009/lustre/cauliflower/brassica_all/QC/proteins/dummy.txt'

    #real examples
    file1 = "/home/perso009/lustre/cauliflower/cauliflower4/QC/genomes_filtered/GWHDUBS00000000.genome.filtered.fna"
    file2 = "/home/perso009/lustre/cauliflower/cauliflower4/QC/genomes_filtered/GWHDUBS00000000.genome.filtered.fna"

    # new Korso annotation sequence files
    Korso1 = "/home/perso009/lustre/cauliflower/T22panproteome/genomes/T22.chr.fna"
    Korso2 = "/home/perso009/lustre/cauliflower/T22panproteome/genomes/T22_wrapped.fna"
    orginal_Korso = "/home/perso009/lustre/cauliflower/cauliflower4/genomes/27622715.fna"


    seqs1 = parser(orginal_Korso)
    seqs2 = parser(Korso2)

    print("Test if sequence lengths are the same (incl. length of headers)")
    seq_lengths(seqs1,seqs2)

    print("\nTest if amount of sequences are the same")
    print(amount_seqs(seqs1), amount_seqs(seqs2))

    print("\nTest is first and last 200 nucleotides are the same")
    begin_end(seqs1,seqs2)

if __name__ == '__main__':
    main()
