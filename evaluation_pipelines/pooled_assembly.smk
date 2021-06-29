include: "share/load_config.smk"

# Define paths for input and output
pooled_assemblers = ["metaspades", "megahit", "ray", "abyss"]#, "operams_pooled"] #, "idba"]
single_assemblers = ["operams_single"]

assembly_dir = path.join(results_dir, "assembly")
conda_env = config["assembly_conda_env"]
long_fq_dir = config["long_fq_dir"]

rule all:
    input:
#        single_assembly = expand(
#            assembly_dir + "/{assembler}/{sample}.{assembler}.scaffolds.fa",
#            sample=samples,
#            assembler=single_assemblers)
        assembly = expand(
            assembly_dir + "/{assembler}/{data}.{assembler}.scaffolds.fa",
            data=pooled_dataset,
            assembler=pooled_assemblers)

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
    priority: 70
    benchmark:
        reports_dir + \
            "/benchmarks/{data}.metaspades.benchmark.txt"
    shell:
        """
        metaspades.py -k 21,33,55,77 -1 {input.r1} \
            -2 {input.r2} -m 500 -o {params.outdir} -t {threads}
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
    priority: 100
    threads: threads
    shell:
        """
        rmdir --ignore-fail-on-non-empty {params.megahit_out}
        megahit -t {threads} -m 0.8 --k-min 21 --k-max 91 -1 {input.r1} \
            -2 {input.r2} -o {params.megahit_out}  --out-prefix {params.prefix}
        cp {output.scaffolds} {output.renamed_scaffolds}
        """
        # mkdir -p {params.megahit_out}

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
    priority: 50
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
    priority: 80
    shell:
        """
        abyss-pe np={threads} name={params.abyss_out} k=32 in='{input.r1} {input.r2}'
        mv {params.abyss_out}* {params.abyss_outdir}
        cp {output.scaffolds} {output.renamed_scaffolds}
        """

rule operams_single:
    input:
        r1 = rules.fastp.output.or1,
        r2 = rules.fastp.output.or2,
        # long_read = long_fq_dir + "/{sample}" +
    output:
        scaffolds = assembly_dir + \
            "/operams_single/{sample}/contigs.fasta",
        renamed_scaffolds = assembly_dir + "/operams_single/{sample}.operams_single.scaffolds.fa"
    # conda: conda_env
    benchmark:
        reports_dir + "/benchmarks/{sample}.operams_single.benchmark.txt"
    params:
        cd = cd,
        outdir = assembly_dir + "/operams_single/{sample}",
        long_fq_dir = long_fq_dir
    log: reports_dir + "/operams_single/{sample}.err"
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
            --num-processors {threads} \
            --out-dir {params.outdir} 2> {log}
        cp {output.scaffolds} {output.renamed_scaffolds}
        """


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



rule operams_pooled:
    input:
        r1 = rules.pool_reads.output.pr1,
        r2 = rules.pool_reads.output.pr2,
        long_read = rules.pool_long_reads.output.preads
    output:
        scaffolds = assembly_dir + \
            "/operams_pooled/{data}/contigs.fasta",
        renamed_scaffolds = assembly_dir + "/operams_pooled/{data}.operams_pooled.scaffolds.fa"
    # conda: conda_env
    benchmark:
        reports_dir + "/benchmarks/{data}.operams_pooled.benchmark.txt"
    params:
        cd = cd,
        outdir = assembly_dir + "/operams_pooled/{data}"
    log: reports_dir + "/operams_pooled/{data}.err"
    priority: 70
    threads: threads
    shell:
        """
        perl {params.cd}/lib/OPERA-MS-0.8.3/OPERA-MS.pl \
            --short-read1 {input.r1} \
            --short-read2 {input.r2} \
            --num-processors {threads} \
            --long-read {input.long_read} \
            --out-dir {params.outdir} 2> {log}
        cp {output.scaffolds} {output.renamed_scaffolds}
        """

