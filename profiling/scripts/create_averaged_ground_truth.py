# This script will take the ground truths and average them PER RANK
import os
import sys
import subprocess
from pathlib import Path
import numpy as np
import shutil
# FIXME: for local testing
try:
    sys.path.append(str(Path(os.path.abspath(os.path.join(__file__, os.pardir))).parent))
except NameError:
    sys.path.append("/home/dkoslicki/Desktop/second_challenge_evaluation/profiling/scripts")

import load_data

ranks = ["superkingdom", "phylum", "class", "order", "family", "genus", "species", "strain"]
dataset = ["marine_dataset", "strain_madness_dataset"][0]
# FIXME: for local testing
try:
    base = str(Path(os.path.abspath(os.path.join(__file__, os.pardir))).parent) + f"/{dataset}/"
except NameError:
    base = "/home/dkoslicki/Desktop/second_challenge_evaluation/profiling/" + f"/{dataset}/"
if "marine" in dataset:
    ground_truth = f"{base}/data/ground_truth/gs_marine_short.profile"
else:
    ground_truth = f"{base}/data/ground_truth/gs_strain_madness_short_long.profile"

# read in the profiles and average per rank (mean)
sample_list = load_data.open_profile_from_tsv(ground_truth, False)

average_rank_to_tax_id_to_percentage = {}
for rank in ranks:
    average_rank_to_tax_id_to_percentage[rank] = dict()

# now loop over all samples, get the percentages and stick them in
for i in range(len(sample_list)):
    profile = sample_list[i][2]  # third entry is the actual prediction/sample/profile data structure
    # get all the ranks, tax IDs and percentages for this profile
    profile_percentages = load_data.get_rank_to_taxid_to_percentage(profile)
    for rank in ranks:
        if rank in profile_percentages:
            # get the actual predictions
            tax_id_to_percentage = profile_percentages[rank]
            for (tax_id, percentage) in tax_id_to_percentage.items():
                # If tax_id not in average, populate it and make it a list
                if tax_id not in average_rank_to_tax_id_to_percentage[rank]:
                    average_rank_to_tax_id_to_percentage[rank][tax_id] = [percentage]
                else:  # just add it
                    average_rank_to_tax_id_to_percentage[rank][tax_id].append(percentage)

# then do the actual averaging
num_samples = len(sample_list)
for rank in ranks:
    for tax_id in average_rank_to_tax_id_to_percentage[rank].keys():
        average_rank_to_tax_id_to_percentage[rank][tax_id] = np.sum(average_rank_to_tax_id_to_percentage[rank][tax_id]) / float(num_samples)

# Now to somehow export this