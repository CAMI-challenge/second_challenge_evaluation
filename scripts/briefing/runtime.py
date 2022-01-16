import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
matplotlib.use('Agg')


FILE = '../../data/runtimes.csv'
COLORS = sns.color_palette('colorblind')
COLORS1_AS = COLORS[2]
COLORS2_AS = COLORS[7]
COLORS1_GB = COLORS[3]
COLORS2_GB = COLORS[8]
COLORS1_TB = COLORS[0]
COLORS2_TB = COLORS[9]
COLORS1_PR = COLORS[4]
COLORS2_PR = COLORS[6]


assemblers = 'MetaHipMer,MEGAHIT,GATB,metaSPAdes,OPERA-MS,Ray Meta,AbySS'.split(',')
genome_binners = 'UltraBinner,MetaBAT,MetaBinner,Autometa,MaxBin,CONCOCT,SolidBin,LSHVec,Vamb'.split(',')
taxonomic_binners = 'DIAMOND,MEGAN,Kraken,PhyloPythiaS+'.split(',')
profilers = ['Bracken', 'CCMetagen', 'Centrifuge', 'DUDes', 'FOCUS', 'LSHVec', 'MetaPhlAn', 'MetaPhyler',
             'Metalign', 'MetaPalette', 'mOTUs', 'TIPP']


def comp_average(a, b):
    if np.isnan(a):
        return b
    if np.isnan(b):
        return a
    return (a + b) / 2


def get_sorted(runtimes, tools, metric):
    x = runtimes[runtimes['Name'].isin(tools)].copy()
    # x['method'] = x['Name'] + ' ' + x['Version'] + ' ' + x['detail'].str.upper()
    x['method'] = x['Name'] + ' ' + x['detail'].str.upper()

    x = x.sort_values(by=['Runtime (hours)']).drop_duplicates(subset=['Name', 'dataset'])
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

    colors1_as = [COLORS1_AS] * n0
    colors2_as = [COLORS2_AS] * n0
    colors1_gb = [COLORS1_GB] * n1
    colors2_gb = [COLORS2_GB] * n1
    colors1_tb = [COLORS1_TB] * n2
    colors2_tb = [COLORS2_TB] * n2
    colors1_pr = [COLORS1_PR] * n3
    colors2_pr = [COLORS2_PR] * n3
    my_colors = {'marine': colors1_as + colors1_gb + colors1_tb + colors1_pr,
                 'strain madness': colors2_as + colors2_gb + colors2_tb + colors2_pr}

    return sorted_pd, my_colors, metric


def add_legend(ax):
    xpos = -1.1
    ypos = -0.144
    fontsize = 18

    circles = [
        Line2D([], [], markeredgewidth=0, linestyle="None", marker="s", markersize=14, markerfacecolor=COLORS1_AS)]
    leg0 = ax.legend(circles, ['marine'], loc='lower left', bbox_to_anchor=(xpos, ypos), fontsize=fontsize, borderaxespad=0.,
                     handlelength=1, handletextpad=.3, frameon=False, title='Assembly')
    leg0._legend_box.align = 'left'
    leg0.get_title().set_fontsize(fontsize)

    circles = [
        Line2D([], [], markeredgewidth=0, linestyle="None", marker="s", markersize=14, markerfacecolor=COLORS1_GB),
        Line2D([], [], markeredgewidth=0, linestyle="None", marker="s", markersize=14, markerfacecolor=COLORS2_GB)]
    leg1 = ax.legend(circles, ['marine', 'strain madness'], loc='lower left', bbox_to_anchor=(xpos, ypos - 0.1),
                     fontsize=fontsize, borderaxespad=0., handlelength=1, handletextpad=.3, frameon=False,
                     title='Genome binning')
    leg1._legend_box.align = 'left'
    leg1.get_title().set_fontsize(fontsize)

    circles = [
        Line2D([], [], markeredgewidth=0, linestyle="None", marker="s", markersize=14, markerfacecolor=COLORS1_TB),
        Line2D([], [], markeredgewidth=0, linestyle="None", marker="s", markersize=14, markerfacecolor=COLORS2_TB)]
    leg2 = ax.legend(circles, ['marine', 'strain madness'], loc='lower left', bbox_to_anchor=(xpos + 1.1, ypos - 0.033),
                     fontsize=fontsize, borderaxespad=0., handlelength=1, handletextpad=.3, frameon=False,
                     title='Taxonomic binning')
    leg2._legend_box.align = 'left'
    leg2.get_title().set_fontsize(fontsize)

    circles = [
        Line2D([], [], markeredgewidth=0, linestyle="None", marker="s", markersize=14, markerfacecolor=COLORS1_PR),
        Line2D([], [], markeredgewidth=0, linestyle="None", marker="s", markersize=14, markerfacecolor=COLORS2_PR)]
    leg3 = ax.legend(circles, ['marine', 'strain madness'], loc='lower left', bbox_to_anchor=(xpos + 1.1, ypos - 0.13),
                     fontsize=fontsize, borderaxespad=0., handlelength=1, handletextpad=.3, frameon=False,
                     title='Taxonomic profiling')
    leg3._legend_box.align = 'left'
    leg3.get_title().set_fontsize(fontsize)

    plt.gca().add_artist(leg0)
    plt.gca().add_artist(leg1)
    plt.gca().add_artist(leg2)
    plt.gca().add_artist(leg3)


def doit(sorted_pd, my_colors, metric, ax):
    ax = sorted_pd.plot(kind='barh', zorder=20, color=my_colors, ax=ax) # figsize=(4, 12), width=0.7,
    ax.grid(which='major', axis='x', linestyle='-', linewidth='0.5', color='lightgrey', zorder=0)
    ax.set_xlabel(metric, fontsize=20)
    ax.set_ylabel('')
    ax.tick_params(axis='y', which='both', labelsize=16, labelbottom=True, pad=-1)
    ax.tick_params(axis='x', which='both', labelsize=16, labelbottom=True)

    ax.set_xscale('symlog')  # linthresh=1
    vals = ax.get_xticks()
    vals[1] = 1

    plt.gca().invert_yaxis()

    add_legend(ax)
    plt.legend().set_visible(False)


