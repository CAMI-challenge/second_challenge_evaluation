#!/usr/bin/env python

import sys
import os
import argparse
import ast

parser = argparse.ArgumentParser()
parser.add_argument("-dir", type=str, help="working dir of metaquast output")
parser.add_argument("-o", type=str, help="out dir")
parser.add_argument("-d", default=False, help="Use default metrics (no strain recall/precision)", action='store_true')
parser.add_argument("-mm", default=100., type=float, help="required mismatches for a genome to be high quality")
parser.add_argument("-gf", default=0.9, type=float, help="required genome fraction for a genome to be high quality (between 0 and 1)")
parser.add_argument("-na", default=True, action='store_false', help="Do not use NGA50 averaged over all genomes, but NA50 instead")
parser.add_argument("-s1", "--split-by-ani", default=False, action='store_true', help="Split genomes by ANI>95% and <95%. Doubles the rows. Requires f1 file (genome - comm/uniq)")
parser.add_argument("-f1", "--ani-file", type=str, help="File with all genomes and whether they are comm/uniq (tab-separated)")
parser.add_argument("-s2", "--split-by-database", default=False, action='store_true', help="Split genomes by database or newly sequenced. Doubles the rows. Requires f2 file (metadata.tsv)")
parser.add_argument("-f2", "--metadata-file", type=str, help="File with all genomes and whether they are database/new (tab-separated), database is last column")
parser.add_argument("-f3", "--gid-file", type=str, help="genome_to_id_file")
parser.add_argument("-sf", "--subset", type=str, help="file with subsets of genomes")
parser.add_argument("-sx", "--suffix", type=str, help="suffix for file names")
parser.add_argument("-x", "--exclude", default=True, action='store_false', help="Do not exclude circular elements")
parser.add_argument("-sum", "--summary", default=False, action='store_true', help="Only summary is available not runs per reference")
args = parser.parse_args()

if not len(sys.argv) > 1:
    parser.print_help()
    quit()

unique = []
common = []
if args.split_by_ani:
    try:
        with open(args.ani_file, 'r') as af:
            for line in af:
                spl = line.strip().split('\t')
                name = spl[0].replace("-","_").replace("+","_")
                if spl[1] == "uniq":
                    unique.append(name) # if unique or not (True = unique)
                else:
                    common.append(name)
    except TypeError: #?
        parser.print_help()
        quit()

gid = {}
try:
    with open(args.gid_file, 'r') as gf:
        for line in gf:
            spl = line.strip().split('\t')
            gid[spl[0]] = os.path.basename(spl[1]).rsplit(".",1)[0].replace("-","_").replace("+","_") # might need some more replaces?
except TypeError: #?
    print("Genome to ID file is required")
    parser.print_help()
    quit()

subsets = {}
with open(args.subset, 'r') as s:
    for line in s:
        name, members = line.split('\t')
        l = ast.literal_eval(members)
        subset = [gid[x] for x in l]
        subsets[name] = subset

db = []
new = []
if args.split_by_database:
    try:
        with open(args.metadata_file, 'r') as md:
            f = True
            for line in md:
                if f:
                    f = False
                    continue # skip first line
                spl = line.strip().split('\t')
                if (spl[-1] == "known_strain"):
                    db.append(gid[spl[0]]) # True = database
                else:
                    new.append(gid[spl[0]])
    except TypeError:
        parser.print_help()
        quit()

directory = args.dir
folders = os.listdir(directory)
if args.d:
    if args.na:
        metrics = "assembler\t# contigs\t# mismatches per 100 kbp\t# misassemblies\tDuplication ratio\tGenome fraction (%)\tLargest alignment\tNGA50\n".split('\t')
    else:
        metrics = "assembler\t# contigs\t# mismatches per 100 kbp\tDuplication ratio\tGenome fraction (%)\tLargest alignment\tNA50\n".split('\t')
else:
    if args.na:
        metrics = "assembler\tStrain recall\t# mismatches per 100 kbp\tDuplication ratio\t# misassemblies\tGenome fraction (%)\tStrain precision\tNGA50".split('\t')
    else:
        metrics = "assembler\tStrain recall\t# mismatches per 100 kbp\tDuplication ratio\tGenome fraction (%)\tStrain precision\tNA50".split('\t')

