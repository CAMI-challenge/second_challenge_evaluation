rule fastp:
    input:
        lambda wc: path.join(fq_dir, wc.sample + "_reads.fq.gz")
    output:
        or1 = qc_dir + "/{sample}.qc_1.fq",
        or2 = qc_dir + "/{sample}.qc_2.fq",
        html = reports_dir + "/fastp/{sample}.qc.report.html"
    threads: 8
    conda: config["profile_conda_env"]
    shell:
        """
        fastp --interleaved_in --in1 {input} -o {output.or1} -O {output.or2} \
            -5 20 -3 20 -l 50 -h {output.html} -w {threads}
        """