import pandas as pd
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import string
import itertools


TOOL = "Tool"
AVG_RECALL_BP_CAMI1 = "CAMI 1 average completeness (bp)"
AVG_PRECISION_BP = "Average purity (bp)"
ARI_BY_BP = "Adjusted Rand index (bp)"
PERCENTAGE_ASSIGNED_BPS = "Percentage of binned bp"
F1_SCORE_BP_CAMI1 = "CAMI 1 F1 score (bp)"
SAMPLE = "Sample"
MIN_RECALL = '> 50% completeness'
MIN_RECALL_LIST = [.5]
MAX_CONTAMINATION_LIST = [.1]

pd.set_option('display.expand_frame_repr', False)
METRICS = [AVG_RECALL_BP_CAMI1, AVG_PRECISION_BP, ARI_BY_BP, PERCENTAGE_ASSIGNED_BPS]
METRICS_R = [metric + 'rank' for metric in METRICS]

# pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
# pd.set_option('display.max_colwidth', 99999999)
pd.set_option('display.expand_frame_repr', False)

DATASETS = ['mar_gsa', 'mar_ma', 'str_gsa', 'str_ma', 'rhi_gsa', 'rhi_ma']
DATASETSB = ['mar_unique', 'mar_common', 'str_unique', 'str_common']

DATASET_TO_PATH = {'mar_gsa': '../marine_dataset/results/amber_marine_nocircular/',
                   'mar_ma': '../marine_dataset/results/amber_marine_megahit_nocircular/',
                   'str_gsa': '../strain_madness_dataset/results/amber_strain_madness/',
                   'str_ma': '../strain_madness_dataset/results/amber_strain_madness_megahit/',
                   'rhi_gsa': '../plant_associated_dataset/results/amber_rhizosphere_noplasmids/',
                   'rhi_ma': '../plant_associated_dataset/results/amber_rhizosphere_megahit_noplasmids/',
                   'mar_unique': '../strain_madness_dataset/results/amber_marine_unique_strains_nocircular/',
                   'mar_common': '../strain_madness_dataset/results/amber_marine_common_strains_nocircular/',
                   'str_unique': '../strain_madness_dataset/results/amber_strain_madness_unique_strains/',
                   'str_common': '../strain_madness_dataset/results/amber_strain_madness_common_strains/'}

DATASETS_L = {'mar_gsa': 'Marine\ngsa', 'mar_ma': 'Marine\nma',
              'str_gsa': 'Strain\nmadness\ngsa', 'str_ma': 'Strain\nmadness\nma',
              'rhi_gsa': 'Plant-\nassociated\ngsa', 'rhi_ma': 'Plant-\nassociated\nma',
              'mar_unique': 'Marine\nunique\nstrains', 'mar_common': 'Marine\ncommon\nstrains',
              'str_unique': 'Strain\nmadness\nunique\nstrains', 'str_common': 'Strain\nmadness\ncommon\nstrains'}

DATASETS_L2 = {'mar_gsa': 'Marine gsa', 'mar_ma': 'Marine ma',
               'str_gsa': 'Strain m. gsa', 'str_ma': 'Strain m. ma',
               'rhi_gsa': 'Plant-a. gsa', 'rhi_ma': 'Plant-a. ma'}


def get_ranked(results_path):
    x = pd.read_csv(results_path + 'results.tsv', sep='\t')
    x = x[x[TOOL] != 'Gold standard']
    x = x[[TOOL] + METRICS + [F1_SCORE_BP_CAMI1]]

    x['method'] = x.apply(lambda row: row['Tool'].split(' ')[0], axis=1)
    x = x.loc[x.groupby('method')[F1_SCORE_BP_CAMI1].idxmax()].sort_index()

    for metric, metric_r in zip(METRICS, METRICS_R):
        x[metric_r] = x[metric].rank(method='min', ascending=False, na_option='bottom') - 1

    return x[['method', TOOL] + METRICS_R + METRICS].set_index(['method'])


