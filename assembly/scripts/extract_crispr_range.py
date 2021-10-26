#!/usr/bin/env python

import sys
import os

pred_folder = sys.argv[1]
gid_file = sys.argv[2]
otu_acc_map_f = sys.argv[3]
out = sys.argv[4]
files = os.listdir(pred_folder)

gids = {}
with open(gid_file, 'r') as g:
    for line in g:
        otu, path = line.strip().split('\t')
        gid = path.rsplit('/',1)[-1][:-6]
        gids[otu] = gid

otu_acc_map = {}
with open(otu_acc_map_f, 'r') as o:
    for line in o:
        genome, otu, acc = line.strip().split()
        gid = gids[otu]
        otu_acc_map[gid] = (genome, otu, acc)

ranges = {}
k = 0
for f in files:
    if f.endswith(".csv"):
        genome = f[:-4]
        positions = []
        i = 0
        j = 0
        with open(f, 'r') as pred:
            prev = False
            for line in pred:
                if line.startswith("\"1\""):
                    continue
                perc, perc2, pos = line.strip().split()
                if float(perc) > 0.5:
                    if prev:
                        continue
                    else:
                        start = int(pos)
                    prev = True
                elif (prev):
                    if (int(pos) - start) > 500:
                        positions.append((start, int(pos), 4))
                    elif (int(pos) - start) > 10:
                        positions.append((start, int(pos), 1))
                        j += 1
                    else:
                        i += 1
                    prev = False
        #print(genome)
        #print(positions)
        #print(i)
        #print(j)
        if (len(positions) == 0):
            k += 1
        ranges[genome] = positions

total_crisprs = sum([len(x) for x in ranges.values() if x[2] == 4])
print("%s CRISPR found for %s genomes (no CRISPR found for %s genomes)" % (total_crisprs,len(ranges.keys()), k))

for g in ranges:
    with open(out, 'a+') as o:
        o.write("%s\n" % otu_acc_map[g][2])
        for r in ranges[g]:
            start, end, lvl = r
            if lvl > 1:
                o.write("%s\t%s\t%s\tX\n" % (start, end-start, lvl))

