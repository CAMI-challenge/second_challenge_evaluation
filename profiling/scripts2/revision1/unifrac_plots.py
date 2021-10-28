#!/usr/bin/env python

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv('second_challenge_evaluation/profiling/SamplesForUniFracBaseline/79884_unifrac_human.tsv', sep='\t', index_col=0)
print(df.describe())

fig, axs = plt.subplots(1, 2, figsize=(14, 5))

meanprops = dict(markerfacecolor='black', markeredgecolor='black', markersize=10, marker='>')

plot0 = sns.boxplot(ax=axs[0], x=df['0'], showmeans=True, meanprops=meanprops, color=sns.color_palette('colorblind')[9])
plot0.set_xlim([0, 16])
plot0.grid(which='major', linestyle=':', linewidth='0.5', axis='x')
plot0.set_xlabel('Weighted UniFrac error', fontsize=14)
plot0.tick_params(axis='x', labelsize=12)
plot0.text(-.05, 1, 'a', transform=plot0.transAxes, size=14, weight='bold')
# plot0.set_title(category.replace('_', ' '), fontsize=fontsize, pad=3)

plot1 = sns.histplot(df['0'], ax=axs[1])
plot1.set_xlim([0, 16])
plot1.set_xlabel('Weighted UniFrac error', fontsize=14)
plot1.set_ylabel('Count', fontsize=14)
plot1.tick_params(axis='x', labelsize=12)
plot1.tick_params(axis='y', labelsize=12)
plot1.grid(which='major', linestyle=':', linewidth='0.5', axis='y')
plot1.text(-.15, 1, 'b', transform=plot1.transAxes, size=14, weight='bold')

plt.subplots_adjust(wspace=0.25)
# fig.suptitle("Samples matching 10394.H1.*.*.*.II", fontsize=14)

fig.savefig('plots_human.png', dpi=200, format='png', bbox_inches='tight')
plt.close()
