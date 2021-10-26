#!/usr/bin/env python

import sys
import os

crt_crispr = sys.argv[1]
gid_file = sys.argv[2]
otu_acc_map_f = sys.argv[3]
out = sys.argv[4]

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
with open(crt_crispr, 'r') as crt:
    for line in crt:
        if not line.startswith("CRISPR"):
            genome = line.strip()[:-10] #.fasta.crt
            ranges[genome] = []
        else:
            c, r = line.strip().split(":")
            start, end = [int(x.strip()) for x in r.split("-")]
            ranges[genome].append((start, end, 4)) # no levels

for g in ranges:
    with open(out, 'a+') as o:
        o.write("%s\n" % otu_acc_map[g][2])
        for r in ranges[g]:
            start, end, lvl = r
            if lvl > 1:
                o.write("%s\t%s\t%s\tX\n" % (start, end-start, lvl))