def get_pds(datasets):
    pdres = pd.concat([get_ranked(DATASET_TO_PATH[dataset]).rename(columns=dict([(col, dataset+col) for col in METRICS + METRICS_R + [TOOL]])) for dataset in datasets], axis=1)
    return pdres


def get_pds_unranked(datasets):
    def readfile(path, dataset):
        x = pd.read_csv(path + 'results.tsv', sep='\t')
        x = x[x[TOOL] != 'Gold standard']
        x['dataset'] = dataset
        return x[[TOOL, 'dataset'] + METRICS]

    pdres = pd.concat([readfile(DATASET_TO_PATH[dataset], DATASETS_L2[dataset]) for dataset in datasets], axis=0)
    return pdres


def go(sortedpd, plotcols, datasets, row1, axs, num_rows, pdres_u=pd.DataFrame()):

    def format_axs(i, j, dataset=None):
        axs[i, j].set_xlim([0, 1])

        axs[i, j].set_xticklabels(['{:3.0f}'.format(x * 100) for x in axs[i, j].get_xticks()], fontsize=10, ha='right')

        axs[i, j].tick_params(axis='y', length=0, labelsize=9)

        axs[i, j].spines['right'].set_visible(False)
        axs[i, j].spines['top'].set_visible(False)
        axs[i, j].set_xlabel('')

        if j == 4 and dataset:
            axs[i, j].set_ylabel(DATASETS_L[dataset], fontsize=11, rotation='0', labelpad=35)
            axs[i, j].yaxis.set_label_position('right')
            axs[i, j].yaxis.set_label_coords(1.4, .7)
        elif j == 0:
            axs[i, j].set_ylabel(string.ascii_lowercase[i], rotation='0', weight='bold', fontsize=12)
            axs[i, j].yaxis.set_label_coords(-.8, .85)
        else:
            axs[i, j].set_ylabel('')

        if j > 0:
            axs[i, j].set_yticklabels('')

        if i == num_rows - 1:
            axs[i, j].set_xlabel(xlabel, fontsize=11)
        else:
            axs[i, j].set_xlabel('')

        axs[i, j].grid(which='major', linestyle=':', linewidth='0.5', axis='x')

    if not pdres_u.empty:
        i = 0
        for j, plotcol in enumerate(plotcols):
            metric_ = plotcol['metric_']

            data_order = [DATASETS_L2[dataset] for dataset in datasets]
            print(data_order)
            meanprops = dict(markerfacecolor='black', markeredgecolor='black', markersize=4, marker='>')
            sns.boxplot(orient='h', x=metric_, y='dataset', data=pdres_u, ax=axs[i, j], showmeans=True, order=data_order, linewidth=.5, fliersize=1, meanprops=meanprops)
            format_axs(i, j)

    for j, plotcol in enumerate(plotcols):
        xlabel = plotcol['label']
        metric = plotcol['metric'] if 'metric' in plotcol else None
        metric_ = plotcol['metric_']
        for i, dataset in enumerate(datasets, row1 if pdres_u.empty else row1 + 1):
            print(dataset, i)
            # sortedpd = sortedpd.sort_values(by=[dataset + metric_ + 'rank'])

            sorted_tools = sortedpd[[dataset + TOOL, dataset + metric_, 'color']]
            sorted_tools = sorted_tools[~sorted_tools[dataset + TOOL].isna()]

            if metric_ == ARI_BY_BP or metric_ == PERCENTAGE_ASSIGNED_BPS or metric_ == MIN_RECALL:
                sns.barplot(x=dataset + metric_, y=dataset + TOOL, data=sorted_tools, order=sorted_tools[dataset + TOOL], ax=axs[i, j], linewidth=0.5)

                for patch, color in zip(axs[i, j].patches, sorted_tools.color.values.tolist()):
                    patch.set_facecolor(color)
                    patch.set_edgecolor('black')

            else:
                if metric == 'recall_bp':
                    pd_bins = pd.read_csv(DATASET_TO_PATH[dataset] + 'genome_metrics_cami1.tsv', sep='\t')
                elif metric == 'precision_bp':
                    pd_bins = pd.read_csv(DATASET_TO_PATH[dataset] + 'bin_metrics.tsv', sep='\t')
                pd_bins = pd_bins[pd_bins[TOOL].isin(sorted_tools[dataset + TOOL])]
                pd_bins['method'] = pd_bins[TOOL].map(pd.Series(sorted_tools.index.values, index=sorted_tools[dataset + TOOL]))
                pd_bins = pd_bins[['method', metric]]

                meanprops = dict(markerfacecolor='black', markeredgecolor='black', markersize=4, marker='>')
                sns.boxplot(orient='h', x=metric, y='method', data=pd_bins, ax=axs[i, j], showmeans=True, order=sorted_tools.index, linewidth=.5, meanprops=meanprops, fliersize=1)

                for artists_i, (artist, color) in enumerate(zip(axs[i, j].artists, sorted_tools.color.values.tolist())):
                    artist.set_facecolor(color)
                    for artist_j in range(artists_i * 7, artists_i * 7 + 7):
                        line = axs[i, j].lines[artist_j]
                        if artist_j % 7 == 6:
                            line.set_color(color)
                            line.set_mfc(color)
                            line.set_mec(color)

            format_axs(i, j, dataset)


