include: "share/load_config.smk"

conda_env = config["profile_conda_env"]

profile_dir = path.join(results_dir, "profile")

# "kraken2", "motus", "clark", "kaiju"
profilers = ["kraken2", "motus"]
motus_levels = "class order family genus mOTU"
converted_motus_levels = ["class", "order", "family", "genus"]
bracken_levels = "class order family genus species"
db_dir = config["profile_db_dir"]
nodedmp = config["nodedmp"]

rule all:
    input:
        # profile = expand(
        #     profile_dir + "/{profiler}/{sample}.{profiler}.genus.profile", sample=samples, profiler=profilers)
        cami_profile = expand(profile_dir + "/{profiler}/{sample}.{profiler}.cami.valid.profile",
                              profiler=profilers, sample=samples)

include: "share/fastp.smk"

# By default only use Kraken2
rule kraken_build:
    input: path.join(fq_dir, samples[0] + "_reads.fq.gz")
    output: db_dir + "/kraken_st/lca.complete"
    params: db = db_dir + "/kraken_st"
    threads: threads
    conda:
        "config/conda_kraken_env.yaml"
    benchmark: reports_dir + "/benchmarks/kraken_build.txt"
    shell: "kraken-build --standard --use-wget --threads {threads} --db {params.db}"

rule kraken2_build:
    input: rules.kraken_build.input
    output: db_dir + "/kraken2_st/hash.k2d"
    params: db = db_dir + "/kraken2_st"
    threads: threads
    conda: conda_env
    benchmark: reports_dir + "/benchmarks/kraken2_build.txt"
    shell: "kraken2-build --standard --use-ftp --threads {threads} --db {params.db}"

rule kraken:
    input:
        r1 = rules.fastp.output.or1,
        r2 = rules.fastp.output.or2,
        dbcomplete = rules.kraken_build.output
    output:
        kraken_out = profile_dir + "/kraken/raw/{sample}.kraken.out",
        normal_report = profile_dir + "/kraken/{sample}.kraken_normal.report",
        clf = profile_dir + "/kraken/raw/{sample}.clf.fq",
        unclf = profile_dir + "/kraken/raw/{sample}.unclf.fq"
    params:
        db = rules.kraken_build.params.db
    threads: threads
    conda:
        "config/conda_kraken_env.yaml"
    benchmark: reports_dir + "/benchmarks/{sample}.kraken.txt"
    shell:
        """
        kraken --db {params.db} --threads {threads} --fastq-input --paired {input.r1} {input.r2} \
            --unclassified-out {output.unclf} --classified-out {output.clf} --output {output.kraken_out}
        kraken-report --db {params.db} {output.kraken_out} > {output.normal_report}
        """

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

# By default Bracken builds the Kraken2 database
rule bracken_build:
    input: rules.kraken_build.output
    output: db_dir + "/kraken_st/bracken_build.complete"
    params: db = rules.kraken_build.params.db
    threads: threads
    conda: conda_env
    benchmark: reports_dir + "/benchmarks/bracken_build.txt"
    shell:
        """
        bracken-build -d {params.db} -t {threads} -k 31 -l 150 -x $(dirname $(which kraken))/
        touch {output}
        """

rule bracken_build2:
    input: rules.kraken2_build.output
    output: db_dir + "/kraken2_st/bracken_build.complete"
    params: db = rules.kraken2_build.params.db
    threads: threads
    conda: conda_env
    benchmark: reports_dir + "/benchmarks/bracken_build2.txt"
    shell:
        """
        kraken2 --db {params.db} --threads {threads} <( find -L {params.db}/library /(-name "*.fna" -o -name "*.fasta" -o \
            -name "*.fa" /) -exec cat {{}} + ) > {params.db}/database.kraken
        kmer2read_distr --seqid2taxid {params.db}/seqid2taxid.map --taxonomy {params.db}/taxonomy \
            --kraken {params.db}/database.kraken --output {params.db}/database150mers.kraken -k 35 -l 150 -t {threads}
        generate_kmer_distribution.py -i {params.db}/database150mers.kraken -o {params.db}/database150mers.kmer_distrib
        touch {output}
        """

rule bracken:
    input:
        dbcomplete = rules.bracken_build.output,
        k_report = rules.kraken.output.normal_report
    output:
        profile = profile_dir + "/kraken/{sample}.kraken.S.profile"
    params:
        db = rules.kraken_build.params.db,
        prefix = profile_dir + "/kraken/{sample}.kraken",
        levels = bracken_levels
    threads: threads
    conda: conda_env
    benchmark: reports_dir + "/benchmarks/{sample}.bracken.txt"
    shell:
        """
        for level in {params.levels}
        do
            bracken -d {params.db} -t {threads} -i {input.k_report} -o {params.prefix}.${{level}}.profile -r 150 -l $level
        done
        """

rule bracken2:
    input:
        dbcomplete = rules.bracken_build2.output,
        k2_report = rules.kraken2.output.normal_report
    output:
        profile = profile_dir + "/kraken2/{sample}.kraken2.genus.profile"
    params:
        db = rules.kraken2_build.params.db,
        prefix = profile_dir + "/kraken2/{sample}.kraken2",
        levels = bracken_levels
    threads: threads
    conda: conda_env
    benchmark: reports_dir + "/benchmarks/{sample}.bracken2.txt"
    shell:
        """
        declare -A levels=( ["species"]="S" ["genus"]="G" ["family"]="F" ["order"]="O" ["class"]="C")
        for level in {params.levels}
        do
            bracken -d {params.db} -t {threads} -i {input.k2_report} -o {params.prefix}.${{level}}.profile -r 150 -l $levels[$level]
        done
        """

rule motus:
    input:
        r1 = rules.fastp.output.or1,
        r2 = rules.fastp.output.or2
    output:
        profile_dir + "/motus/{sample}.motus.genus.profile"
    params:
        prefix = profile_dir + "/motus/{sample}.motus",
        level = motus_levels
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
        bracken2 = expand(
            profile_dir + "/kraken2/{{sample}}.kraken2.{level}.profile", level=bracken_levels.split()),
        motus = expand(
            profile_dir + "/motus/{{sample}}.motus.{level}.profile", level=converted_motus_levels)
    output:
        bracken2 = profile_dir + "/kraken2/{sample}.kraken2.cami.profile",
        motus = profile_dir + "/motus/{sample}.motus.cami.profile"
    params:
        converter = path.join(cd, "bin/tocami.py")
    threads: threads
    shell:
        """
        python3 {params.converter} -f bracken <(cat {input.bracken2}) -o {output.bracken2}
        python3 {params.converter} -f motus <(cat {input.motus}) -o {output.motus}
        """

rule validate_taxid:
    input:
        expand(profile_dir + "/{profiler}/{sample}.{profiler}.cami.profile",
               profiler=profilers, sample=samples)
    output:
        expand(profile_dir + "/{profiler}/{sample}.{profiler}.cami.valid.profile",
               profiler=profilers, sample=samples)
    log:
        reports_dir + "/profile/validate_taxid.log"
    params:
        validator = path.join(cd, "bin/rm_invalid_taxa.py"),
        nodedmp = nodedmp
    threads: threads
    shell:
        """
        python3 {params.validator} -n {params.nodedmp} {input} > {log}
        """
