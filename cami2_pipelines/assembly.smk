include: "share/load_config.smk"

# Define paths for input and output
assemblers = ["metaspades", "megahit", "ray", "idba", "abyss"]

assembly_dir = path.join(results_dir, "assembly")
conda_env = config["assembly_conda_env"]

rule all:
    input:
        assembly = expand(
            assembly_dir + "/{assembler}/{data}.{assembler}.scaffolds.fa",
            data=pooled_dataset,
            assembler=assemblers)

include: "share/fastp.smk"
include: "share/pool_fq.smk"

rule metaspades:
    input:
        r1 = rules.pool_reads.output.pr1,
        r2 = rules.pool_reads.output.pr2
    output:
        scaffolds = assembly_dir + \
            "/metaspades/{data}/scaffolds.fasta",
        renamed_scaffolds = assembly_dir + \
            "/metaspades/{data}.metaspades.scaffolds.fa"
    conda: conda_env
    params:
        outdir = assembly_dir + "/metaspades/{data}"
    threads: threads
    benchmark:
        reports_dir + \
            "/benchmarks/{data}.metaspades.benchmark.txt"
    shell:
        """
        metaspades.py -k 21,33,55,77 -1 {input.r1} \
            -2 {input.r2} -o {params.outdir} -t {threads}
        cp {output.scaffolds} {output.renamed_scaffolds}
        """


rule megahit:
    input:
        r1 = rules.pool_reads.output.pr1,
        r2 = rules.pool_reads.output.pr2
    output:
        scaffolds = assembly_dir + \
            "/megahit/{data}/{data}.megahit.contigs.fa",
        renamed_scaffolds = assembly_dir + \
            "/megahit/{data}.megahit.scaffolds.fa"
    conda: conda_env
    benchmark:
        reports_dir + "/benchmarks/{data}.megahit.benchmark.txt"
    params:
        megahit_out = assembly_dir + "/megahit/{data}",
        prefix = "{data}.megahit"
    threads: threads
    shell:
        """
        megahit -t {threads} --continue --k-min 21 --k-max 151 -1 {input.r1} \
            -2 {input.r2} -o {params.megahit_out}  --out-prefix {params.prefix}
        cp {output.scaffolds} {output.renamed_scaffolds}
        """
        # rm -rf {params.megahit_out}


rule ray:
    input:
        r1 = rules.pool_reads.output.pr1,
        r2 = rules.pool_reads.output.pr2
    output:
        scaffolds = assembly_dir + "/ray/{data}/Scaffolds.fasta",
        renamed_scaffolds = assembly_dir + "/ray/{data}.ray.scaffolds.fa"
    conda: conda_env
    benchmark:
        reports_dir + "/benchmarks/{data}.ray.benchmark.txt"
    params:
        ray_out = assembly_dir + "/ray/{data}"
    threads: threads
    shell:
        """
        rm -rf {params.ray_out}
        mpiexec -n {threads} Ray -k31 -p {input.r1} {input.r2} -o {params.ray_out}
        cp {output.scaffolds} {output.renamed_scaffolds}
        """

rule idba:
    input:
        r1 = rules.pool_reads.output.pr1,
        r2 = rules.pool_reads.output.pr2
    output:
        merged_pe = qc_dir + "/merged/{data}_12.fa",
        scaffolds = assembly_dir + "/idba/{data}/scaffold.fa",
        renamed_scaffolds = assembly_dir + "/idba/{data}.idba.scaffolds.fa"
    conda: conda_env
    benchmark:
        reports_dir + "/benchmarks/{data}.idba.benchmark.txt"
    params:
        idba_out = assembly_dir + "/idba/{data}"
    threads: threads
    shell:
        """
        rm -rf {params.idba_out}
        fq2fa --merge {input.r1} {input.r2} {output.merged_pe}
        idba_ud -r {output.merged_pe} --num_threads {threads} -o {params.idba_out}
        cp {output.scaffolds} {output.renamed_scaffolds}
        """

rule abyss:
    input:
        r1 = rules.pool_reads.output.pr1,
        r2 = rules.pool_reads.output.pr2
    output:
        scaffolds = assembly_dir + \
            "/abyss/{data}/{data}.abyss-scaffolds.fa",
        renamed_scaffolds = assembly_dir + "/abyss/{data}.abyss.scaffolds.fa"
    conda: conda_env
    benchmark:
        reports_dir + "/benchmarks/{data}.abyss.benchmark.txt"
    params:
        abyss_out = "{data}.abyss",
        abyss_outdir = assembly_dir + "/abyss/{data}"
    threads: threads
    shell:
        """
        abyss-pe np={threads} name={params.abyss_out} k=96 in='{input.r1} {input.r2}'
        mv {params.abyss_out}* {params.abyss_outdir}
        cp {output.scaffolds} {output.renamed_scaffolds}
        """