def calc_num_recovered_genomes(pd_bins, min_completeness, max_contamination):
    counts_list = []
    for (sample_id, tool), pd_group in pd_bins.groupby(['sample_id', TOOL]):
        for x in itertools.product(min_completeness, max_contamination):
            count = pd_group[(pd_group['recall_bp'] > x[0]) & (pd_group['precision_bp'] > (1 - x[1]))].shape[0]
            counts_list.append((sample_id, tool, '> ' + str(int(x[0] * 100)) + '% completeness', '< ' + str(int(x[1] * 100)) + '%', count))

    pd_counts = pd.DataFrame(counts_list, columns=[SAMPLE, TOOL, 'Completeness', 'Contamination', 'count'])
    pd_counts = pd.pivot_table(pd_counts, values='count', index=[SAMPLE, TOOL, 'Contamination'], columns=['Completeness']).reset_index()
    return pd_counts


def load_hq_bins(datasets):

    def readfile(dataset):
        pd_bins = pd.read_csv(DATASET_TO_PATH[dataset] + 'bin_metrics.tsv', sep='\t')
        df = calc_num_recovered_genomes(pd_bins, MIN_RECALL_LIST, MAX_CONTAMINATION_LIST)
        df['dataset'] = DATASETS_L2[dataset]
        if dataset == 'str_ma':
            gs = 408
        else:
            gs = df[df[TOOL] == 'Gold standard'][MIN_RECALL].values[0]
        df[MIN_RECALL] = df[MIN_RECALL] / gs
        df = df[df[TOOL] != 'Gold standard']
        return df

    pdres = pd.concat([readfile(dataset) for dataset in datasets], axis=0)
    return pdres.drop(columns=['Sample', 'Contamination'])


def load_hq_bins_best(datasets):

    def readfile(dataset):
        pd_bins = pd.read_csv(DATASET_TO_PATH[dataset] + 'bin_metrics.tsv', sep='\t')
        df = calc_num_recovered_genomes(pd_bins, MIN_RECALL_LIST, MAX_CONTAMINATION_LIST)
        if dataset == 'str_ma':
            gs = 408
        else:
            gs = df[df[TOOL] == 'Gold standard'][MIN_RECALL].values[0]
        df[MIN_RECALL] = df[MIN_RECALL] / gs
        df = df[df[TOOL] != 'Gold standard']

        resultspd = pd.read_csv(DATASET_TO_PATH[dataset] + 'results.tsv', sep='\t')
        resultspd = resultspd[[TOOL, F1_SCORE_BP_CAMI1]]
        resultspd = resultspd[resultspd[TOOL] != 'Gold standard']

        df = pd.merge(df, resultspd, on=TOOL)
        df['method'] = df.apply(lambda row: row[TOOL].split(' ')[0], axis=1)

        tools = df.loc[df.groupby('method')[F1_SCORE_BP_CAMI1].idxmax()][TOOL]
        condition = df[TOOL].isin(tools)
        df = df[condition]
        df = df.set_index('method')
        return df[MIN_RECALL].to_frame()

    pdres = pd.concat([readfile(dataset).rename(columns={MIN_RECALL: dataset + MIN_RECALL}) for dataset in datasets], axis=1)
    return pdres


