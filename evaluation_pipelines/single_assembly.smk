include: "share/load_config.smk"

# Define paths for input and output
assemblers = ["megahit"]

assembly_dir = path.join(results_dir, "assembly")
# conda_env = config["assembly_conda_env"]
# long_fq_dir = config["long_fq_dir"]

rule all:
    input:
        single_assembly = expand(
            assembly_dir + "/{assembler}/{sample}.{assembler}.scaffolds.fa",
            sample=samples,
            assembler=assemblers)
        # assembly = expand(
        #     assembly_dir + "/{assembler}/{data}.{assembler}.scaffolds.fa",
        #     data=pooled_dataset,
        #     assembler=pooled_assemblers)

include: "share/fastp.smk"
# include: "share/pool_fq.smk"


rule megahit:
    input:
        r1 = rules.fastp.output.or1,
        r2 = rules.fastp.output.or2
    output:
        scaffolds = assembly_dir + \
            "/megahit/{sample}/{sample}.megahit.contigs.fa",
        renamed_scaffolds = assembly_dir + \
            "/megahit/{sample}.megahit.scaffolds.fa"
    # conda: conda_env
    benchmark:
        reports_dir + "/benchmarks/{sample}.megahit.benchmark.txt"
    params:
        megahit_out = assembly_dir + "/megahit/{sample}",
        prefix = "{sample}.megahit"
    threads: threads
    shell:
        """
        rmdir --ignore-fail-on-non-empty {params.megahit_out}
        megahit -t {threads} -1 {input.r1} \
            -2 {input.r2} -o {params.megahit_out}  --out-prefix {params.prefix}
        cp {output.scaffolds} {output.renamed_scaffolds}
        """
