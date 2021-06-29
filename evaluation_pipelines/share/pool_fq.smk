rule pool_reads:
    input:
        r1s = expand(qc_dir + "/{sample}.qc_1.fq", sample=samples),
        r2s = expand(qc_dir + "/{sample}.qc_2.fq", sample=samples)
    output:
        pr1 = qc_dir + "/{}.qc_1.fq".format(pooled_dataset),
        pr2 = qc_dir + "/{}.qc_2.fq".format(pooled_dataset)
    shell:
        """
        cat {input.r1s} > {output.pr1}
        cat {input.r2s} > {output.pr2}
        """

rule pool_long_reads:
    input:
        reads = [long_fq_dir + "/" + sample.replace("short", "long") + "_reads.fq" for sample in samples]#[for sample in expand(long_fq_dir + "/{sample}.qc_1.fq", sample=samples)]
    output:
        preads = long_fq_dir + "/{}.long.fq".format(pooled_dataset)
    shell:
        """
        cat {input.reads} > {output.preads}
        """