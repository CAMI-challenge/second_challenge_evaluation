#!/usr/bin/env python3
import labels as c
import pandas as pd
import os
import argparse


METRICS = [c.AVG_RECALL_BP_CAMI1, c.AVG_PRECISION_BP, c.F1_SCORE_BP_CAMI1, c.ARI_BY_BP, c.PERCENTAGE_ASSIGNED_BPS]


def get_pd(results_path):
    pdresults = pd.read_csv(os.path.join(results_path, 'results.tsv'), sep='\t', usecols=[c.TOOL] + METRICS)
    pdresults = pdresults[pdresults[c.TOOL] != 'Gold standard'].set_index('Tool') * 100

    return pdresults.append(pd.DataFrame([pdresults.mean().values, pdresults.sem().values, pdresults.var().values, pdresults.std().values],
                      index=['Average', 'Standard error of the mean', 'Variance', 'Standard deviation'],
                      columns=pdresults.columns))


def average_metrics():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', nargs='+', help='AMBER output directories containing results.tsv')

    for path in parser.parse_args().dir:
        get_pd(path)[METRICS].round(1).to_csv(os.path.join(path, 'formatted.tsv'), sep='\t')


if __name__ == "__main__":
    average_metrics()
