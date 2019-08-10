from os import path

# Define paths for input and output
configfile: "config/config.yaml"

# The absolute path of the program
cd = path.dirname(path.abspath(__name__))


dataset = config["dataset"]
pooled_dataset = "{}_pooled".format(dataset)

fq_dir = config["fq_dir"]
proj_dir = path.join(config["out_dir"], dataset)

out_data_dir = path.join(proj_dir, "data")

qc_dir = path.join(out_data_dir, "qc_fq")
reports_dir = path.join(proj_dir, "reports")
results_dir = path.join(proj_dir, "results")

samples, = glob_wildcards(fq_dir + "/{sample}_reads.fq.gz")
threads = config["threads"]


wildcard_constraints:
    sample = "[^\.\/]+"


def get_fq(wc):
    return [path.join(fq_dir, wc.sample + end + ".fastq.gz") for end in ["_R1", "_R2"]]
