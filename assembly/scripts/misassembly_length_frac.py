#!/usr/bin/env python

import sys

assembly_summary_unique = sys.argv[1]
assembly_summary_common = sys.argv[2]

summary = {}
with open(assembly_summary_unique, 'r') as asu:
    for line in asu:
        assm, rec, mism, dup, mis, gf, prec, nga, length, mis_contigs_length = line.strip().split('\t')
        if assm == "assembler":
            continue
        summary[assm] = [(float(mis), float(length), float(mis_contigs_length))]

with open(assembly_summary_common, 'r') as asc:
    for line in asc:
        assm, rec, mism, dup, mis, gf, prec, nga, length, mis_contigs_length = line.strip().split('\t')
        if assm == "assembler":
            continue
        summary[assm].append((float(mis), float(length), float(mis_contigs_length)))

uq = 0
co = 0
uq_tot = 0
co_tot = 0
for assembler in summary:
    unique, common = summary[assembler]
    print(assembler)
    print("Unique: %s misassembled length" % (unique[2]/unique[1]))
    print("Common: %s misassembled length" % (common[2]/common[1]))
    uq += unique[2]
    uq_tot += unique[1]
    co += common[2]
    co_tot += common[1]

print("Total unique: %s" % (uq/uq_tot))
print("Total common: %s" % (co/co_tot))
