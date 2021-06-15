import pandas as pd
import numpy as np
import os
from itertools import cycle


TOOL = "Tool"
AVG_RECALL_BP_CAMI1 = "CAMI 1 average completeness (bp)"
AVG_PRECISION_BP = "Average purity (bp)"
ARI_BY_BP = "Adjusted Rand index (bp)"
PERCENTAGE_ASSIGNED_BPS = "Percentage of binned bp"
F1_SCORE_BP_CAMI1 = "CAMI 1 F1 score (bp)"
METRICS = [AVG_RECALL_BP_CAMI1, AVG_PRECISION_BP, ARI_BY_BP, PERCENTAGE_ASSIGNED_BPS]
METRICS_R = [metric + 'rank' for metric in METRICS]

PATHS = ['../marine_dataset/results/amber_marine_nocircular/',
         '../marine_dataset/results/amber_marine_megahit_nocircular/',
         '../strain_madness_dataset/results/amber_strain_madness/',
         '../strain_madness_dataset/results/amber_strain_madness_megahit/']


def get_ranked(results_path, rank_method=False):
    x = pd.read_csv(results_path + 'results.tsv', sep='\t')
    x = x[x[TOOL] != 'Gold standard']
    x = x[[TOOL] + METRICS + [F1_SCORE_BP_CAMI1]]

    if rank_method:
        x['method'] = x.apply(lambda row: row['Tool'].split(' ')[0], axis=1)
        x = x.loc[x.groupby('method')[F1_SCORE_BP_CAMI1].idxmax()].sort_index()

    for metric, metric_r in zip(METRICS, METRICS_R):
        x[metric_r] = x[metric].rank(method='min', ascending=False, na_option='bottom') - 1
    x['sum'] = x[METRICS_R].sum(axis=1)

    if rank_method:
        return x[['method'] + METRICS_R].set_index('method')
    return x.set_index(TOOL)


def rank_dataset(path, outfile):
    pdr = get_ranked(path)

    pdlist = []
    for metric_r in METRICS_R:
        pdlist.append(pd.DataFrame(["%s (%i)" % (idx, pos) for idx, pos in pdr[metric_r].sort_values().iteritems()], columns=[metric_r]))
    metric_r = 'sum'
    pdlist.append(pd.DataFrame(["%s (%i)" % (idx, pos) for idx, pos in pdr[metric_r].sort_values().iteritems()], columns=[metric_r]))
    rankings = pd.concat(pdlist, axis=1)
    rankings.to_csv(path + outfile, sep='\t')


def store_all_scores(pdresults):
    pdresults['score'] = pdresults.sum(axis=1)
    completeness_gsa = ['mar_gsa' + AVG_RECALL_BP_CAMI1 + 'rank', 'str_gsa' + AVG_RECALL_BP_CAMI1 + 'rank']
    completeness_ma = ['mar_ma' + AVG_RECALL_BP_CAMI1 + 'rank', 'str_ma' + AVG_RECALL_BP_CAMI1 + 'rank']
    purity_gsa = ['mar_gsa' + AVG_PRECISION_BP + 'rank', 'str_gsa' + AVG_PRECISION_BP + 'rank']
    purity_ma = ['mar_ma' + AVG_PRECISION_BP + 'rank', 'str_ma' + AVG_PRECISION_BP + 'rank']
    ari_gsa = ['mar_gsa' + ARI_BY_BP + 'rank', 'str_gsa' + ARI_BY_BP + 'rank']
    ari_ma = ['mar_ma' + ARI_BY_BP + 'rank', 'str_ma' + ARI_BY_BP + 'rank']
    percentage_gsa = ['mar_gsa' + PERCENTAGE_ASSIGNED_BPS + 'rank', 'str_gsa' + PERCENTAGE_ASSIGNED_BPS + 'rank']
    percentage_ma = ['mar_ma' + PERCENTAGE_ASSIGNED_BPS + 'rank', 'str_ma' + PERCENTAGE_ASSIGNED_BPS + 'rank']

    pdresults['completeness_gsa'] = pdresults[completeness_gsa].sum(axis=1)
    pdresults['completeness_ma'] = pdresults[completeness_ma].sum(axis=1)
    pdresults['purity_gsa'] = pdresults[purity_gsa].sum(axis=1)
    pdresults['purity_ma'] = pdresults[purity_ma].sum(axis=1)
    pdresults['ari_gsa'] = pdresults[ari_gsa].sum(axis=1)
    pdresults['ari_ma'] = pdresults[ari_ma].sum(axis=1)
    pdresults['percentage_gsa'] = pdresults[percentage_gsa].sum(axis=1)
    pdresults['percentage_ma'] = pdresults[percentage_ma].sum(axis=1)

    pdresults['all_gsa'] = pdresults['completeness_gsa'] + pdresults['purity_gsa'] + pdresults['ari_gsa'] + pdresults['percentage_gsa']
    pdresults['all_ma'] = pdresults['completeness_ma'] + pdresults['purity_ma'] + pdresults['ari_ma'] + pdresults['percentage_ma']

    pdresults['completeness_all'] = pdresults['completeness_gsa'] + pdresults['completeness_ma']
    pdresults['purity_all'] = pdresults['purity_gsa'] + pdresults['purity_ma']
    pdresults['ari_all'] = pdresults['ari_gsa'] + pdresults['ari_ma']
    pdresults['percentage_all'] = pdresults['percentage_gsa'] + pdresults['percentage_ma']

    cols = completeness_gsa + ['completeness_gsa'] + \
        completeness_ma + ['completeness_ma', 'completeness_all'] + \
        purity_gsa + ['purity_gsa'] + \
        purity_ma + ['purity_ma', 'purity_all'] + \
        ari_gsa + ['ari_gsa'] + \
        ari_ma + ['ari_ma', 'ari_all'] + \
        percentage_gsa + ['percentage_gsa'] + \
        percentage_ma + ['percentage_ma', 'percentage_all'] + \
        ['all_gsa', 'all_ma', 'score']

    pdresults = pdresults.sort_values(by='score')
    pdresults[cols].to_csv('../scores_gsa_vs_ma.tsv', sep='\t')


