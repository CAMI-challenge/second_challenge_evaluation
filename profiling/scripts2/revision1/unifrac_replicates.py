#!/usr/bin/env python

# This script computes all pairwise weighted UniFrac distances between the human replicate samples
# available in https://qiita.ucsd.edu/study/description/10394.
# Code uses OPAL (https://github.com/CAMI-challenge/OPAL). Please copy it to OPAL's root directory to run it.
# Change the paths below to point to the loaded biom file and saved tsv file.

import biom
import itertools
import pandas as pd
from src.utils import load_data
from src import unifrac_distance as uf
from src.utils import ProfilingTools as PF
import re


ALL_RANKS = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']


def get_samples_from_biom(sample_ids, biom_table):
    samples_list = []
    observations = biom_table.ids(axis='observation')
    for sample_id in sample_ids:
        profile = []
        for obs in observations:
            percentage = float(biom_table.get_value_by_ids(obs_id=obs, samp_id=sample_id))
            if percentage == 0:
                continue

            prediction = load_data.Prediction()
            metadata = biom_table.metadata(id=obs, axis='observation')

            taxpathsn_list = [x for x in metadata['taxonomy'] if x[3:]]
            taxpathsn = '|'.join(taxpathsn_list)

            prediction.taxid = taxpathsn_list[-1]
            prediction.rank = ALL_RANKS[len(taxpathsn_list) - 1]
            prediction.percentage = float(biom_table.get_value_by_ids(obs_id=obs, samp_id=sample_id))

            prediction.taxpath = taxpathsn
            prediction.taxpathsn = taxpathsn
            profile.append(prediction)
        samples_list.append((sample_id, {}, profile))
    return samples_list


def main():
    biom_table1 = biom.load_table('second_challenge_evaluation/profiling/scripts2/revision1/SamplesForUniFracBaseline/105260_species.biom')  # SJII_MG_1-4_RKL0006 (7944)
    biom_table2 = biom.load_table('second_challenge_evaluation/profiling/scripts2/revision1/SamplesForUniFracBaseline/105255_species.biom')  # RKL0006_SJII_5-8_MG_lane1 (7966)

    p = re.compile('^10394\.H1\..*(1week|fresh)')

    sample_ids1 = list(filter(p.match, biom_table1.ids(axis='sample')))
    sample_ids2 = list(filter(p.match, biom_table2.ids(axis='sample')))

    samples_list = get_samples_from_biom(sample_ids1, biom_table1)
    samples_list += get_samples_from_biom(sample_ids2, biom_table2)

    sampleid_to_profile = {}

    print('done loading')

    load_data.normalize_samples(samples_list)
    print('done normalizing')

    for sample in samples_list:
        sample_id, sample_metadata, profile = sample
        sampleid_to_profile[sample_id] = PF.Profile(sample_metadata=sample_metadata, profile=profile)
    print('done 3')

    sample_ids_combinations = list(itertools.combinations(sample_ids1 + sample_ids2, 2))

    samples12_to_unifrac = {}
    for i, (sample1, sample2) in enumerate(sample_ids_combinations):
        print(i)
        samples12_to_unifrac[(sample1, sample2)] = uf.compute_unifrac(sampleid_to_profile[sample1], sampleid_to_profile[sample2])[0]

    df = pd.DataFrame.from_dict(samples12_to_unifrac, orient='index')
    df.to_csv('second_challenge_evaluation/profiling/scripts2/revision1/SamplesForUniFracBaseline/unifrac_human__fresh_1week.tsv', sep='\t')
    print(df.describe())


if __name__ == "__main__":
    main()
