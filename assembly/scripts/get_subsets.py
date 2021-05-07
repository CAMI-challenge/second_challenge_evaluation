#!/usr/bin/env python

import sys
import os

metadata = sys.argv[1]
gid = sys.argv[2]
unique = sys.argv[3]

new = set()
db = set()
plasmids = set()
with open(metadata, 'r') as md:
    for line in md:
        if line.startswith("genome"):
            continue
        genid, otu, ncbi, nov = line.strip().split('\t')
        #if (nov == "known_strain"):
        #    db.add(genid)
        # this is just a cross-check

anon_map = {}
with open(gid, 'r') as g:
    for line in g:
        genid, path = line.strip().split('\t')
        anon_map[os.path.basename(path).rsplit(".",1)[0]] = genid
        #if genid in db:
        #    #if "contigs" in path:
        #    #    print(genid)
        #    continue
        if "RNODE" in path:
            plasmids.add(genid)
        elif "genomic" in path or "PRJNA" in path or "MPI" in path: # modify for other datasets?
            db.add(os.path.basename(path).rsplit(".",1)[0])
            #db.add(genid)
        else:
            new.add(os.path.basename(path).rsplit(".",1)[0])
            #new.add(genid)
            # depends on format of unique file
            # remove .fasta at the end of path

uq_map = {}
with open(unique, 'r') as uq:
    for line in uq:
        name, typ = line.strip().split('\t')
        uq_map[name] = (typ == "uniq")

new_uq = set()
new_co = set()
db_uq = set()
db_co = set()
# rhizosphere only
db_extra = set()
new_extra = set()
for elem in new:
    try:
        uq_map[elem]
    except:
        new_extra.add(anon_map[elem])
        continue
    if uq_map[elem]:
        new_uq.add(anon_map[elem])
    else:
        new_co.add(anon_map[elem])

for elem in db:
    try:
        uq_map[elem]
    except:
        db_extra.add(anon_map[elem])
        continue
    if uq_map[elem]:
        db_uq.add(anon_map[elem])
    else:
        db_co.add(anon_map[elem])

print("New_unique\t%s" % list(new_uq))
print("New_common\t%s" % list(new_co))
print("Database_unique\t%s" % list(db_uq))
print("Database_common\t%s" % list(db_co))
print("Circular\t%s" % list(plasmids))
# only rhizosphere
print("New_extra\t%s" % list(new_extra))
print("Database_extra\t%s" % list(db_extra))