def cross_rank():
    pdres = pd.concat([get_ranked(PATHS[0], True).rename(columns=dict([(col, 'mar_gsa'+col) for col in METRICS_R])),
                       get_ranked(PATHS[1], True).rename(columns=dict([(col, 'mar_ma'+col) for col in METRICS_R])),
                       get_ranked(PATHS[2], True).rename(columns=dict([(col, 'str_gsa'+col) for col in METRICS_R])),
                       get_ranked(PATHS[3], True).rename(columns=dict([(col, 'str_ma'+col) for col in METRICS_R]))], axis=1)
    store_all_scores(pdres.copy())

    nan_methods = pdres.loc[pdres.isnull().any(axis=1)].index.to_list()

    pdres = pd.concat([pdres[['mar_gsa'+col for col in METRICS_R]].rename(columns=dict([('mar_gsa'+col, 'gsa'+col) for col in METRICS_R])),
                       pdres[['str_gsa'+col for col in METRICS_R]].rename(columns=dict([('str_gsa'+col, 'gsa'+col) for col in METRICS_R])),
                       pdres[['mar_ma'+col for col in METRICS_R]].rename(columns=dict([('mar_ma'+col, 'ma'+col) for col in METRICS_R])),
                       pdres[['str_ma'+col for col in METRICS_R]].rename(columns=dict([('str_ma'+col, 'ma'+col) for col in METRICS_R]))])
    pdres = pdres.fillna(0)
    pdres = pdres.groupby(pdres.index).sum()

    pdres['sum'] = pdres.sum(axis=1)
    pdres['gsasum'] = pdres[['gsa'+metric_r for metric_r in METRICS_R]].sum(axis=1)
    pdres['masum'] = pdres[['ma'+metric_r for metric_r in METRICS_R]].sum(axis=1)

    cols = []
    pdlist = []
    for metric_r in METRICS_R + ['sum']:
        for assembly_type in ['gsa', 'ma']:
            pd_col = assembly_type+metric_r
            top = ["%s (%i)" % (idx, pos) for idx, pos in pdres[pd_col].sort_values().iteritems() if idx not in nan_methods]
            bottom = ["%s (%i)" % (idx, pos) for idx, pos in pdres[pd_col].sort_values().iteritems() if idx in nan_methods]
            pdlist.append(pd.DataFrame(top + bottom, columns=[pd_col]))
            cols.append(pd_col)
        pd_col = 'gsa+ma'+metric_r
        pdres[pd_col] = pdres[['gsa'+metric_r, 'ma'+metric_r]].sum(axis=1)
        top = ["%s (%i)" % (idx, pos) for idx, pos in pdres[pd_col].sort_values().iteritems() if idx not in nan_methods]
        bottom = ["%s (%i)" % (idx, pos) for idx, pos in pdres[pd_col].sort_values().iteritems() if idx in nan_methods]
        pdlist.append(pd.DataFrame(top + bottom, columns=[pd_col]))
        cols.append(pd_col)
    pd_col = 'sum'
    top = ["%s (%i)" % (idx, pos) for idx, pos in pdres[pd_col].sort_values().iteritems() if idx not in nan_methods]
    bottom = ["%s (%i)" % (idx, pos) for idx, pos in pdres[pd_col].sort_values().iteritems() if idx in nan_methods]
    pdlist.append(pd.DataFrame(top + bottom, columns=[pd_col]))
    cols.append(pd_col)

    rankings = pd.concat(pdlist, axis=1)
    rankings[cols].to_csv('../rankings_across.tsv', sep='\t')


def main():
    for path in PATHS:
        rank_dataset(path, 'rankings.tsv')

    cross_rank()


if __name__ == "__main__":
    main()
