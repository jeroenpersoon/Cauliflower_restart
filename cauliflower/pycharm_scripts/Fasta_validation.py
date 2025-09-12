#!/bin/bash
import itertools
from sys import argv

def parser(file_name):
    file = open(file_name, "r").read()
    seqs = []
    seq = []
    for line in file.split("\n"):
        if line.startswith(">"):
            seqs.append("".join(seq))
            seq = []
            seqs.append(line)
        else:
            seq.append(line)
    seqs.append("".join(seq))
    return seqs[1:]

def seq_lengths(seqs1, seqs2):
    for i in range((len(seqs1))):
        print(len(seqs1[i]) == len(seqs2[i]))

def amount_seqs(seqs):
    count = 0
    for line in seqs:
        if line.startswith(">"):
            count += 1
    return count

def begin_end(seqs1, seqs2):
    for seq in range(len(seqs1)):
        if not seqs1[seq].startswith(">"):
            begin_seq1 = seqs1[seq][:200]
            end_seq1 = seqs1[seq][-200:]
            begin_seq2 = seqs2[seq][:200]
            end_seq2 = seqs2[seq][-200:]
            print("are first 200 nucl. the same", begin_seq1 == begin_seq2)
            print(begin_seq1)
            print(begin_seq2)

            print("are last 200 nucl. the same", end_seq1 == end_seq2)
            print(end_seq1)
            print(end_seq2)

        else:
            begin_seq1, end_seq1 = "1", "1"
            begin_seq2, end_seq2 = "2", "2"

def main():
    file1 = argv[1]
    file2 = argv[2]
    seqs1 = parser(file1)
    seqs2 = parser(file2)
    print("Test if sequence lengths are the same (incl. length of headers)")
    seq_lengths(seqs1,seqs2)
    print("\nTest if amount of sequences are the same")
    print(amount_seqs(seqs1), amount_seqs(seqs2))
    print("\nTest is first and last 200 nucleotides are the same")
    begin_end(seqs1,seqs2)

if __name__ == '__main__':
    main()
