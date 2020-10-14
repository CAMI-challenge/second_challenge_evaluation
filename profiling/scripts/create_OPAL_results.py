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

with open("tool_mapping.csv", 'r') as fid:
    for line in fid.readlines():
        line = line.strip()
        anonymous_name, tool_name, version, tool_name_abbrv = line.split(',')
        anonymous_names.append(anonymous_name)
        tool_names.append(tool_name_abbrv)  # Use the abbreviated name for visual clarity
        versions.append(version)

def run_opal(commands, name):
    """
    Gather all the submissions for all datasets, then run OPAL
    :param commands: additional options to pass to OPAL
    :type commands: str
    :param name: Name of the OPAL_options included (will be included in output folder)
    :type name: str
    :return: None
    """
    OPAL_options = name
    for dataset in ["marine_dataset", "strain_madness_dataset"]:
        for submission_type in ["short_read_samples", "long_read_samples", "assembly_or_averaged"]:
            base = str(Path(os.path.abspath(os.path.join(__file__, os.pardir))).parent) + f"/{dataset}/"
            opal_out = f"{base}/results/OPAL_{OPAL_options}_{submission_type}"
            if (submission_type != "assembly_or_averaged") and ("marine" in dataset):
                ground_truth = f"{base}/data/ground_truth/gs_marine_short.profile"  # marine, all samples
            elif (submission_type == "assembly_or_averaged") and ("marine" in dataset):
                ground_truth = f"{base}/data/ground_truth/gs_marine_short_average.profile"  # marine, averaged
            elif (submission_type == "assembly_or_averaged") and ("marine" not in dataset):
                ground_truth = f"{base}/data/ground_truth/gs_strain_madness_short_long_average.profile"  # strain madness, averaged
            else:
                ground_truth = f"{base}/data/ground_truth/gs_strain_madness_short_long.profile"  # strain madness, all samples

            ## default args
            plotLabel = f"{dataset}, {submission_type}"

            # Look for results to evaluate
            # NOTE! This looks in a specific sub-directory
            to_evaluate = []
            labels = []
            for i in range(len(anonymous_names)):
                anonymous_name = anonymous_names[i]
                file_name = os.path.join(base, "data/submissions", submission_type, anonymous_name + ".profile")
                if os.path.exists(file_name):
                    to_evaluate.append(file_name)
                    labels.append(f"{tool_names[i]}")

            # Delete results if they exist
            shutil.rmtree(opal_out, ignore_errors=True)

            # Run OPAL
            to_run = f"{python_exec} {opal_script} -g {ground_truth} -o {opal_out} -d \"{plotLabel}\" {commands}" \
                     f" -l \"{','.join(labels)}\" {' '.join(to_evaluate)}"
            print(" ")
            print(f"{dataset}, {submission_type}:")
            res = subprocess.run(to_run, shell=True)
            #print(to_run)


# Default
run_opal("", "default")
# Normalized
run_opal("-n", "normalized")
# Filtered 1%
run_opal("-f 1", "filtered")
# Normalized and Filtered 1%
run_opal("-n -f 1", "normalized_filtered")

