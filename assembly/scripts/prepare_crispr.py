#!/usr/bin/env python

import sys
import os
from Bio import SeqIO

crisprs = sys.argv[1] # cami_crisprs.tsv
acc_mapping = sys.argv[2] # accession_otu_mapping.tsv
gid_file = sys.argv[3] # genome_to_id.tsv
out_path = sys.argv[4]

all_crisprs = {}
with open(crisprs, 'r') as c:
    genome = ""
    last = ""
    for line in c:
        if line.startswith("GCA"):
            accession = line.strip()
            if last.startswith("GCA"):
                pass
                # No CRISPR found
                #print(last)
        else:
            start, length, trustlvl, seq = line.strip().split('\t')
            if int(trustlvl) >= 4: # levels from 1 to 4 with 4 most certain
                if accession in all_crisprs:
                    all_crisprs[accession].append((start, length, trustlvl, seq))
                else:
                    all_crisprs[accession] = [(start, length, trustlvl, seq)]
        last = line.strip()

otu_acc_map = {}
with open(acc_mapping, 'r') as otu_acc_map_f:
    for line in otu_acc_map_f:
        genome, otu, accession = line.strip().split()
        otu_acc_map[otu] = (accession, genome)

crispr_map = {}
with open(gid_file, 'r') as gids:
    for line in gids:
        otu, path = line.strip().split('\t')
        if otu in otu_acc_map:
            accession, genome = otu_acc_map[otu]
            if accession in all_crisprs:
                crisprs = all_crisprs[accession]
                for record in SeqIO.parse(path, "fasta"):
                    i = 0
                    out_file = os.path.join(out_path, "%s_crisprs.fa" % accession)
                    for crispr in crisprs:
                        start, length, trust, seq = crispr
                        crispr_sequence = record.seq[int(start):int(start)+int(length)]
                        i += 1
                        with open(out_file, 'a+') as f:
                            f.write(">%s_CRISPR_%s\n" % (accession, i))
                            f.write(str(crispr_sequence))
                            f.write('\n')
                    break # ignore plasmids etc

i = 0
j = 0
for c in all_crisprs:
    if all_crisprs[c] != []:
        i += 1
        j += len(all_crisprs[c])
        
print("%s CRISPR sequences for %s genomes (out of 65)" % (j, i))
