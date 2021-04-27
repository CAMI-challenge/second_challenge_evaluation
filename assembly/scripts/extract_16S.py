#!/usr/bin/env python

import sys
import os
import ast
import subprocess
from io import StringIO
from Bio import SeqIO

gid = sys.argv[1] # genome to id
high_q = sys.argv[2] # subset file
out_folder = sys.argv[3]
hq_genomes = []

with open(high_q, 'r') as hq:
    for line in hq:
        name, l = line.strip().split('\t')
        if (name == "very_high_quality_genomes"):
            hq_genomes = ast.literal_eval(l)

with open(gid, 'r') as gen_to_id:
    for line in gen_to_id:
        otu, path = line.strip().split('\t')
        out = os.path.join(out_folder, "%s_16S.fa" % otu)
        if (otu in hq_genomes):
            with open(path, 'r') as g:
                for line in g:
                    name = line[1:].split(" ")[0] # retrieve GI
                    print(otu)
                    print(name)
                    command = "curl -X GET -G https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide -d id=%s -d rettype=gb -d retmode=text" % name
                    gb = subprocess.check_output(command, shell=True).decode()
                    stringio = StringIO(gb)
                    genome = SeqIO.read(stringio, "genbank")
                    stringio.close()
                    for gene in genome.features:
                        if gene.type == "rRNA":
                            if 'product' in gene.qualifiers:
                                if '16S' in gene.qualifiers['product'][0]:
                                    start = gene.location.nofuzzy_start
                                    end = gene.location.nofuzzy_end
                                    with open(out, 'w') as outf:
                                        outf.write(">%s_16S\n" % name)
                                        outf.write(str(genome.seq[start:end]))
                                    print("16S written")
                                    break #only write one 16S per genome
                            else:
                                print("Product not in qualifiers")
                    break

                            
