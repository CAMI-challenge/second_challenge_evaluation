import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
matplotlib.use('Agg')


FILE = '../data/runtimes.csv'
COLORS = sns.color_palette('colorblind')
COLORS1_AS = COLORS[2]
COLORS2_AS = COLORS[7]
COLORS1_GB = COLORS[3]
COLORS2_GB = COLORS[8]
COLORS1_TB = COLORS[0]
COLORS2_TB = COLORS[9]
COLORS1_PR = COLORS[4]
COLORS2_PR = COLORS[6]


def comp_average(a, b):
    if np.isnan(a):
        return b
    if np.isnan(b):
        return a
    return (a + b) / 2


def get_sorted(runtimes, tools, metric):
    x = runtimes[runtimes['Name'].isin(tools)].copy()
    x['method'] = x['Name'] + ' ' + x['Version'] + ' ' + x['detail']

    x = x[['method', metric, 'dataset']]
    x = x.pivot_table(index=['method'], columns='dataset', values=metric)

    if not 'strain madness' in x.columns:
        x['average'] = x['marine']
    else:
        x['average'] = x.apply(lambda row: comp_average(row['marine'], row['strain madness']), axis=1)
    x = x.sort_values(by=['average']).drop(columns='average')
    return x


def format_pd(runtimes, metric):
    sorted_pd = get_sorted(runtimes, assemblers, metric)
    n0 = len(sorted_pd)
    sorted_pd = pd.concat([sorted_pd, get_sorted(runtimes, genome_binners, metric)])
    n1 = len(sorted_pd) - n0
    sorted_pd = pd.concat([sorted_pd, get_sorted(runtimes, taxonomic_binners, metric)])
    n2 = len(sorted_pd) - n0 - n1
    sorted_pd = pd.concat([sorted_pd, get_sorted(runtimes, profilers, metric)])
    n3 = len(sorted_pd) - n0 - n1 - n2

    sorted_pd = sorted_pd * 100
    sorted_pd = np.log2(sorted_pd).clip(lower=0)

    colors1_as = [COLORS1_AS] * n0
    colors2_as = [COLORS2_AS] * n0
    colors1_gb = [COLORS1_GB] * n1
    colors2_gb = [COLORS2_GB] * n1
    colors1_tb = [COLORS1_TB] * n2
    colors2_tb = [COLORS2_TB] * n2
    colors1_pr = [COLORS1_PR] * n3
    colors2_pr = [COLORS2_PR] * n3
    my_colors = (
        tuple(colors1_as + colors1_gb + colors1_tb + colors1_pr),
        tuple(colors2_as + colors2_gb + colors2_tb + colors2_pr))

    return sorted_pd, my_colors, metric


