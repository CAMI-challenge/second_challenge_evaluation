#!/usr/bin/env python

import sys

name = sys.argv[1]

#assemblers = {"sample_short_gsa" : "gsa", "MetaHipMer_short":"HipMer", "MetaHipMer2_short":"HipMer2", "metaSPAdes_short":"SPAdes", "Megahit_short":"MEGAHIT","OPERA-MS_hybrid":"OPERA-MS", "pooled_short_gsa":"gsa"}
#exclude gsa
assemblers = {"MetaHipMer_short":"HipMer", "MetaHipMer2_short":"HipMer2", "metaSPAdes_short":"SPAdes", "Megahit_short":"MEGAHIT","OPERA-MS_hybrid":"OPERA-MS"}
samples = {"LjRoot109" : ["sample3", "pooled"],
    "LjRoot170" : ["sample2", "sample3", "sample4", "pooled"],
    "LjRoot28" : ["sample3", "pooled"],
    "3934_BI" : ["sample0", "pooled"]}

metrics = {}
assm = ""
with open(name, 'r') as f:
    for line in f:
        try:
            assm, rec, mm, dup, ma, gf, prec, nga50 = line.strip().split('\t')
            if assm == "assembler":
                continue
        except:
            genome, sample  = line.strip()[:-4].rsplit("_",1) # exlcude .tsv
        assembler = genome + "_" + sample + "_" + assm
        if assm in assemblers:
            if genome in samples and sample in samples[genome]:
                metrics[assembler] = [float(rec), float(mm), float(dup),float(ma), float(gf), float(prec), float(nga50)]
       
#all_rec = [x[0] for x in metrics.values()]
all_mm = [x[1] for x in metrics.values()]
max_mm = max(all_mm)
min_mm = min(all_mm)
all_dup = [x[2] for x in metrics.values()]
max_dup = max(all_dup)
min_dup = min(all_dup)
all_ma = [x[3] for x in metrics.values()]
max_ma = max(all_ma)
min_ma = min(all_ma)
all_gf = [x[4] for x in metrics.values()]
max_gf = max(all_gf)
min_gf = min(all_gf)
#all_prec = [x[5] for x in metrics.values()]
all_nga50 = [x[6] for x in metrics.values()]
max_nga50 = max(all_nga50)
min_nga50 = min(all_nga50)

weight = [0.2, 0.1, 0.1, 0.3, 0.3]
scores = []
for assembler in metrics:
    rec, mm, dup, ma, gf, prec, nga50 = metrics[assembler]
    val_mm = (max_mm - mm)/(max_mm - min_mm)
    val_dup = (max_dup - dup)/(max_dup - min_dup)
    val_ma = (max_ma - ma)/(max_ma - min_ma)
    val_gf = (gf - min_mm)/(max_mm - min_mm)
    try:
        val_nga50 = (nga50 - min_mm)/(max_mm - min_mm)
    except:
        val_nga50 = 0 # no assembler has 50% gf
    score = sum([x * y for x,y in zip(weight,[val_mm,val_dup,val_ma,val_gf,val_nga50])])
    scores.append((score,assembler))

scores = sorted(scores,reverse=True)
for score in scores:
    print("%s\t%s" % (score[1], score[0]))
