#!/usr/bin/env python

import sys
import os
import argparse
import random
from numpy import random as np_rand

def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", help="out path")
    parser.add_argument("-g", help="path to target genomes folder")
    parser.add_argument("-m", help="tsv matrix file with abundances per sample") # this or the next two
    parser.add_argument("-s", help="dataset size in B", type=float)
    if not len(sys.argv) > 4:
        parser.print_help()
        return None
    args = parser.parse_args()
    return args

def calculate_coverage(id_file, abundance_file):
    id_size = {}
    with open(id_file, 'r') as gid:
        for line in gid:
            otu, path = line.strip().split('\t')
            id_size[otu] = os.path.getsize(path)
    with open(abundance_file, 'r') as ab:
        for line in ab:
            otu, abundance = line.strip().split('\t')
            id_size[otu] = id_size[otu] * float(abundance)
    return sum(id_size.values())

# given a list of genomes and abundances as well as the total data (abundance * filesize) and the size, calculate individual abundances
def list_to_individual_ab(target_coverages, target_genomes, tot_ab, size):
    target_coverages = [float(x) for x in target_coverages]
    ziplist = zip(target_coverages, [os.path.getsize(x) for x in target_genomes])
    summed_up = sum([x * y for (x,y) in ziplist])
    req_data = summed_up/size # gbp required to achieve coverage of x for all genomes
    remaining_data = 1 - req_data # gbp left for other genomes
    quotient = remaining_data/req_data # quotient of remaining vs required data
    abundances = tot_ab/quotient # sum of data left to distribute among target genomes
    ziplist = zip(target_coverages, [os.path.getsize(x) for x in target_genomes])
    abundance_to_set = [abundances/y * x/sum(target_coverages) for (x,y) in ziplist]
    return abundance_to_set

# reads the abundance matrix
def read_matrix(filename):
    genomes = []
    all_abundances = []
    with open(filename, 'r') as f:
        for line in f:
            row = line.strip().split('\t')
            genome = row[0]
            abundances = row[1:]
            genomes.append(genome)
            all_abundances.append(abundances)
    return (genomes, all_abundances)

def main():
    args = parse_options()
    if args == None:
        return
    gid_file = os.path.join(args.o, "genome_to_id.tsv")
    md_file = os.path.join(args.o, "metadata.tsv")
    camitax_file = os.path.join(args.o, "camitax.tsv")
    otu_id_map = {}
    with open(camitax_file, 'r') as ct:
        for line in ct:
            split = line.strip().split('\t')
            genome = split[0]
            taxid = split[1]
            otu_id_map[genome] = taxid
    if (args.m != None):
        genomes, abundances = read_matrix(args.m)
        genomes = [os.path.join(args.g, genome + ".fasta") for genome in genomes]
        for j in range(len(genomes)):
            name = os.path.basename(genomes[j])[:-6] # cutting of .fasta
            path = genomes[j]
            taxid = otu_id_map[name]
            novelty = "manual_strain"
            with open(md_file, 'a+') as m:
                m.write(name + '\t' + taxid + '\t' + taxid + '\t' +  novelty + '\n')
            with open(gid_file, 'a+') as g:
                g.write(name + '\t' + path + '\n')
        transposed_ab = list(map(list, zip(*abundances)))
        files = os.listdir(args.o)
        for i in range(len(transposed_ab)):
            ab_file = os.path.join(args.o, "abundance%s.tsv" % i)
            tot_ab = calculate_coverage(gid_file, ab_file)
            values = list_to_individual_ab(transposed_ab[i], genomes, tot_ab, args.s)
            for j in range(len(genomes)):
                name = os.path.basename(genomes[j])[:-6] # cutting of .fasta
                with open(ab_file, 'a+') as a:
                    a.write(name + '\t' + str(values[j]) + '\n')

if __name__ == "__main__":
    main()
