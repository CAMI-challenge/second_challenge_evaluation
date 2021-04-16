import pandas as pd
import numpy as np
import os


pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)


RANKS = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain']

METRICS = ['Completeness', 'Purity', 'F1 score', 'L1 norm error', 'Bray-Curtis distance', 'Shannon equitability'] # 'Weighted UniFrac error'

DECIMALS = {'Completeness': 1, 'Purity': 1, 'F1 score': 1, 'L1 norm error': 2, 'Bray-Curtis distance': 2, 'Shannon equitability': 2}
DECIMALS.update({metric + rank: DECIMALS[metric] for metric in METRICS for rank in RANKS + ['avg']})
DECIMALS['Weighted UniFrac error'] = 2

# ASCENDING = ['L1 norm error', 'Bray-Curtis distance', 'Shannon equitability', 'Weighted UniFrac error']
DESCENDING = ['Completeness', 'Purity', 'F1 score']
DESCENDING += [metric + rank for rank in RANKS for metric in DESCENDING]

pd.set_option('display.max_columns', 999)
pd.set_option('display.max_rows', 100)


def load_results(path):
    pdres = pd.read_csv(path + 'results.tsv', sep='\t')
    # Gold standard is used to compute difference in alpha diversity, so leave it for now
    # pdres = pdres[pdres['tool'] != 'Gold standard']

    tools = sorted(pdres['tool'].unique(), key=str.casefold)
    pdres = pdres.groupby(['rank', 'tool', 'metric'], sort=False).mean().reset_index()
    formattepd = pd.DataFrame()

    for tool in tools:
        toolpd = pd.DataFrame()
        for metric in METRICS:
            values = []
            colnames = []
            for rank in RANKS:
                xx = pdres[(pdres['tool'] == tool) & (pdres['metric'] == metric) & (pdres['rank'] == rank)]
                if metric == 'L1 norm error' or metric == 'Bray-Curtis distance' or metric == 'Shannon equitability':
                    values.append(xx['value'].values[0] if not xx['value'].empty else None)
                else:
                    values.append(xx['value'].values[0] * 100 if not xx['value'].empty else None)
                colnames.append(metric+rank)
                if rank == 'species':
                    if metric == 'L1 norm error' or metric == 'Bray-Curtis distance':
                        xx = [xx for xx in values if xx is not None]
                    else:
                        xx = [xx if xx is not None else 0 for xx in values]
                    average = sum(xx) / len(xx)
                    values.append(average)
                    colnames.append(metric+'avg')
            mpd = pd.DataFrame([values], columns=colnames)
            toolpd = pd.concat([toolpd, mpd], axis=1)

        xx = pdres[(pdres['tool'] == tool) & (pdres['metric'] == 'Weighted UniFrac error') & (pdres['rank'] == 'na')]
        toolpd['Weighted UniFrac error'] = xx['value'].values[0]
        toolpd['tool'] = tool

        formattepd = pd.concat([formattepd, toolpd])

    formattepd = formattepd.set_index('tool')
    for rank in RANKS: # + ['avg']
        formattepd['Shannon equitability' + rank] -= formattepd.loc['Gold standard']['Shannon equitability' + rank]
        formattepd['Shannon equitability' + rank] = formattepd['Shannon equitability' + rank].abs()

    def shannon_avg(row):
        shannon_list = [row['Shannon equitability' + rank] for rank in RANKS[:7] if not np.isnan(row['Shannon equitability' + rank])]
        return sum(shannon_list) / len(shannon_list)

    def f1_avg(row):
        return 2 * row['Purityavg'] * row['Completenessavg'] / (row['Purityavg'] + row['Completenessavg'])
    formattepd['Shannon equitabilityavg'] = formattepd.apply(lambda row: shannon_avg(row), axis=1)
    formattepd['F1 scoreavg'] = formattepd.apply(lambda row: f1_avg(row), axis=1)
    formattepd = formattepd.drop('Gold standard').reset_index()

    float_cols = formattepd.columns[1:]
    formattepd[float_cols] = formattepd[float_cols].astype('float64')
    return formattepd.round(DECIMALS)


def append_stats(formattepd, bestpd):
    bestpd = bestpd.drop(index='mOTUs 2.0.1_1')

    mean_series = pd.DataFrame(bestpd.mean()).T.round(DECIMALS).iloc[0]
    sem_series = pd.DataFrame(bestpd.sem()).T.round(DECIMALS).iloc[0]
    var_series = pd.DataFrame(bestpd.var()).T.round(DECIMALS).iloc[0]
    std_series = pd.DataFrame(bestpd.std()).T.round(DECIMALS).iloc[0]

    return formattepd.append(pd.DataFrame([mean_series, sem_series, var_series, std_series],
                               index=['Average', 'Standard error of the mean', 'Variance', 'Standard deviation'],
                               columns=formattepd.columns))


