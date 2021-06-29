## Profiling and assembly pipelines on CAMI datasets

> The binning pipeline will be included soon

### Prerequirements

To reproduce the output, you need to use `Bioconda`.

Please follow the instruction [here](https://bioconda.github.io) to install `Bioconda`. 
And then you need to install `snakemake` and Python package `click`:

```shell
conda install snakemake=5.5.4
conda install Click=7.0
```

After this has been done, download the pipeline onto your system:

```shell
git clone git@github.com:hzi-bifo/cami2_pipelines.git
```

### Modify the config file: `config/config.yaml
All the paths must be either relative path to the parent directory of `config` folder or absolute path.

```yaml
dataset: marine
fq_dir: ../datasets/marine/reads/short
out_dir: ../outputs
profile_db_dir: <path to install the Kraken2 database> # not required by assembly
profile_conda_env: config/conda_env.yaml
assembly_conda_env: config/conda_assembly.yaml
binning_conda_env: config/conda_binning.yaml
nodedmp: ../cami_dbs/ncbi_taxonomy/nodes.dmp
threads: 20
```


### Run the pipelines

The parameters for `run_benchmark.py`:
```
Usage: run_benchmark.py [OPTIONS]

  Benchmarking for CAMI dataset

Options:
  -e, --evaluation [all|profile|assembly]
                                  The evaluation to run.  [required]
  -t, --threads INTEGER           The number of threads to use.  [default: 2]
  -d, --dryrun                    Print the details without run the pipeline.
                                  [default: False]
  -c, --conda_prefix PATH         The prefix of conda ENV. [default: in the
                                  working directory].
  -o, --out_dir PATH              The directory for outputs. The path can be
                                  specified either in the CLI here as option
                                  or in the config file.
  --version                       Print the version.
  --help                          Show this message and exit.
```

If you do not want to create the conda ENV in the working directory, 
please use -c parameter to specify the desired path to create the `conda` ENVs. 
The `conda` ENVs will be created under the path of the program by default. 
The program may take ten minutes to create the ENV for the first time.

#### Run the profiling pipeline
```shell
python3 run_benchmark.py -e profile -t 20
```

#### Run the assembly pipeline
```shell
python3 run_benchmark.py -e assembly -t 20
```


#### All in one:
```shell
python3 run_benchmark.py -e all -t 20
```

### The output structure

```
outputs
└── marine
    ├── data
    │   └── qc_fq
    ├── reports
    │   ├── benchmarks
    │   ├── fastp
    │   └── profile
    └── results
        ├── assembly
        │   ├── abyss
        │   ├── megahit
        │   └── ray
        └── profile
            ├── kraken2
            └── motus
```

### Utilities included in this repo
There are some useful programs distributed along with the pipelines, please check [here](bin/README.md)
