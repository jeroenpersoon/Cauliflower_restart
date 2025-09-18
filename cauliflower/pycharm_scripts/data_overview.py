#!/bin/bash
"""
Author: Jeroen Persoon
Description:
Usage:
"""

from pathlib import Path
import pandas as pd

def statistics(statistics_folder, output_file):
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
        names = first_line.split('\t')

    #so form the genome_content_raw.tsv the sample names were extracted.
    #these names were split on a dot and only the first part will be taken
    #as sample name.
        line = []
        for elem in names:
            if elem[:3] == "Bol" or elem[:3] == "OX_":
                line.append(elem.split('.')[0].split('_')[0])
            else:
                line.append(elem.split('.')[0])

        line = '\t'.join(line)
        outfile.write(line+'\tFrom file:\n')
    return genomes, proteins, sorted(annotation, reverse = True)

# def start_outfile(samples_overview, output_file):
#     names = {}
#     df = pd.read_csv(samples_overview, sep='\t', header=0)
#     sample_names = dict(zip(df["FASTA"].apply(lambda x: x.split('/')[-1]),
#                     df["FASTA"]))
#     print(sample_names)
#     sample_names = dict(sorted(sample_names.items()))
#     print(sample_names)
#     with open(output_file, 'w') as outfile:
#         outfile.write("test")

def genome_protein_writer(files, output_file):
    '''
    Takes the line which begin with the strings in lines_wanted and writes
    the lines to the same output file initialized in the statistics function

    :param files: list with paths to statistics files
    :param output_file: .tsv file with the data overview
    :return: /
    '''
    lines_unwanted = ["N25 sequence length:",
                    "N25 sequence index:", "N75 sequence length:",
                    "N75 sequence index:", ""]
    #goes through every file in the list with file paths.
    for file in files:
        with open(file, 'r') as fo:
            with open(output_file, 'a') as outfile:
                #goes over every line in the file and ignores the rows
                #which we do not want to print to our output file, print
                #the lines which we do want in the output file
                for line in fo:
                    if line.split('\t')[0] not in lines_unwanted:
                        outfile.write(f"{line.strip('\n')}\t{file.name}\n")


def get_busco_scores(file_numbers, summary_folder):
    """
    make a dictionary with the accessions ID (.fna) as keys and a list
    containing the amount of busco's and the percentages for
    single, duplicated, fragmented and missing busco's

    :param file_numbers: the proteomes.txt file which is made when running
    busco containing the protein number and the path to the original protein
    file
    :param summary_folder: BUSCO_summary_files folder created by busco function
    :return: the dictionary containing accession ID and busco results.
    """
    proteomes = {}
    #goes through the proteomes.txt file and only takes the lines starting with
    #a number. Extract from the filepath to the filtered .faa file the
    #accession ID. puts the number as key and the accession ID (name) as value
    with open(file_numbers, 'r') as openfn:
        for line in openfn:
            if line.split(',')[0].isdigit():
                proteomes[line.split(',')[0]] = [line.split('/')[-1].split('.')[0]]

    #goes through all the summary files, extends accession ID in the list
    #with the busco results.
    for file in Path(summary_folder).glob("*.txt"):
        with open(file, 'r') as summaries:
            lines = summaries.readlines()
            key = file.stem.split('.')[-1]
            proteomes[key].append(''.join(lines[9].strip()))
            proteomes[key].append(''.join(lines[10].strip()))
            proteomes[key].append(''.join(lines[11].strip()))
            proteomes[key].append(''.join(lines[12].strip()))
            proteomes[key].append(''.join(lines[7].strip()))

    #makes a new dictionary with the accession ID as key and the busco results
    #as value. Also adds .fna to the key to make it match the headers of the
    #output file later.
    new_keys = []
    new_values = []
    new_proteomes = {}
    for key in proteomes.keys():
        if proteomes[key][0][:3] == "Bol" or proteomes[key][0][:3] == "OX_":
            new_keys.append(proteomes[key][0].split('_')[0])
        else:
            new_keys.append(proteomes[key][0])
        new_values.append(proteomes[key][1:])

    for i in range(len(new_keys)):
        new_proteomes[new_keys[i]] = new_values[i]


    #rename new_proteomes
    return new_proteomes


