import labels as utils_labels
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import os
import pandas as pd


def plot_summary(counts, df_results, tools, output_dir, rank, file_name, xlabel, ylabel):
    cmaps = ['Blues_r', 'Reds_r', 'Greens_r', 'Purples_r', 'Wistia', 'Greys_r', 'Oranges', 'cool_r', 'pink', 'GnBu_r']
    colors_list = []
    for i, count in enumerate(counts):
        if isinstance(count, list):
            print(cmaps[i], 'X')
            colors = plt.get_cmap(cmaps[i])(np.linspace(.3, .7, count[-1] + 1))[:-1]
            for j, color in enumerate(colors, start=1):
                if j in count:
                    colors_list.append(tuple(color))
        elif count != 0:
            print(cmaps[i])
            colors = plt.get_cmap(cmaps[i])(np.linspace(.3, .7, count + 1))[:-1]
            for color in colors:
                colors_list.append(tuple(color))

    df_mean = df_results.groupby(utils_labels.TOOL).mean().reindex(tools)


    fig, axs = plt.subplots(figsize=(5, 4.5))

    # force axes to be from 0 to 100%
    axs.set_xlim([0.0, 1.0])
    axs.set_ylim([0.0, 1.0])

    for i, (tool, df_row) in enumerate(df_mean.iterrows()):
        axs.errorbar(df_row[utils_labels.AVG_PRECISION_BP], df_row[utils_labels.AVG_RECALL_BP], xerr=df_row['avg_precision_bp_var'], yerr=df_row['avg_recall_bp_var'],
                     fmt='o',
                     ecolor=colors_list[i],
                     mec=colors_list[i],
                     mfc=colors_list[i],
                     capsize=3,
                     markersize=8)

    # turn on grid
    # axs.minorticks_on()
    axs.grid(which='major', linestyle=':', linewidth='0.5')
    # axs.grid(which='minor', linestyle=':', linewidth='0.5')

    axs.tick_params(axis='x', labelsize=12)
    vals = axs.get_yticks()
    axs.set_yticklabels(['{:3.0f}'.format(x * 100) for x in vals], fontsize=11)
    vals = axs.get_xticks()
    axs.set_xticklabels(['{:3.0f}'.format(x * 100) for x in vals], fontsize=11)

    if rank:
        file_name = rank + '_' + file_name
        plt.title(rank)
        ylabel = ylabel.replace('genome', 'taxon')

    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.tight_layout()
    # fig.savefig(os.path.join(output_dir, file_name + '.eps'), dpi=100, format='eps', bbox_inches='tight')

    colors_iter = iter(colors_list)
    circles = []
    for x in range(len(df_mean)):
        circles.append(Line2D([], [], markeredgewidth=0.0, linestyle="None", marker="o", markersize=11, markerfacecolor=next(colors_iter)))
    lgd = plt.legend(circles, tools, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., handlelength=0, frameon=False, fontsize=12)

    # fig.savefig(os.path.join(output_dir, binning_type, file_name + '.pdf'), dpi=100, format='pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, file_name + '.png'), dpi=200, format='png', bbox_extra_artists=(lgd,), bbox_inches='tight')
    fig.savefig(os.path.join(output_dir, file_name + '.pdf'), dpi=200, format='pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.close(fig)


def main():
    #workdir = '/home/fmeyer/cami2/paper/strain_madness'
    workdir = '/home/dkoslicki/Desktop/second_challenge_evaluation/profiling/scripts'  # FIXME: not portable
    df_results = pd.read_csv(os.path.join(workdir, 'amber_strain_madness_unique.tsv'), sep='\t')
    labels = 'MetaBAT (A1),MetaBAT (A2),MetaBinner (B1),MetaBinner (B2),MetaBinner (B3),MetaBinner (B4),Autometa (C1),Autometa (C2),MetaWRAP (D1),UltraBinner (E1),UltraBinner (E2),UltraBinner (E3),MaxBin (F1),CONCOCT (G1),SolidBin (H1),SolidBin (H2),SolidBin (H3),LSHVec-strain (I1)'.split(',')
    counts = [2, 4, 2, 1, 3, 1, 1, 3, 1]
    file_name = '_strain_madness'

    plot_summary(counts, df_results, labels, workdir, None,
                 'avg_purity_completeness_bp' + file_name,
                 'Average purity per bin (%)',
                 'Average completeness per genome (%)')


    #workdir = '/home/fmeyer/cami2/ismb2020/marine'
    workdir = '/home/dkoslicki/Desktop/second_challenge_evaluation/profiling/scripts'  # FIXME: not portable
    df_results = pd.read_csv(os.path.join(workdir, 'amber_marine_megahit.tsv'), sep='\t')
    labels = 'A1,A2,B2,B3,B4,B5,B7,B8,B9,D1,E1,E2,F1,G1,J1'.split(',')
    counts = [2, [2, 3, 4, 5, 7, 8, 9], 0, 1, 2, 1, 1, 0, 0, 1]
    file_name = '_marine_megahit'

    plot_summary(counts, df_results, labels, workdir, None,
                 'avg_purity_completeness_bp' + file_name,
                 'Average purity per bin (%)',
                 'Average completeness per genome (%)')



if __name__ == "__main__":
    main()