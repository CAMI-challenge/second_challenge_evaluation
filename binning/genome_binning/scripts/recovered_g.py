import pandas as pd
import itertools


TOOL = "Tool"
F1_SCORE_BP_CAMI1 = "CAMI 1 F1 score (bp)"
SAMPLE = "Sample"

DATASETS = {'mg': '../marine_dataset/results/amber_marine_nocircular/',
            'mm': '../marine_dataset/results/amber_marine_megahit_nocircular/',
            'sg': '../strain_madness_dataset/results/amber_strain_madness/',
            'sm': '../strain_madness_dataset/results/amber_strain_madness_megahit/',
            'rg': '../plant_associated_dataset/results/amber_rhizosphere_noplasmids/',
            'rh': '../plant_associated_dataset/results/amber_rhizosphere_hybrid_noplasmids/',
            'rm': '../plant_associated_dataset/results/amber_rhizosphere_megahit_noplasmids/'}


MIN_COMPLETENESS = [.5, .7, .9]
MAX_CONTAMINATION = [.1, .05]


def calc_num_recovered_genomes(pd_bins):
    counts_list = []
    for (sample_id, tool), pd_group in pd_bins.groupby(['sample_id', TOOL]):
        for x in itertools.product(MIN_COMPLETENESS, MAX_CONTAMINATION):
            count = pd_group[(pd_group['recall_bp'] > x[0]) & (pd_group['precision_bp'] > (1 - x[1]))].shape[0]
            counts_list.append((sample_id, tool, '> ' + str(int(x[0] * 100)) + '% completeness', '< ' + str(int(x[1] * 100)) + '%', count))

    pd_counts = pd.DataFrame(counts_list, columns=[SAMPLE, TOOL, 'Completeness', 'Contamination', 'count'])
    pd_counts = pd.pivot_table(pd_counts, values='count', index=[SAMPLE, TOOL, 'Contamination'], columns=['Completeness']).reset_index()
    return pd_counts


def load_results(path):
    pd_bins = pd.read_csv(path + 'bin_metrics.tsv', sep='\t')
    df = calc_num_recovered_genomes(pd_bins)

    resultspd = pd.read_csv(path + 'results.tsv', sep='\t')
    resultspd = resultspd[[TOOL, F1_SCORE_BP_CAMI1]]

    df = pd.merge(df, resultspd, on=TOOL)
    df['method'] = df.apply(lambda row: row[TOOL].split(' ')[0], axis=1)

    tools = df.loc[df.groupby('method')[F1_SCORE_BP_CAMI1].idxmax()][TOOL]
    condition = df[TOOL].isin(tools)
    df = df[condition]
    df = df.drop(columns=['Sample', 'Tool', F1_SCORE_BP_CAMI1])
    return df


def go():
    cols = ['> 50% completeness', '> 70% completeness', '> 90% completeness']

    df = pd.concat([load_results(val).rename(columns=dict([(col, idx + col) for col in cols])).
                   set_index(['method', 'Contamination']) for idx, val in DATASETS.items()], axis=1)

    assemblies = ['mg', 'mm', 'sg', 'sm', 'rg', 'rh', 'rm']
    fifty = '> 50% completeness'
    seventy = '> 70% completeness'
    ninety = '> 90% completeness'
    colsx = [x+fifty for x in assemblies]
    colsx += [x+seventy for x in assemblies]
    colsx += [x+ninety for x in assemblies]

    sums = df.groupby('method').sum().sum(axis=1)
    sorted_methods = list(sums.sort_values(ascending=False).index)

    df[colsx].reindex(sorted_methods, level='method').to_csv('../recovered_genomes.tsv', sep='\t')


if __name__ == "__main__":
    go()