def add_legend(save, ax=None):
    if not ax:
        fig, ax = plt.subplots(figsize=(12, 1))
        ax.axis('off')

    xpos = 0.17
    ypos = 1.33

    circles = [
        Line2D([], [], markeredgewidth=0, linestyle="None", marker="s", markersize=8, markerfacecolor=COLORS1_AS)]
    leg0 = ax.legend(circles, ['marine'], loc='upper right', bbox_to_anchor=(xpos, ypos), fontsize=14, borderaxespad=0.,
                     handlelength=1, handletextpad=.5, frameon=False, title='Assembly')
    leg0._legend_box.align = 'left'
    leg0.get_title().set_fontsize(14)

    circles = [
        Line2D([], [], markeredgewidth=0, linestyle="None", marker="s", markersize=8, markerfacecolor=COLORS1_GB),
        Line2D([], [], markeredgewidth=0, linestyle="None", marker="s", markersize=8, markerfacecolor=COLORS2_GB)]
    leg1 = ax.legend(circles, ['marine', 'strain madness'], loc='upper right', bbox_to_anchor=(xpos + 0.25, ypos),
                     fontsize=14, borderaxespad=0., handlelength=1, handletextpad=.5, frameon=False,
                     title='Genome binning')
    leg1._legend_box.align = 'left'
    leg1.get_title().set_fontsize(14)

    circles = [
        Line2D([], [], markeredgewidth=0, linestyle="None", marker="s", markersize=8, markerfacecolor=COLORS1_TB),
        Line2D([], [], markeredgewidth=0, linestyle="None", marker="s", markersize=8, markerfacecolor=COLORS2_TB)]
    leg2 = ax.legend(circles, ['marine', 'strain madness'], loc='upper right', bbox_to_anchor=(xpos + 0.50, ypos),
                     fontsize=14, borderaxespad=0., handlelength=1, handletextpad=.5, frameon=False,
                     title='Taxonomic binning')
    leg2._legend_box.align = 'left'
    leg2.get_title().set_fontsize(14)

    circles = [
        Line2D([], [], markeredgewidth=0, linestyle="None", marker="s", markersize=8, markerfacecolor=COLORS1_PR),
        Line2D([], [], markeredgewidth=0, linestyle="None", marker="s", markersize=8, markerfacecolor=COLORS2_PR)]
    leg3 = ax.legend(circles, ['marine', 'strain madness'], loc='upper right', bbox_to_anchor=(xpos + 0.75, ypos),
                     fontsize=14, borderaxespad=0., handlelength=1, handletextpad=.5, frameon=False,
                     title='Taxonomic profiling')
    leg3._legend_box.align = 'left'
    leg3.get_title().set_fontsize(14)

    plt.gca().add_artist(leg0)
    plt.gca().add_artist(leg1)
    plt.gca().add_artist(leg2)

    if save:
        plt.savefig('efficiency_legend.pdf', dpi=100, format='pdf', bbox_inches='tight')


def doit(sorted_pd, my_colors, metric):
    ax = sorted_pd.plot(kind='barh', zorder=20, color=my_colors, figsize=(4, 12), width=0.7)
    ax.grid(which='major', axis='x', linestyle='-', linewidth='0.5', color='lightgrey', zorder=0)
    ax.set_xlabel(metric, fontsize=14)
    ax.set_ylabel('')
    ax.tick_params(axis='y', which='both', labelsize=12, labelbottom=True)
    ax.tick_params(axis='x', which='both', labelsize=12, labelbottom=True)

    ax.xaxis.set_major_locator(plt.MaxNLocator(6))
    vals = ax.get_xticks()
    ax.set_xticklabels(['{:,.1f}'.format(np.exp2(x) / 100) for x in vals], fontsize=12)

    plt.gca().invert_yaxis()

    # add_legend(save=False, ax=ax)
    plt.legend().set_visible(False)

    if metric == 'Runtime (hours)':
        plt.savefig('runtimes.pdf', dpi=100, format='pdf', bbox_inches='tight')
    else:
        plt.savefig('memory_usage.pdf', dpi=100, format='pdf', bbox_inches='tight')

    plt.close()


if __name__ == "__main__":
    # add_legend(save=True)
    # exit()
    runtimes = pd.read_csv(FILE, sep=',').fillna('')

    assemblers = 'Flye,MEGAHIT,metaSPAdes,OPERA-MS,Ray Meta,AbySS'.split(',')
    genome_binners = 'UltraBinner,MetaBAT,MetaBinner,Autometa,MaxBin,CONCOCT,SolidBin,LSHVec,Vamb'.split(',')
    taxonomic_binners = 'DIAMOND,MEGAN,Kraken,PhyloPythiaS+'.split(',')
    profilers = ['Bracken', 'CCMetagen', 'Centrifuge', 'DUDes', 'FOCUS', 'LSHVec', 'MetaPhlAn', 'MetaPhyler',
                 'Metalign', 'MetaPalette', 'mOTUs', 'TIPP']

    doit(*format_pd(runtimes, 'Runtime (hours)'))
    doit(*format_pd(runtimes, 'Maximum memory (GB)'))
