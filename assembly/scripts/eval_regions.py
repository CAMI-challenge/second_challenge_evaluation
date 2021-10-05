#!/usr/bin/env python

import sys
import os
import statistics
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np

paf = sys.argv[1]

max_diff = 0.
assemblers = {}
files = os.listdir(paf)
for f in files:
    if f.endswith("paf"):
        paff = os.path.join(paf, f)
    else:
        continue
    frags = []
    cigs = []
    diffs = []
    c_lengths = []
    length = 0
    cont = False
    assembler = f[:f.find("Otu") - 1]
    with open(paff, 'r') as p:
        for line in p:
            spl = line.strip().split('\t')
            length = spl[1]
            c_lengths.append(int(spl[6]))
            for elem in spl:
                if elem.startswith("cg:"): #CIGAR
                    cig = elem.rsplit(":",1)[1]
                elif elem.startswith("de:"): # difference
                    diff = float(elem.rsplit(":",1)[1])
                    if diff > max_diff:
                        max_diff = diff
                    if diff < 0:
                        cont = True
            if cont:
                cont = False
                continue
            start = int(spl[2])
            end = int(spl[3])
            #frags.append((start, end))
            frags.append((end-start)/float(length)*100)
            cigs.append(cig)
            diffs.append(float(diff)*100)
        if assembler in assemblers:
            assemblers[assembler][0].extend(frags)
            assemblers[assembler][1].extend(cigs)
            assemblers[assembler][2].extend(diffs)
            assemblers[assembler][3].extend(c_lengths)
        else:
            assemblers[assembler] = [frags, cigs, diffs, c_lengths]

subset = ['ABySS_short','A-STAR_contig_hybrid','HipMer_Metagenome_short','marmgCAMI2_short_read_pooled_gsa','Megahit_v1-1-4-2_short','metaSPAdes_v3-13-1_short','Miniasm_GATB_hybrid','OPERA-MS-inhouse_hybrid']
subset_names = {'ABySS_short':"ABySS",'A-STAR_contig_hybrid':"A-STAR",'HipMer_Metagenome_short':"HipMer",'marmgCAMI2_short_read_pooled_gsa':"gsa",'Megahit_v1-1-4-2_short':"MEGAHIT",'metaSPAdes_v3-13-1_short':"metaSPAdes",'Miniasm_GATB_hybrid':"GATB",'OPERA-MS-inhouse_hybrid':"OPERA-MS"}
fig, (ax1, ax2) = plt.subplots(figsize=(14, 12), nrows=1, ncols=2, sharey = True)
#ax1.set_title("Completeness", fontsize=20)
ax1.tick_params(labelsize=20)
#ax2.set_title("Divergence", fontsize=20)
ax2.tick_params(labelsize=20)
completeness = {}
divergence = {}
lengths = {}
for assembler in assemblers:
    if assembler not in subset:
        continue
    print(assembler)
    print("mean: %s" % statistics.mean(assemblers[assembler][0]))
    print("median: %s" % statistics.median(assemblers[assembler][0]))
    print("mean contig length: %s" % statistics.mean(assemblers[assembler][3]))
    print("median contig length: %s" % statistics.median(assemblers[assembler][3]))
    completeness[assembler] = assemblers[assembler][0]
    divergence[assembler] = assemblers[assembler][2]
    #if (assembler != 'marmgCAMI2_short_read_pooled_gsa'):
    lengths[assembler] = assemblers[assembler][3]

plot1 = ax1.violinplot([completeness[x] for x in subset_names], vert=False)
plot2 = ax2.violinplot([divergence[x] for x in subset_names], vert=False)
ax1.set_yticks(np.arange(1, len(subset) + 1))
#ax2.set_yticks(np.arange(1, len(subset) + 1))
ax1.set_yticklabels(["%s (%s)" % (subset_names[x], len(assemblers[x][1])) for x in subset], fontsize=20)
#ax2.set_yticklabels([subset_names[x] for x in subset])
ax1.set_xlabel("Genome fraction (%)", fontsize=20)
ax2.set_xlabel("Mismatched bases (%)", fontsize=20)
colors = sns.color_palette("tab10")
for patch, color in zip(plot1['bodies'], colors):
    patch.set_color(color)
    patch.set_edgecolor('black')
for patch, color in zip(plot2['bodies'], colors):
    patch.set_color(color)
    patch.set_edgecolor('black')
fig.suptitle("16S rRNA gene assembly quality", fontsize=22)
plt.savefig("16S_violins.png", bbox_inches='tight')
plt.close()

plot3 = plt.boxplot([lengths[x] for x in subset_names], vert=False, patch_artist=True)
plt.yticks(np.arange(1, len(subset) + 1),[subset_names[x] for x in subset_names])
#plt.ticklabel_format(axis='x',style='sci',scilimits=(0,0))
plt.xlabel("Mapped contig lengths (bp)")
plt.xscale("log")
colors = sns.color_palette("tab10")
for patch, color in zip(plot3['boxes'], colors):
    patch.set(facecolor = color, alpha = 0.3)
plt.title("16S rRNA gene carrying contig lengths", fontsize=12)
plt.savefig("16S_boxes_lengths.png", dpi=200, bbox_inches='tight')
