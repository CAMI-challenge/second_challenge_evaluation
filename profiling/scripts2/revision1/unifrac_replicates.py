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


table = biom.load_table('cami2/second_challenge_evaluation/profiling/scripts2/revision1/SamplesForUniFracBaseline/79884_otu_table.redist.species.biom')

samples = table.ids(axis='sample')

p = re.compile('^10394.H1.*.*.*.II')
samples = [x for x in samples if p.match(x)]  # list(filter(p.match, samples))

observations = table.ids(axis='observation')
sampleid_to_profile = {}
samples_list = []
sample_ids_combinations = list(itertools.combinations(samples, 2))

for sample_id in samples:
    profile = []
    for obs in observations:
        percentage = float(table.get_value_by_ids(obs_id=obs, samp_id=sample_id))
        if percentage == 0:
            continue

        prediction = load_data.Prediction()
        metadata = table.metadata(id=obs, axis='observation')

        taxpathsn_list = [x for x in metadata['taxonomy'] if x[3:]]
        taxpathsn = '|'.join(taxpathsn_list)

        prediction.taxid = taxpathsn_list[-1]
        prediction.rank = ALL_RANKS[len(taxpathsn_list) - 1]
        prediction.percentage = float(table.get_value_by_ids(obs_id=obs, samp_id=sample_id))

        prediction.taxpath = taxpathsn
        prediction.taxpathsn = taxpathsn
        profile.append(prediction)
    samples_list.append((sample_id, {}, profile))
print('done loading')

load_data.normalize_samples(samples_list)
print('done normalizing')

for sample in samples_list:
    sample_id, sample_metadata, profile = sample
    sampleid_to_profile[sample_id] = PF.Profile(sample_metadata=sample_metadata, profile=profile)
print('done 3')

samples12_to_unifrac = {}
for i, (sample1, sample2) in enumerate(sample_ids_combinations):
    print(i)
    samples12_to_unifrac[(sample1, sample2)] = uf.compute_unifrac(sampleid_to_profile[sample1], sampleid_to_profile[sample2])[0]

df = pd.DataFrame.from_dict(samples12_to_unifrac, orient='index')
df.to_csv('second_challenge_evaluation/profiling/scripts2/revision1/SamplesForUniFracBaseline/79884_unifrac_human.tsv', sep='\t')
