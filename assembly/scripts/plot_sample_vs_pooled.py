#!/usr/bin/enb python

import sys
import os
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patches as mpt
import pandas as pd
import seaborn as sns
import numpy as np

path = sys.argv[1]

files = os.listdir(path)

results = {}
dfs = []
for f in files:
    name = os.path.join(path, f)
    genome = f.rsplit("_",1)[0]
    sample = f.rsplit("_",1)[1][:-4] # remove tsv
    if genome not in results:
        results[genome] = {}
    with open(name, 'r') as summary:
        for line in summary:
            if line.startswith("assembler"):
                metrics = line.strip().split('\t')[1:]
            else:
                spl = line.strip().split('\t')
                assembler = spl[0]
                i = 1
                for metric in metrics:
                    if assembler not in results[genome]:
                        results[genome][assembler] = {}
                    if sample not in results[genome][assembler]:
                        results[genome][assembler][sample] = {}
                    results[genome][assembler][sample][metric] = float(spl[i])
                    i += 1

single_sample = {"sample_short_gsa" : "gsa", "MetaHipMer_short":"HipMer", "MetaHipMer2_short":"HipMer2", "metaSPAdes_short":"SPAdes", "Megahit_short":"MEGAHIT","OPERA-MS_hybrid":"OPERA-MS"}
pooled = {"pooled_short_gsa":"gsa", "MetaHipMer_short":"HipMer", "MetaHipMer2_short":"HipMer2", "metaSPAdes_short":"SPAdes", "Megahit_short":"MEGAHIT","OPERA-MS_hybrid":"OPERA-MS"}
xlabels = ['LjRoot109', 'LjRoot170', 'LjRoot28', '3934_BI']

metrics = ["Genome fraction (%)", "# misassemblies", "# mismatches per 100 kbp", "NGA50"]
vals_pooled = {metric:[] for metric in metrics}
vals_single = {metric:[] for metric in metrics}
for metric in metrics:
    i = 0
    j = 0
    for genome in xlabels:
        vals_single[metric].append([])
        vals_pooled[metric].append([])
        if genome == "LjRoot170":
            vals_single[metric].append([])
            vals_single[metric].append([])
        for assm in single_sample.keys():
            if genome == "LjRoot170":
                vals_single[metric][i].append(results[genome][assm]["sample2"][metric])
                vals_single[metric][i+1].append(results[genome][assm]["sample3"][metric])
                vals_single[metric][i+2].append(results[genome][assm]["sample4"][metric])
            elif genome == "3934_BI":
                vals_single[metric][i].append(results[genome][assm]["sample0"][metric])
            else:    
                vals_single[metric][i].append(results[genome][assm]["sample3"][metric])
        for assm in pooled.keys():
            vals_pooled[metric][j].append(results[genome][assm]["pooled"][metric])
        j += 1
        if genome == "LjRoot170": # three samples
            i += 3
        else:
            i += 1

colors_scatter = [sns.color_palette('colorblind')[x] for x in [2, 4, 5, 9, 7, 8]]

fig, axes = plt.subplots(2,2, sharex='col', figsize=(10,10))
xs_single = [0, 2, 2.8, 3.6, 5.6, 7.6]
xs_pooled = [0.8, 4.4, 6.4, 8.4]
k = 0
for ax_row in axes:
    for ax in ax_row:
        metric = metrics[k]
        ax.boxplot(vals_single[metric], positions = xs_single, patch_artist=True, boxprops=dict(facecolor=sns.color_palette('colorblind')[0]), showfliers=False, whis=0, zorder=1)
        ax.boxplot(vals_pooled[metric], positions = xs_pooled, patch_artist=True, boxprops=dict(facecolor=sns.color_palette('colorblind')[3]), showfliers=False, whis=0, zorder=1)
        ax.set_xlim(-0.5,9)
        ax.set_xticks([0.4,3.2,6,8])
        ax.set_xticklabels(['LjRoot109','LjRoot170','LjRoot28','3934_BI'])
        if metric == "NGA50":
            ax.set_yscale("log")
        ax.title.set_text(metric)
        i = 0
        for val in vals_single[metric]:
            sns.scatterplot(ax=ax,x=xs_single[i], y=val, c=colors_scatter, zorder=2)
            i += 1
        i = 0
        for val in vals_pooled[metric]:
            sns.scatterplot(ax=ax,x=xs_pooled[i], y=val, c=colors_scatter, zorder=2)
            i += 1

        if k == 2 or k == 3:
            ax2 = ax.twiny()
            ax2.set_xlim(-0.5,9)
            new_ticks = [x for x in xs_single]
            new_ticks.extend(xs_pooled)
            ax2.set_xticks(sorted(new_ticks))
            ljroot109 = ["8\n\n0.5", "131\n\n86"]
            ljroot170 = ["8\n\n0"," 8\n\n1"," 8\n\n2", "101\n\n85"]
            ljroot28 = ["0.5\n\n0", "8\n\n0"]
            BI_3934 = ["8\n\n0", "8\n\n0"]
            ax2.xaxis.set_ticks_position("bottom")
            ax2.xaxis.set_label_position("bottom")
            ax2.spines["bottom"].set_position(("axes", -0.1))
            ax2.set_frame_on(True)
            ax2.patch.set_visible(False)
            for sp in ax2.spines.values():
                sp.set_visible(False)
            ax2.spines["bottom"].set_visible(True)
            ax2.set_xticklabels([x for slist in [ljroot109, ljroot170, ljroot28, BI_3934] for x in slist])
        k += 1

legend2 = [Line2D([0], [0], color=x, marker="o", linestyle='None', label=y) for x,y in zip(colors_scatter,single_sample.values())]
plt.legend(handles = legend2, bbox_to_anchor=(1.04,1), loc='center left')
fig.savefig("Coassembly.png", bbox_inches='tight')
