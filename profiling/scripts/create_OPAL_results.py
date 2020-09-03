# same as the shell script, but I like python better
import os
import sys
import subprocess
from pathlib import Path
import shutil

# initial test for creating the figures using OPAL
opal_script = "/home/dkoslicki/Desktop/OPAL/opal.py"  # FIXME: not portable
python_exec = "/home/dkoslicki/anaconda3/envs/OPAL/bin/python"  # FIXME: not portable

# get tool names, version, and anonymous names into arrays
tool_names = []
versions = []
anonymous_names = []
with open("tools.txt", 'r') as fid:
    for line in fid.readlines():
        tool_names.append(line.strip())

with open("versions.txt", 'r') as fid:
    for line in fid.readlines():
        versions.append(line.strip())

with open("anonymous_names.txt", 'r') as fid:
    for line in fid.readlines():
        anonymous_names.append(line.strip())

# Marine short
#dataset = "marine_dataset"  #<----
#submission_type = "short_read_samples"  #<----

OPAL_options = "default"  #<----
for dataset in ["marine_dataset", "strain_madness_dataset"]:
    for submission_type in ["short_read_samples", "long_read_samples", "assembly_or_averaged"]:
        base = str(Path(os.path.abspath(os.path.join(__file__, os.pardir))).parent) + f"/{dataset}/"
        opal_out = f"{base}/results/OPAL_{OPAL_options}_{submission_type}"
        if "marine" in dataset:
            ground_truth = f"{base}/data/ground_truth/gs_marine_short.profile"
        else:
            ground_truth = f"{base}/data/ground_truth/gs_strain_madness_short_long.profile"


        ## default args
        plotLabel = f"{dataset}, {submission_type}"

        # Look for results to evaluate
        # NOTE! This looks in a specific sub-directory
        to_evaluate = []
        labels = []
        for i in range(len(anonymous_names)):
            anonymous_name = anonymous_names[i]
            file_name = os.path.join(base, "data/submissions", submission_type, anonymous_name + ".profile")
            #print(file_name)
            if os.path.exists(file_name):
                #print(anonymous_name)
                to_evaluate.append(file_name)
                labels.append(f"{tool_names[i]}_{versions[i]}_{i}")  # FIXME: stupid "_{i}" on the end since OPAL wants unique labels

        # Delete results if they exist
        shutil.rmtree(opal_out, ignore_errors=True)

        # Run OPAL
        to_run = f"{python_exec} {opal_script} -g {ground_truth} -o {opal_out} -d \"{plotLabel}\"" \
                 f" -l \"{','.join(labels)}\" {' '.join(to_evaluate)}"
        print(" ")
        print(f"{dataset}, {submission_type}:")
        res = subprocess.run(to_run, shell=True)
        #print(to_run)


