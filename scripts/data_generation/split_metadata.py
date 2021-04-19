#!/usr/bin/env python

"""
Script for creating metadata.tsv and genome_to_id.tsv for CAMISIM from the generated metadata file of check_consistency.py
"""

import sys
import os

md_old = sys.argv[1] # just the file as input
out_folder = sys.argv[2]
gen = os.path.join(out_folder,"genome_to_id.tsv")
md_new = os.path.join(out_folder,"metadata.tsv")
with open(md_new,'a+') as m:
    m.write("genome_ID\tOTU\tNCBI_ID\tnovelty_category\n")

with open(md_old,'r') as md:
    for line in md:
        taxid, gen_name, path, novelty = line.strip().split('\t')
        with open(md_new,'a+') as m:
            m.write("{g}\t{n}\t{n}\t{nov}\n".format(g=gen_name,n=taxid,nov=novelty))
        with open(gen,'a+') as g:
            g.write("{g}\t{p}\n".format(g=gen_name,p=path))