def write_busco_scores(outputfile, busco_scores, accessions_info):
    """
    Writes the busco amounts and percentages results to the output file

    :param outputfile: path to output file
    :param busco_scores: dictionary with busco results made by get_busco_scores
    function
    :return: /
    """

    wanted_lines = ['Complete and single-copy BUSCOs (S)', 'Complete and duplicated BUSCOs (D)',
                    'Fragmented BUSCOs (F)', 'Missing BUSCOs (M)']

    #Goes over all the headings of the output file and see if they match with
    #the key in the dictionary with the busco scores. If so extends the items
    #in the wanted_lines list with the numbers accordingly.
    outf = pd.read_csv(outputfile, sep='\t', header=0)
    for name in outf.columns:
        for i in busco_scores:
            if name == i:
                for nr, item in enumerate(wanted_lines):
                    wanted_lines[nr] += f"\t{busco_scores[name][nr].split('\t')[0]}"

    wanted_percentages = ['Complete and single-copy BUSCOs (S) %',
                          'Complete and duplicated BUSCOs (D) %',
                          'Fragmented BUSCOs (F) %', 'Missing BUSCOs (M) %']

    #same principle as above. Take the string with the busco % from the
    #busco scores dictionary and extents the wanted_percentages list.
    for col in outf.columns:
        for key in busco_scores:
            if key == col:
                percentages = (busco_scores[key][-1].split('%')[1:-1])
                for i, line in enumerate(wanted_percentages):
                    wanted_percentages[i] += f"\t{percentages[i].split(':')[1]}"

    #prints every string in the wanted_lines and wanted_percentage list with a
    #newline after each string
    with open(outputfile, 'a') as outfile:
        for line in wanted_lines:
            outfile.write(line + '\n')

        for perc in wanted_percentages:
            outfile.write(perc+'\n')

    with open(accessions_info, 'r') as acc_info:
        varieties = {}
        accf = pd.read_csv(acc_info, sep='\t', header=0)
        for entry in accf['FASTA']:
            for key in busco_scores.keys():
                if entry.split('/')[-1].split('.')[0] == key:
                    varieties[key] = accf[accf['FASTA'] == entry]['Species'].tolist()
                    varieties[key].append(accf[accf['FASTA'] == entry]['Variety'].item())
                # else:
                #     varieties[key] = ['\t']
                #     varieties[key].append('\t')
    varieties['27622715'] = ['oleracea', 'botrytis']
    varieties['Bnigra_C2'] = ['nigra', float('nan')]
    varieties['OX'] = ['oleracea', 'capitata']

    print(varieties)
    var_line=[]
    spe_line=[]
    for col in outf.columns:
        for key in varieties.keys():
            if key == col:
                spe_line.append(f"{varieties[key][0]}\t")
                var_line.append(f"{varieties[key][1]}\t")

    print(''.join(spe_line))
    print(var_line)
    # with open(outputfile, 'r') as outfile:
    #     lines = outfile.readlines()
    # lines[1:1] = ''.join(spe_line)
    # # lines[3:3] = ''.join(var_line)


    with open(outputfile, 'a') as of:
        of.write(f"Species\t{''.join(spe_line)}\n")
        of.write(f"Variety\t{''.join(var_line)}")


def main():
    location = "/lustre/BIF/nobackup/perso009/cauliflower/brassica_all/QC/statistics"
    output = "/lustre/BIF/nobackup/perso009/cauliflower/brassica_all/QC/overview.tsv"
    data_overview = "/home/perso009/lustre/cauliflower/brassica_all/QC/statistics/Brassica_data_availability.tsv"
    gen, pro, ann = statistics(location, output)
    # start_outfile(data_overview, output)
    genome_protein_writer(gen, output)
    genome_protein_writer(ann, output)
    genome_protein_writer(pro, output)

    proteome_numbers = "/home/perso009/lustre/cauliflower/brassica_all/panproteome/proteome_DB/databases/proteomes.txt"
    busco_location = "/home/perso009/lustre/cauliflower/brassica_all/panproteome/proteome_DB/busco/brassicales_odb10/protein/BUSCO_summary_files"
    busco_results = get_busco_scores(proteome_numbers, busco_location)

    write_busco_scores(output, busco_results, data_overview)

    # write_species_info(output, data_overview)

    #tot test on cauliflower4
    # test_location = "/lustre/BIF/nobackup/perso009/cauliflower/cauliflower4/QC/statistics"
    # test_output = "/lustre/BIF/nobackup/perso009/cauliflower/cauliflower4/QC/overview.tsv"
    # test_proteome_numbers = "/home/perso009/lustre/cauliflower/cauliflower4/panproteome/proteome_DB_5/databases/proteomes.txt"
    # test_busco_location = "/home/perso009/lustre/cauliflower/cauliflower4/panproteome/proteome_DB_5/busco/brassicales_odb10/protein/BUSCO_summary_files"
    # gen, pro, ann = statistics(test_location, test_output)
    # print(statistics(test_location, test_output))
    # # start_outfile(data_overview, output)
    # genome_protein_writer(gen, test_output)
    # genome_protein_writer(ann, test_output)
    # genome_protein_writer(pro, test_output)
    # busco_results = get_busco_scores(test_proteome_numbers, test_busco_location)
    #
    # write_busco_scores(test_output, busco_results)


if __name__ == '__main__':
    main()