def main():
    pdres_u = get_pds_unranked(DATASETS)
    pdres_u = pdres_u.set_index([TOOL, 'dataset'])

    hqbins = load_hq_bins(DATASETS)
    hqbins = hqbins.set_index([TOOL, 'dataset'])

    pdres_u = pd.concat([pdres_u, hqbins], axis=1).reset_index()

    pdres = get_pds(DATASETS)

    hq_bins_best = load_hq_bins_best(DATASETS)

    pdres = pd.concat([pdres, hq_bins_best], axis=1)

    pdres['sum'] = pdres[[dataset + metric_r for dataset in DATASETS[:4] for metric_r in METRICS_R]].sum(axis=1)
    sortedpd = pdres.sort_values(by=['sum'])
    pd_mar_str = sortedpd[[dataset + metric_r for dataset in DATASETS[:4] for metric_r in METRICS_R]]
    nan_methods = pd_mar_str.loc[pd_mar_str.isnull().any(axis=1)].index.to_list()
    not_nan_methods = pd_mar_str.loc[~pd_mar_str.isnull().any(axis=1)].index.to_list()
    pdres = pdres.reindex(not_nan_methods + nan_methods)

    pdres2 = get_pds(DATASETSB)
    pdres2 = pdres2.reindex(not_nan_methods + nan_methods)

    pastels = matplotlib.cm.get_cmap('Set3')
    cat_colors = [pastels(x) for x in np.linspace(0, 1, 12)][:len(pdres)]
    cat_colors = sns.color_palette(cat_colors, desat=.75)
    pdres['color'] = cat_colors
    pdres2['color'] = cat_colors

    plotcols = [{'label': 'Completeness (%)', 'metric': 'recall_bp', 'metric_': AVG_RECALL_BP_CAMI1},
                {'label': 'Purity (%)', 'metric': 'precision_bp', 'metric_': AVG_PRECISION_BP},
                {'label': 'ARI (%)', 'metric_': ARI_BY_BP},
                {'label': 'Binned bp (%)', 'metric_': PERCENTAGE_ASSIGNED_BPS},
                {'label': 'HQ genomes (%)', 'metric_': MIN_RECALL}]

    num_cols = 5
    num_rows = 7
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(8, 11), sharex=True)
    go(pdres, plotcols, DATASETS, 0, axs, num_rows, pdres_u)
    plt.subplots_adjust(wspace=0.1, hspace=0.105)
    fig.savefig(DATASET_TO_PATH['mar_gsa'] + 'boxplots.pdf', dpi=100, format='pdf', bbox_inches='tight')
    plt.close()

    # num_rows = 4
    # fig, axs = plt.subplots(num_rows, num_cols, figsize=(8, 6.37), sharex=True)
    # # go(pdres, plotcols, DATASETS, 0, axs, num_rows, pdres_u)
    # go(pdres2, plotcols, DATASETSB, 0, axs, num_rows)
    # plt.subplots_adjust(wspace=0.1, hspace=0.105)
    # fig.savefig(DATASET_TO_PATH['mar_gsa'] + 'boxplots2.pdf', dpi=100, format='pdf', bbox_inches='tight')
    # plt.close()

    print('done')


if __name__ == "__main__":
    main()
