#!/usr/bin/env python

import sys

crisprs = sys.argv[1] # cami_crisprs.tsv
acc_mapping = sys.argv[2] # accession_otu_mapping.tsv
gid_file = sys.argv[3] # genome_to_id.tsv

all_crisprs = {}
with open(crisprs, 'r') as c:
    genome = ""
    for line in c:
        if line.startswith("GCA"):
            genome = line.strip()
        else:
            start, length, trustlvl, seq = line.strip().split('\t')
            if int(trustlvl) >= 4: # levels from 1 to 4 with 4 most certain
                if genome in all_crisprs:
                    all_crisprs[genome].append((start, length, trustlvl, seq))
                else:
                    all_crisprs[genome] = [(start, length, trustlvl, seq)]

otu_acc_map = {}
with open(acc_mapping, 'r') as otu_acc_map_f:
    for line in otu_acc_map_f:
        genome, otu, accession = line.strip().split('\t')
        otu_acc_map[accession] = (otu, genome)

i = 0
j = 0
for c in all_crisprs:
    if all_crisprs[c] != []:
        i += 1
        j += len(all_crisprs[c])
        


print("%s CRISPR sequences for %s genomes (out of 65)" % (j, i))