if args.summary:
    metrics = ["assembler","Genome_fraction","num_mismatches_per_100_kbp", "num_misassemblies", "NGA50", "Strain recall", "Strain precision", "Duplication_ratio"]

small_good = ["# mismatches per 100 kbp", "# misassemblies", "Duplication ratio"]
small_good.extend(["num_mismatches_per_100_kbp", "num_misassemblies", "Duplication_ratio"])

def add_to_map(assemblers, a, metric, value):
    if value == "-" and metric not in small_good:
        value == 0
    elif value == "-":
        return assemblers # do not add
    if metric == "Genome fraction (%)" or metric == "Genome_fraction":
        assemblers[a][metric] = float(value)/100.
    elif metric == "NGA50":
        try:
            assemblers[a][metric] = float(value)
        except:
            assemblers[a][metric] = 0.
    else:
        try:
            assemblers[a][metric] = float(value)
        except:
            assemblers[a][metric] = None
    return assemblers

def append_to_map(assemblers, a, metric, value, genome):
    if value == "-" and metric not in small_good:
        value = 0
    elif value == "-":
        return assemblers # do not add
    if metric == "Genome fraction (%)" or metric == "Genome_fraction":
        assemblers[a][metric][genome] = float(value)/100.
    elif metric == "NGA50":
        try:
            assemblers[a][metric][genome] = float(value)
        except:
            assemblers[a][metric][genome] = 0.
    else:
        try:
            assemblers[a][metric][genome] = float(value)
        except:
            assemblers[a][metric][genome] = None
    return assemblers

def read_metaquast(path, assembler_map, append, genome):
    assm = ""
    with open(path, 'r') as q:
        for line in q:
            spl = line.strip().split('\t')
            v0 = spl[0]
            if not args.summary:
                metric = spl[0]
            else:
                genome = spl[0]
                metric = os.path.basename(path)[:-4]
            if v0 == "Assembly" or v0 == "Assemblies":
                assm = spl[1:]
                continue
            if metric in metrics:
                i = 0
                added = []
                for a in assm:
                    added.append(a)
                    if append:
                        if metric not in assembler_map[a]:
                            assembler_map[a][metric] = {}
                        assembler_map = append_to_map(assembler_map, a, metric, spl[i + 1], genome)
                    else:
                        assembler_map = add_to_map(assembler_map, a, metric, spl[i + 1])
                    i += 1
                for a in assembler_map:
                    if a not in added:
                        if append:
                            if metric not in assembler_map[a]:
                                assembler_map[a][metric] = {}
                            assembler_map = append_to_map(assembler_map, a, metric, 0., genome)
                        else:
                            assembler_map = add_to_map(assembler_map, a, metric, 0.)
    return assembler_map

#"""
if args.summary:
    path = os.path.join(directory, "summary", "TSV")
else:
    path = os.path.join(directory, "runs_per_reference")
assm = []
with open(os.path.join(directory, "summary", "TSV", "NGA50.tsv")) as am:
    for line in am:
        assm = line.strip().split('\t')[1:]
        break

assemblers = {}
for a in assm:
    if a not in assemblers:
        assemblers[a] = {}

genomes = os.listdir(path)
all_genomes = []
for genome in genomes:
    if args.exclude and genome.startswith("RNODE"):
        continue
    if args.summary:
        metric = genome[:-4]
        if metric in metrics:
            report = os.path.join(path, genome)
            assemblers = read_metaquast(report, assemblers, True, metric)
    else:
        report = os.path.join(path, genome, "report.tsv")
        assemblers = read_metaquast(report, assemblers, True, genome)
    all_genomes.append(genome)

