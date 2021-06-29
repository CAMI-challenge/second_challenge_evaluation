include: "share/load_config.smk"

conda_env = config["profile_conda_env"]

profile_dir = path.join(results_dir, "profile")

# "kraken2", "motus", "clark", "kaiju"
profilers = ["kraken2", "motus"]
motus_levels = "class order family genus mOTU"
converted_motus_levels = ["class", "order", "family", "genus"]
bracken_levels = "class order family genus species"
db_dir = config["profile_db_dir"]
#nodedmp = config["nodedmp"]

rule all:
    input:
        # profile = expand(
        #     profile_dir + "/{profiler}/{sample}.{profiler}.genus.profile", sample=samples, profiler=profilers)
        cami_profile = expand(profile_dir + "/{profiler}/{sample}.{profiler}.cami.profile",
                              profiler=profilers, sample=samples),
        multisample_cami_profile = expand(profile_dir + "/{dataset}.{profiler}.cami.profile",
                                          dataset=dataset, profiler=profilers)

include: "share/fastp.smk"

# By default only use Kraken2
rule kraken2_build:
    input: cd + "./profiling.smk"
    output: db_dir + "/kraken2_st/hash.k2d"
    params: db = db_dir + "/kraken2_st"
    threads: threads
    conda: conda_env
    benchmark: reports_dir + "/benchmarks/kraken2_build.txt"
    shell: "kraken2-build --standard --use-ftp --threads {threads} --db {params.db}"


rule kraken2:
    input:
        r1 = rules.fastp.output.or1,
        r2 = rules.fastp.output.or2,
        dbcomplete = rules.kraken2_build.output
    output:
        kraken2_out = profile_dir + "/kraken2/raw/{sample}.kraken.out",
        normal_report = profile_dir + "/kraken2/{sample}.kraken2_normal.report"
    params:
        db = rules.kraken2_build.params.db,
        clf = profile_dir + "/kraken2/raw/{sample}.clf#.fq",
        unclf = profile_dir + "/kraken2/raw/{sample}.unclf#.fq"
    threads: threads
    conda: conda_env
    benchmark: reports_dir + "/benchmarks/{sample}.kraken2.txt"
    shell:
        """
        kraken2 --db {params.db} --threads {threads} --paired {input.r1} {input.r2} \
            --unclassified-out {params.unclf} --classified-out {params.clf} --output {output.kraken2_out} \
            --report {output.normal_report}
        """

rule bracken_build2:
    input: rules.kraken2_build.output
    output: db_dir + \
        "/kraken2_st/database{}mers.kmer_distrib".format(read_length)
    params:
        db = rules.kraken2_build.params.db,
        read_len = read_length
    threads: threads
    conda: conda_env
    benchmark: reports_dir + "/benchmarks/bracken_build2.txt"
    shell:
        """
        if [ ! -f {params.db}/database.kraken]; then
            kraken2 --db {params.db} --threads {threads} <( find -L {params.db}/library /(-name "*.fna" -o -name "*.fasta" -o \
            -name "*.fa" /) -exec cat {{}} + ) > {params.db}/database.kraken
        fi
        kmer2read_distr --seqid2taxid {params.db}/seqid2taxid.map --taxonomy {params.db}/taxonomy \
            --kraken {params.db}/database.kraken --output {params.db}/database{params.read_len}mers.kraken -k 35 \
                -l {params.read_len} -t {threads}
        generate_kmer_distribution.py -i {params.db}/database{params.read_len}mers.kraken \
            -o {params.db}/database{params.read_len}mers.kmer_distrib
        """


rule bracken2:
    input:
        dbcomplete = rules.bracken_build2.output,
        k2_report = rules.kraken2.output.normal_report
    output:
        profile = expand(
            profile_dir + "/kraken2/{{sample}}.kraken2.{levels}.profile", levels=bracken_levels.split())
    params:
        db = rules.kraken2_build.params.db,
        prefix = profile_dir + "/kraken2/{sample}.kraken2",
        levels = bracken_levels,
        read_len = read_length
    threads: threads
    conda: conda_env
    benchmark: reports_dir + "/benchmarks/{sample}.bracken2.txt"
    shell:
        """
        declare -A levels=( ["species"]="S" ["genus"]="G" ["family"]="F" ["order"]="O" ["class"]="C")
        for level in {params.levels}
        do
            bracken -d {params.db} -t {threads} -i {input.k2_report} -o {params.prefix}.${{level}}.profile \
                -r {params.read_len} -l ${{levels[$level]}}
        done
        """

rule motus:
    input:
        r1 = rules.fastp.output.or1,
        r2 = rules.fastp.output.or2
    output:
        expand(profile_dir +
               "/motus/{{sample}}.motus.{levels}.profile", levels=motus_levels.split())
    params:
        prefix = profile_dir + "/motus/{sample}.motus",
        levels = motus_levels
    threads: threads
    conda: conda_env
    benchmark: reports_dir + "/benchmarks/{sample}.motus.txt"
    shell:
        """
        for level in {params.levels}
        do 
            motus profile -t {threads} -f {input.r1} -r {input.r2} -k $level -o {params.prefix}.${{level}}.profile
        done
        """

rule convert_format:
    input:
        lambda wc: expand(profile_dir + "/{{profiler}}/{{sample}}.{{profiler}}.{level}.profile",
                          level=bracken_levels.split() if wc.profiler == "kraken2" else converted_motus_levels)
        # bracken2 = expand(
        #     profile_dir + "/{{profiler}}/{{sample}}.{{profiler}}.{level}.profile", level=bracken_levels.split()),
        # motus = expand(
        #     profile_dir + "/motus/{{sample}}.motus.{level}.profile", level=converted_motus_levels)
    output:
        profile_dir + "/{profiler}/{sample}.{profiler}.cami.profile",
        #bracken2 = profile_dir + "/kraken2/{sample}.kraken2.cami.profile",
        #motus = profile_dir + "/motus/{sample}.motus.cami.profile"
    #conda: conda_env
    params:
        converter = path.join(cd, "bin/tocami.py"),
        taxdmp = config["taxdmp"],
        taxdb = config["taxdb"],
        input_format = lambda wc: "bracken" if wc.profiler == "kraken2" else "motus"
    threads: threads
    shell:
        """
        python3 {params.converter} -f {params.input_format} -s {wildcards.sample} \
            <(cat {input}) -o {output} -t {params.taxdmp} -d {params.taxdb}
        """


rule cat_profile:
    input:
        expand(profile_dir + "/{{profiler}}/{sample}.{{profiler}}.cami.profile",
               sample=samples)
    output:
        profile_dir + \
            "/{}.{{profiler}}.cami.profile".format(dataset)
    shell:
        """
        cat {input} > {output}
        """


# rule validate_taxid:
#     input:
#         expand(profile_dir + "/{profiler}/{sample}.{profiler}.cami.profile",
#                profiler=profilers, sample=samples)
#     output:
#         expand(profile_dir + "/{profiler}/{sample}.{profiler}.cami.valid.profile",
#                profiler=profilers, sample=samples)
#     log:
#         reports_dir + "/profile/validate_taxid.log"
#     params:
#         validator = path.join(cd, "bin/rm_invalid_taxa.py"),
#         nodedmp = nodedmp
#     threads: threads
#     shell:
        # """
        # python3 {params.validator} -n {params.nodedmp} {input} > {log}
        # """
