#!/usr/bin/env python3

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

def create_heatmap(distances, outputfig):
    data = pd.read_csv(distances, sep='\t', header=None, names=["Accession 1", "Accession 2", "Distance"])
    data_matrix = data.pivot(index="Accession 1", columns="Accession 2", values="Distance")
    data_sym = data_matrix.combine_first(data_matrix.T)
    for accession in data_sym.index:
        data_sym.loc[accession, accession] = 0.0

    plt.figure(figsize=(10,10))
    sns.heatmap(data_sym)
    plt.title("Distance matrix Cauliflower")
    plt.tight_layout()
    plt.savefig(outputfig, dpi=500)
    plt.close()


def main():
    distances = "/home/perso009/lustre/cauliflower/cauliflower4/mash/distances.txt"
    output = "/home/perso009/lustre/cauliflower/cauliflower4/mash/distance_heatmap.png"
    create_heatmap(distances, output)


if __name__ == '__main__':
    main()