def compute_rankings(pdres, ranked_cols):
    pdres['method'] = pdres.apply(lambda row: row['tool'].split(' ')[0] + ' cami1' if 'cami1' in row['tool'] else row['tool'].split(' ')[0], axis=1)
    pdres.loc[pdres[pdres['tool'] == 'mOTUs 2.0.1_1'].index[0], 'method'] = 'mOTUs 2.0.1'
    pdres = pdres.set_index('tool')

    pdcopy = pdres.apply(lambda x: x.fillna(0 if x.name in DESCENDING else 9999999), axis=0)

    # Compute scores for all results, keep only best per method, and recompute
    for i in [0, 1]:
        for metric in METRICS:
            for rank in RANKS[:-1]:
                pdcopy = pdcopy.loc[pdres.index]
                pdres[metric + rank + 'score'] = pdcopy[metric + rank].rank(method='min', ascending=False if metric in DESCENDING else True, na_option='bottom') - 1
        pdres['Weighted UniFrac error' + 'score'] = pdres['Weighted UniFrac error'].rank(method='min', ascending=True, na_option='bottom') - 1
        pdres['sum'] = pdres[ranked_cols].sum(axis=1)
        pdres = pdres.loc[pdres.groupby('method')['sum'].idxmin()]

    return pdres


def save_ranked(rankedpd, filename):
    rankedpd = rankedpd.copy()
    pdlist = []
    for metric in METRICS:
        cols = [metric + rank + 'score' for rank in RANKS[:-1]]
        rankedpd[metric] = rankedpd[cols].sum(axis=1)
        pdlist.append(pd.DataFrame(["%s (%i)" % (idx, pos) for idx, pos in rankedpd[metric].sort_values().iteritems()], columns=[metric]))
    metric = 'Weighted UniFrac error'
    pdlist.append(pd.DataFrame(["%s (%i)" % (idx, pos) for idx, pos in rankedpd[metric + 'score'].sort_values().iteritems()], columns=[metric]))
    metric = 'sum'
    pdlist.append(pd.DataFrame(["%s (%i)" % (idx, pos) for idx, pos in rankedpd[metric].sort_values().iteritems()], columns=[metric]))
    pd.concat(pdlist, axis=1).to_csv(filename, sep='\t', index=False)


def rank_across_datasets(df1, df2, filename):
    common = set(df1['method']).intersection(set(df2['method']))

    df1 = df1[df1['method'].isin(common)]
    df2 = df2[df2['method'].isin(common)]

    dfx = pd.concat([df1, df2]).groupby('method').sum()
    dfx = dfx.loc[dfx.groupby('method')['sum'].idxmin()]

    save_ranked(dfx, filename)


def main():
    results = ['../marine_dataset/results/OPAL_short_long_noplasmids/',
               '../marine_dataset/results/OPAL_short_long_noplasmids_normalized_filtered/',
               '../strain_madness_dataset/results/OPAL_short_long/',
               '../strain_madness_dataset/results/OPAL_short_long_normalized_filtered/']

    ranked_cols = [metric+rank + 'score' for metric in METRICS for rank in RANKS[:-1]] + ['Weighted UniFrac error' + 'score']
    best_list = []
    for path in results:
        formattepd = load_results(path)

        rankedpd = compute_rankings(formattepd, ranked_cols)
        save_ranked(rankedpd[ranked_cols + ['sum']], os.path.join(path, 'rankings.tsv'))

        formattepd = formattepd.set_index('tool')
        avg_cols = [metric + rank for metric in METRICS for rank in RANKS[:-1] + ['avg'] + [RANKS[-1]]] + ['Weighted UniFrac error']
        formattepd = append_stats(formattepd[avg_cols], rankedpd[avg_cols])
        formattepd.to_csv(os.path.join(path, 'formatted_results.tsv'), sep='\t')

        best_list.append(rankedpd[ranked_cols + ['method'] + ['sum']])

    rank_across_datasets(best_list[0], best_list[2], os.path.join('../', 'rankings_across_marine_strain_madness.tsv'))
    rank_across_datasets(best_list[1], best_list[3], os.path.join('../', 'rankings_across_marine_strain_madness_normalized_filtered.tsv'))


if __name__ == "__main__":
    main()
