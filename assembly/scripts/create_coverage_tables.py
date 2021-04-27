#!/usr/bin/env python

import subprocess
import sys
import os

path = sys.argv[1]

genomes = {}
with open(os.path.join(path, "genome_to_id.tsv"), 'r') as md:
    for line in md:
        if (not line.startswith("genome")):
            genome, p = line.strip().split('\t')
            genomes[genome] = p

files = os.listdir(path)
for f in files:
    if f.startswith("201"):
        bam_files = os.listdir(os.path.join(path, f, "bam"))
        coverage = os.path.join(path, "coverage_new%s.tsv" % f.split("_")[-1])
        cmap = {}
        for bam in bam_files:
            if bam.endswith(".bam"):
                name = bam.rstrip(".bam")
                gen = genomes[name]
                bases = float(subprocess.check_output("grep -v \">\" %s | wc | awk '{print $3-$1}'" % os.path.join("genomes", gen),
                    stderr=subprocess.STDOUT,
                    shell=True))
                nonzero = subprocess.check_output(
                    "samtools stats %s | grep ^COV | cut -f3,4" % os.path.join(path, f, "bam", bam),
                    stderr=subprocess.STDOUT,
                    shell=True)
                nz = nonzero.split()
                nonzero_map = {}
                for i in range(int(len(nz)/2)):
                    nonzero_map[int(nz[2*i])] = float(nz[2*i+1])
                nonzero_map[0] = bases - sum(nonzero_map.values()) # all bases minus all covered bases = all noncovered bases
                cov = 0
                for g in nonzero_map:
                    cov += g * nonzero_map[g]
                cmap[name] = cov/float(bases)
        with open(coverage, 'w+') as cov:
            for genome in genomes:
                if genome in cmap:
                    cov.write("%s\t%s\n" % (os.path.basename(genomes[genome]), cmap[genome]))
                else:
                    cov.write("%s\t%s\n" % (os.path.basename(genomes[genome]), 0.0))