def calculate_final(assembler_map, subset):
    out = {}
    for assembler in assembler_map:
        out[assembler] = {}
        if args.summary:
            gf = "Genome_fraction"
            mm = "num_mismatches_per_100_kbp"
        else:
            gf = "Genome fraction (%)"
            mm = "# mismatches per 100 kbp"
        prec = 0
        complete = 0
        total = 0
        for genome in subset:
            total += 1
            if genome not in assembler_map[assembler][gf]:
                continue
            if assembler_map[assembler][gf][genome] > args.gf:
                complete += 1
            if assembler_map[assembler][gf][genome] > args.gf and assembler_map[assembler][mm][genome] < args.mm:
                prec += 1
        for metric in assembler_map[assembler]:
            m = 0
            i = 0
            for genome in assembler_map[assembler][metric]:
                if genome in subset:
                    if assembler_map[assembler][metric][genome] is not None:
                        m += assembler_map[assembler][metric][genome]
                        i += 1
            if metric == "NGA50": 
                out[assembler][metric] = m/len(subset)
            else:
                if i > 0:
                    out[assembler][metric] = m/i
                else:
                    out[assembler][metric] = 0 
        if complete > 0:
            out[assembler]["Strain precision"] = prec/complete
        else:
            out[assembler]["Strain precision"] = 0.
        out[assembler]["Strain recall"] = prec/total
    return out

result_files = {}
#subsets are: subsets (file), new, db, common, unique
if args.split_by_database:
    result_files["database_genomes"] = calculate_final(assemblers, db)
    result_files["new_genomes"] = calculate_final(assemblers, new)
if args.split_by_ani:
    result_files["unique_genomes"] = calculate_final(assemblers, unique)
    result_files["common_genomes"] = calculate_final(assemblers, common)
if len(subsets) > 0:
    i = 2
    for subset in subsets:
        result_files[subset] = calculate_final(assemblers, subsets[subset])
        i += 1

#result_files["total"] = calculate_final(assemblers, all_genomes)

for subset in result_files:
    assemblers = result_files[subset]
    if not (subset == "total" or subset == "non_circular_common_genomes" or subset == "non_circular_unique_genomes"):
        continue
    print(subset)
    for assembler in assemblers:
        print("%s\t%s\t%s" % (assembler, assemblers[assembler]["Strain recall"], assemblers[assembler]["Strain precision"]))

if args.d:
    header = "assembler\t# contigs\t# mismatches per 100 kbp\tDuplication ratio\t# misassemblies\tGenome fraction (%)\tLargest alignment\tNGA50\n"
else:
    header = "assembler\tStrain recall\t# mismatches per 100 kbp\tDuplication ratio\t# misassemblies\tGenome fraction (%)\tStrain precision\tNGA50\n"
for subset in result_files:
    if args.suffix:
        collected = os.path.join(args.o,"%s%s.tsv" % (subset, args.suffix))
    else:
        collected = os.path.join(args.o,"%s.tsv" % (subset))
    write_header = not os.path.exists(collected)
    with open(collected, 'a+') as q:
        if write_header:
            q.write(header)
        assemblers = result_files[subset]
        for assembler in assemblers:
            if (args.d):
                contigs = assemblers[assembler]["# contigs"]
            else:
                contigs = assemblers[assembler]["Strain recall"]
            try:
                mismatches = assemblers[assembler]["# mismatches per 100 kbp"]
            except KeyError:
                mismatches = assemblers[assembler]["num_mismatches_per_100_kbp"]
            try:
                dup = assemblers[assembler]["Duplication ratio"]
            except KeyError:
                dup = assemblers[assembler]["Duplication_ratio"]
            try:
                ma = assemblers[assembler]["# misassemblies"]
            except KeyError:
                ma = assemblers[assembler]["num_misassemblies"]
            try:
                gf = assemblers[assembler]["Genome fraction (%)"]
            except KeyError:
                gf = assemblers[assembler]["Genome_fraction"]
            if (args.d):
                align = assemblers[assembler]["Largest alignment"]
            else:
                align = assemblers[assembler]["Strain precision"]
            try:
                nga = assemblers[assembler]["NGA50"]
            except ValueError:
                nga = 0.
            line = "{method}\t{contigs}\t{mismatches}\t{dup}\t{ma}\t{gf}\t{align}\t{nga}\n" .format(
                method = assembler, 
                contigs = contigs,
                mismatches = mismatches,
                dup = dup,
                ma = ma,
                gf = gf,
                align = align,
                nga = nga)
            q.write(line)

