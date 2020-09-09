import labels as utils_labels
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import os
import pandas as pd
from pathlib import Path
import traceback
import sys

def plot_summary(counts, df_results, tools, output_dir, rank, file_name, xlabel, ylabel, x_key, y_key, x_lim, y_lim):
    cmaps = ['Blues_r', 'Reds_r', 'Greens_r', 'Purples_r', 'Wistia', 'Greys_r', 'Oranges', 'cool_r', 'pink', 'GnBu_r']
    colors_list = []
    for i, count in enumerate(counts):
        if isinstance(count, list):
            #print(cmaps[i], 'X')
            colors = plt.get_cmap(cmaps[i])(np.linspace(.3, .7, count[-1] + 1))[:-1]
            for j, color in enumerate(colors, start=1):
                if j in count:
                    colors_list.append(tuple(color))
        elif count != 0:
            #print(cmaps[i])
            colors = plt.get_cmap(cmaps[i])(np.linspace(.3, .7, count + 1))[:-1]
            for color in colors:
                colors_list.append(tuple(color))

    df_mean = df_results.fillna(np.inf).groupby('tool').mean().reindex(tools).replace(np.inf, np.nan)
    df_std = df_results.fillna(np.inf).groupby('tool').std().reindex(tools).replace(np.inf, np.nan)

    fig, axs = plt.subplots(figsize=(5, 4.5))

    # force axes to be in specified range
    axs.set_xlim([0.0, x_lim])
    axs.set_ylim([0.0, y_lim])

    for i, (tool, df_row) in enumerate(df_mean.iterrows()):
        #print(df_std.loc[tool].loc[x_key])
        try:
            axs.errorbar(df_row[x_key], df_row[y_key], xerr=df_std.loc[tool].loc[x_key], yerr=df_std.loc[tool].loc[y_key],
                         fmt='o',
                         ecolor=colors_list[i],
                         mec=colors_list[i],
                         mfc=colors_list[i],
                         capsize=3,
                         markersize=8)
        except:
            continue

    # turn on grid
    # axs.minorticks_on()
    axs.grid(which='major', linestyle=':', linewidth='0.5')
    # axs.grid(which='minor', linestyle=':', linewidth='0.5')

    axs.tick_params(axis='x', labelsize=12)
    vals = axs.get_yticks()
    axs.set_yticklabels(['{:0.2f}'.format(x * 1) for x in vals], fontsize=11)
    vals = axs.get_xticks()
    axs.set_xticklabels(['{:0.2f}'.format(x * 1) for x in vals], fontsize=11)

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
    #print(f"Output: {os.path.join(output_dir, file_name + '.png')}")

def make_scatter(name):
    OPAL_options = name
    for dataset in ["marine_dataset", "strain_madness_dataset"]:
        for submission_type in ["short_read_samples", "long_read_samples", "assembly_or_averaged"]:
            base = str(Path(os.path.abspath(os.path.join(__file__, os.pardir))).parent) + f"/{dataset}/"
            opal_out = f"{base}results/OPAL_{OPAL_options}_{submission_type}"
            for rank in ["Superkingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species"]:
                try:
                    out_dir = opal_out
                    input = f"{opal_out}/by_rank/{rank.lower()}.tsv"
                    print(input)
                    df_results = pd.read_csv(input, sep='\t', na_values='na')
                    df_group = df_results.groupby('tool')
                    tools = sorted(df_group.indices.keys())
                    tools_string = list(tools)
                    tools_base = list(map(lambda x: x.split('v')[0], tools_string))
                    _, counts = np.unique(tools_base, return_counts=True)  # this is not stable, hence we need to sort above

                    # purity/completeness
                    plot_summary(counts, df_results, tools, out_dir, rank,
                                 'completeness_purity_' + dataset,
                                 'Completeness',
                                 'Purity',
                                 'Completeness',
                                 'Purity',
                                 1.0,
                                 1.0)

                    # L1 norm error/Weighted UniFrac error
                    plot_summary(counts, df_results, tools, out_dir, rank,
                                 'L1_wUniFrac_' + dataset,
                                 'Weighted UniFrac error',
                                 'L1 norm error',
                                 'Weighted UniFrac error',
                                 'L1 norm error',
                                 0.15,
                                 2)
                except:
                    #sys.exit(1)
                    tb = traceback.format_exc()
                    error_type, error, _ = sys.exc_info()
                    #print(tb)
                    print(error)


def main():
    make_scatter("default")
    # Normalized
    make_scatter("normalized")
    # Filtered 1%
    make_scatter("filtered")
    # Normalized and Filtered 1%
    make_scatter("normalized_filtered")


if __name__ == "__main__":
    main()