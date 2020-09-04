import os
import sys
import subprocess
from pathlib import Path
import shutil
sys.path.append(str(Path(os.path.abspath(os.path.join(__file__, os.pardir))).parent))
sys.path.append("/home/dkoslicki/Desktop/second_challenge_evaluation/profiling/scripts")  # FIXME: for local testing
from load_data import open_profile_from_tsv

dataset = ["marine_dataset", "strain_madness_dataset"][0]
base = str(Path(os.path.abspath(os.path.join(__file__, os.pardir))).parent) + f"/{dataset}/"
if "marine" in dataset:
    ground_truth = f"{base}/data/ground_truth/gs_marine_short.profile"
else:
    ground_truth = f"{base}/data/ground_truth/gs_strain_madness_short_long.profile"

# read in the profiles and average per rank (mean)
sample_list = open_profile_from_tsv(ground_truth, False)
