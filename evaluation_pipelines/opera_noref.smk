include: "share/load_config.smk"

# Define paths for input and output
pooled_assemblers = ["operams_pooled_noref"] #, "idba"]
single_assemblers = ["operams_single_noref"]

assembly_dir = path.join(results_dir, "assembly")
conda_env = config["assembly_conda_env"]
long_fq_dir = config["long_fq_dir"]

rule all:
    input:
        single_assembly = expand(
            assembly_dir + "/{assembler}/{sample}.{assembler}.scaffolds.fa",
            sample=samples,
            assembler=single_assemblers),
        assembly = expand(
            assembly_dir + "/{assembler}/{data}.{assembler}.scaffolds.fa",
            data=pooled_dataset,
            assembler=pooled_assemblers)

include: "share/fastp.smk"
include: "share/pool_fq.smk"


rule operams_single_noref:
    input:
        r1 = rules.fastp.output.or1,
        r2 = rules.fastp.output.or2,
        # long_read = long_fq_dir + "/{sample}" +
    output:
        scaffolds = assembly_dir + \
            "/operams_single_noref/{sample}/contigs.fasta",
        renamed_scaffolds = assembly_dir + "/operams_single_noref/{sample}.operams_single_noref.scaffolds.fa"
    # conda: conda_env
    benchmark:
        reports_dir + "/benchmarks/{sample}.operams_single_noref.benchmark.txt"
    params:
        cd = cd,
        outdir = assembly_dir + "/operams_single_noref/{sample}",
        long_fq_dir = long_fq_dir
    log: reports_dir + "/operams_single_noref/{sample}.err"
    priority: 80
    threads: threads
    shell:
        """
        sample={wildcards.sample}
        long_reads={params.long_fq_dir}/${{sample/short/long}}_reads.fq
        echo $sample
        echo $long_reads
        perl {params.cd}/lib/OPERA-MS-0.8.3/OPERA-MS.pl \
            --short-read1 {input.r1} \
            --short-read2 {input.r2} \
            --long-read $long_reads \
            --no-ref-clustering \
            --no-strain-clustering \
            --num-processors {threads} \
            --out-dir {params.outdir} 2> {log}
        cp {output.scaffolds} {output.renamed_scaffolds}
        """



rule operams_pooled_noref:
    input:
        r1 = rules.pool_reads.output.pr1,
        r2 = rules.pool_reads.output.pr2,
        long_read = rules.pool_long_reads.output.preads
    output:
        scaffolds = assembly_dir + \
            "/operams_pooled_noref/{data}/contigs.fasta",
        renamed_scaffolds = assembly_dir + "/operams_pooled_noref/{data}.operams_pooled_noref.scaffolds.fa"
    # conda: conda_env
    benchmark:
        reports_dir + "/benchmarks/{data}.operams_pooled_noref.benchmark.txt"
    params:
        cd = cd,
        outdir = assembly_dir + "/operams_pooled_noref/{data}"
    log: reports_dir + "/operams_pooled_noref/{data}.err"
    priority: 70
    threads: threads
    shell:
        """
        perl {params.cd}/lib/OPERA-MS-0.8.3/OPERA-MS.pl \
            --short-read1 {input.r1} \
            --short-read2 {input.r2} \
            --long-read {input.long_read} \
            --no-ref-clustering \
            --no-strain-clustering \
            --num-processors {threads} \
            --out-dir {params.outdir} 2> {log}
        cp {output.scaffolds} {output.renamed_scaffolds}
        """

