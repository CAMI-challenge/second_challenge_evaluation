#!/usr/bin/env python

import sys
import os
from Bio import SeqIO

crisprs_f = sys.argv[1] # cami_crisprs.tsv
crisprs_crt = sys.argv[2] # cami_crisprs_crt.tsv
crisprs_ml = sys.argv[3] # cami_crisprs_ml.tsv
acc_mapping = sys.argv[4] # accession_otu_mapping.tsv
gid_file = sys.argv[5] # genome_to_id.tsv
out_path = sys.argv[6]

i = 0
crisprs = [crisprs_f, crisprs_crt, crisprs_ml]
all_crisprs = {}
for crispr in crisprs:
    with open(crispr, 'r') as c:
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
                        starts = [x[0] for x in all_crisprs[accession]]
                        found = False
                        j = 0
                        for s in starts:
                            if (s <= int(start) and s + 500 >= int(start)) or (s >= int(start) and s - 500 <= int(start)):
                                all_crisprs[accession][j][4].add(i)
                                found = True
                            j += 1
                        if not found:
                            all_crisprs[accession].append([int(start), int(length), int(trustlvl), seq, set([i])])
                    else:
                        all_crisprs[accession] = [[int(start), int(length), int(trustlvl), seq, set([i])]]
            last = line.strip()
    i += 1

otu_acc_map = {}
with open(acc_mapping, 'r') as otu_acc_map_f:
    for line in otu_acc_map_f:
        genome, otu, accession = line.strip().split()
        otu_acc_map[otu] = (accession, genome)

f = 0
crt = 0
ml = 0
f_crt = 0
f_ml = 0
crt_ml = 0
all = 0

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
                        start, length, trust, seq, presence = crispr
                        group = ""
                        if presence == set([0,1,2]):
                            group = "all"
                            all += 1
                        elif presence == set([0]):
                            group = "finder"
                            f += 1
                        elif presence == set([1]):
                            group = "crt"
                            crt += 1
                        elif presence == set([2]):
                            group = "ml"
                            ml += 1
                        elif presence == set([0,1]):
                            group = "finder_crt"
                            f_crt += 1
                        elif presence == set([0,2]):
                            group = "finder_ml"
                            f_ml += 1
                        elif presence == set([1,2]):
                            group = "crt_ml"
                            crt_ml += 1
                        crispr_sequence = record.seq[int(start):int(start)+int(length)]
                        with open(out_file, 'a+') as outf:
                            outf.write(">%s_CRISPR_%s_from_%s_(%s)\n" % (accession, i, start, group))
                            outf.write(str(crispr_sequence))
                            outf.write('\n')
                        i += 1
                    break # ignore plasmids etc

i = 0
j = 0
for c in all_crisprs:
    accessions = [x[0] for x in otu_acc_map.values()]
    if c not in accessions:
        continue
    if all_crisprs[c] != []:
        i += 1
        j += len(all_crisprs[c])
        
print("%s CRISPR sequences for %s genomes (out of 50)" % (j, i))
print("Only Finder: %s, only CRT: %s, only ML: %s" % (f,crt,ml))
print("Finder/CRT: %s, Finder/ML: %s, CRT/ML: %s, All: %s" % (f_crt, f_ml, crt_ml, all))
