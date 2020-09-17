import click
import logging
from opal import *

import pandas as pd
import seaborn as sns
from src import l1norm as l1

from src import braycurtis as bc
# from src import rankings as rk
# from src import html_opal as html
# from src import plots as pl
from src.utils import load_data


def load_profiles(submission_files, reproduce_files, no_normalization):
    normalize = False if no_normalization else True

    profiles_list = []

    for idx, submission_file in enumerate(submission_files):
        submission_profile = load_data.open_profile(submission_file, normalize)
        sample_profile_dict = {}
        for sample_id, meta, profile in submission_profile:
            sample_profile_dict[sample_id] = {'submission': (meta, profile)}
        profiles_list.append(sample_profile_dict)

    for idx, reproduce_file in enumerate(reproduce_files):
        reproduce_profile = load_data.open_profile(reproduce_file, normalize)
        for sample_id, meta, profile in reproduce_profile:
            if sample_id in profiles_list[idx]:
                profiles_list[idx][sample_id]['reproduce'] = (meta, profile)
            else:
                logging.getLogger('opal').critical(
                    "Sample ID '{}' is not consistent with submission in {}".format(sample_id, reproduce_file))
                exit(1)

    return profiles_list


def compute_metrics(submission_rank_to_taxid_to_percentage, reproduce_rank_to_taxid_to_percentage):

    l1norm = l1.compute_l1norm(
        submission_rank_to_taxid_to_percentage, reproduce_rank_to_taxid_to_percentage)

    # Bray-Curtis
    braycurtis = bc.braycurtis(
        submission_rank_to_taxid_to_percentage, reproduce_rank_to_taxid_to_percentage)

    return l1norm, braycurtis


def reformat_pandas(sample_id, label, braycurtis, l1norm):
    """Reformats metrics data into one unified pandas DataFrame.
    Parameters
    ----------
    sample_id : str
    label : str
        str for tool name.
    braycurtis : float
    l1norm : float
    Returns
    -------
    Pandas.DataFrame with following columns: metric, rank, tool, value
    """
    # convert L1 Norm
    pd_l1norm = pd.DataFrame(
        index=[sample_id], data=l1norm).stack().reset_index()
    pd_l1norm.columns = ['sample', 'rank', 'value']
    pd_l1norm['tool'] = label
    pd_l1norm['metric'] = c.L1NORM

    # convert Bray-Curtis
    pd_braycurtis = pd.DataFrame(
        index=[sample_id], data=braycurtis).stack().reset_index()
    pd_braycurtis.columns = ['sample', 'rank', 'value']
    pd_braycurtis['tool'] = label
    pd_braycurtis['metric'] = c.BRAY_CURTIS

    return pd.concat([pd_braycurtis, pd_l1norm], ignore_index=True, sort=False)


def evaluate(profiles_list, labels):
    pd_metrics = pd.DataFrame()

    # pd_perct = pd.DataFrame()
    perct_dict = {'sample': [], 'rank': [],
                  'taxid': [], 'tool': [],
                  'perct': [], 'type': []}
    one_profile_assessed = False
    for samples_profile, label in zip(profiles_list, labels):
        for sample_id, profiles in samples_profile.items():
            if 'submission' in profiles and 'reproduce' in profiles:
                submission_rank_taxid_percentage = load_data.get_rank_to_taxid_to_percentage(
                    profiles['submission'][1])
                # print(label)
                reproduce_rank_taxid_percentage = load_data.get_rank_to_taxid_to_percentage(
                    profiles['reproduce'][1])

                # print(submission_rank_taxid_percentage)
                for rank, taxid_perct in submission_rank_taxid_percentage.items():
                    # keys, values = zip(*taxid_perct.items())
                    for taxid, perct in taxid_perct.items():
                        perct_dict['sample'].append(sample_id)
                        perct_dict['rank'].append(rank)
                        perct_dict['taxid'].append(taxid)
                        perct_dict['tool'].append(label)
                        perct_dict['perct'].append(perct)
                        perct_dict['type'].append('submission')

                for rank, taxid_perct in reproduce_rank_taxid_percentage.items():
                    for taxid, perct in taxid_perct.items():
                        perct_dict['sample'].append(sample_id)
                        perct_dict['rank'].append(rank)
                        perct_dict['taxid'].append(taxid)
                        perct_dict['tool'].append(label)
                        perct_dict['perct'].append(perct)
                        perct_dict['type'].append('reproduce')

                l1norm, braycurtis = compute_metrics(submission_rank_taxid_percentage,
                                                     reproduce_rank_taxid_percentage
                                                     )
                pd_metrics = pd.concat([pd_metrics, reformat_pandas(
                    sample_id, label, braycurtis, l1norm)], ignore_index=True)
                one_profile_assessed = True

    if not one_profile_assessed:
        logging.getLogger('opal').critical("No profile could be evaluated.")
        exit(1)

    return pd_metrics, pd.DataFrame.from_dict(perct_dict)


@click.command()
@click.option('-s',
              '--submissions',
              type=str,
              required=True,
              help='Comma separated input submission profiles')
@click.option('-r',
              '--reproduces',
              type=str,
              required=True,
              help='Comma separated input reproduced profiles')
@click.option('-l',
              '--labels',
              type=str,
              required=True,
              help='Comma separated labels for profiles')
@click.option('-o',
              '--output',
              type=str,
              required=True,
              help='Prefic for output files')
@click.option('-n',
              '--normalization',
              is_flag=True,
              help='Normalize the abundance profile')
def visualize_reproducibility(submissions, reproduces, labels, output, normalization):
    no_normalization = False if normalization else True
    submission_files = submissions.strip().split(',')
    reproduce_files = reproduces.strip().split(',')

    labels = labels.strip().split(',')

    profiles_list = load_profiles(submission_files,
                                  reproduce_files,
                                  no_normalization=no_normalization)

    reproduce_metrics, taxid_perct = evaluate(profiles_list,
                                              labels)

    reproduce_metrics.to_csv(output + '.rank_L1.tsv', sep='\t', index=False)
    taxid_perct.to_csv(output + '.taxid_perct.tsv', sep='\t', index=False)
    # sns.set_style("white")
    sns.set_style("ticks")
    sns.set_context("paper", rc={"font.size": 12,
                                 "axes.titlesize": 12, "axes.labelsize": 12})

    metric_boxplot = sns.catplot(x='tool',
                                 y='value',
                                 kind="box",
                                 col="rank",
                                 hue="metric",
                                 palette="Set2",
                                 col_wrap=2,
                                 data=reproduce_metrics)

    # print(taxid_perct)

    metric_boxplot.savefig(output + ".png")


if __name__ == "__main__":
    visualize_reproducibility()
