#!/usr/bin/env python

import sys
import argparse
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd
import numpy as np
import seaborn as sns
import math

parser = argparse.ArgumentParser()
parser.add_argument("-files", type=argparse.FileType('r'), nargs='+')
# Here we don't need scales and will do the scaling ourselves!
# multiple files, these will get merged via their assemblers
parser.add_argument("-o", type=str, help="out folder")
# one file/plot per metric is created
args = parser.parse_args()

subsets = []
dfs = []
for f in args.files:
    filename = f.name
    typ = f.name.split("/")[-1].split(".")[0]
    subsets.append(typ)
    df = pd.read_csv(f, sep='\t', header=0)
    df['type'] = typ
    dfs.append(df)

dfs = pd.concat(dfs)
pairs = [("Strain recall", "Strain precision"),("NGA50", "# misassemblies"),("Genome fraction (%)","# mismatches per 100 kbp")]

fig, axes = plt.subplots(2,2)
i = 0
j = 0
for pair in pairs:
    sns.scatterplot(ax = axes[i,j], data=dfs,x=pair[0],y=pair[1], hue="assembler",style="type",)
    if pair[0] == "NGA50":
        axes[i,j].set_xscale('log')
        axes[i,j].invert_yaxis()
    else:
        axes[i,j].xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        if pair[1] == "Strain precision":
            axes[i,j].yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        else:
            axes[i,j].invert_yaxis()
    axes[i,j].legend([],[], frameon=False)
    i += 1
    if i == 2:
        i = 0
        j = 1

handles, labels = axes[0,0].get_legend_handles_labels()
axes[1,1].axis('off')
fig.legend(handles, labels, loc='lower right')
plt.show()
