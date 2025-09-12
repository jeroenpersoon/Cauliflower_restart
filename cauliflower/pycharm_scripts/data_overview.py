#!/bin/bash

from pathlib import Path
def statistics(statistics_folder, output_file, overview_file):
    '''
    Goes through the statistics folder and collects the files to put the paths
    in separate lists.

    :param statistics_folder: path to the statistics folder created by the
    PanUtils QC pipeline
    :param output_file:
    :return: three lists with the paths to the raw and filtered statistics
    for genome, protein and annotation separately
    '''
    genomes, proteins, annotation = [], [], []
    folder = Path(statistics_folder)
    #goes through folder and takes all .tsv files
    for file in folder.glob("*.tsv"):
        split_stem = file.stem.split('_')
        #checks if the file has genome, protein or annotation at the beginning
        #of the name and puts it in de correct list.
        if split_stem[0] == "genome":
            genomes.append(file)
        elif split_stem[0] == "protein":
            proteins.append(file)
        elif split_stem[0] == "annotation":
            if split_stem[-1] != "statistics":
                annotation.append(file)
            else:
                continue

    #initializes the output file and writes the sample names as heading of the
    #columns in the first line
    with open(genomes[0], 'r') as infile:
        first_line = infile.readline()
    with open(output_file, 'w') as outfile:
        outfile.write(first_line)

    return genomes, proteins, annotation

def genome_protein_writer(files, output_file):
    '''
    Takes the line which begin with the strings in lines_wanted and writes
    the lines to the same output file initialized in the statistics function

    :param files: list with paths to statistics files
    :param output_file: .tsv file with the data overview
    :return: /
    '''
    lines_wanted = ["Number of sequences:", "Average sequence length:",
                    "Minimum sequence length:", "N50 sequence length:",
                    "N50 sequence index:", "N95 sequence length:",
                    "N95 sequence index:", "gene", "mRNA"]
    for file in files:
        with open(file, 'r') as fo:
            with open(output_file, 'a') as outfile:
                for line in fo:
                    if line.split('\t')[0] in lines_wanted:
                        outfile.write(line)

def add_stats(output_file):


def main():
    location = "/lustre/BIF/nobackup/perso009/cauliflower/cauliflower4/QC/statistics"
    output = "/lustre/BIF/nobackup/perso009/cauliflower/caulifloer4/QC/overview.tsv"
    data_overview = ""
    gen, pro, ann = statistics(location, output, data_overview)
    genome_protein_writer(gen, output)
    genome_protein_writer(ann, output)
    genome_protein_writer(pro, output)

    # busco_location =

if __name__ == '__main__':
    main()
