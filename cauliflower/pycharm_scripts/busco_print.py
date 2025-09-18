#!/bin/bash

from pathlib import Path

def print_files(folder, proteomes, outputfile):
    with open(outputfile, 'w') as of:
        for file in Path(folder).glob('*.txt'):
            with open(proteomes, 'r') as proteomes_num:
                prot_lines = proteomes_num.readlines()
                with open(file, 'r') as summaries:
                    for line in prot_lines:
                        if line.split(',')[0] == file.stem.split('.')[-1]:
                            of.write(line.split('/')[-1])
                            break
                    lines = summaries.readlines()
                    write_lines = [lines[9], lines[10], lines[11], lines[12], lines[7]]
                    of.writelines(write_lines)

def main():
    busco_location = "/home/perso009/lustre/cauliflower/brassica_all/panproteome/proteome_DB/busco/brassicales_odb10/protein/BUSCO_summary_files"
    proteome_numbers = "/home/perso009/lustre/cauliflower/brassica_all/panproteome/proteome_DB/databases/proteomes.txt"
    output = "/lustre/BIF/nobackup/perso009/cauliflower/brassica_all/QC/busco_summ_overview.tsv"

    print_files(busco_location, proteome_numbers, output)


if __name__ == '__main__':
    main()