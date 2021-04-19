#!/usr/bin/env python

import sys
import os
import argparse
import random
from numpy import random as np_rand
import add_plasmids
import fungal_metadata

def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", help="Plasmid metadata file")
    parser.add_argument("-p", help="Plasmid fasta file path")
    parser.add_argument("-e", help="plasmids to exclude, i.e. the marine metadata file")
    parser.add_argument("-f", help="Path to the fungal genomes")
    parser.add_argument("-md", help="metadata file")
    parser.add_argument("-id", help="genome_to_id file")
    parser.add_argument("-s", help="random seed", type=int)
    parser.add_argument("-o", help="out path")
    parser.add_argument("-size", help="data set size (in kB! 5 GB = 5000000.)",type=float)
    if not len(sys.argv) > 9:
        parser.print_help()
        return None
    args = parser.parse_args()
    return args

def main():
    args = parse_options()
    if args == None:
        return
    random.seed(args.s)
    np_rand.seed(args.s)
    add_fungal_metadata(args.o, args.f)
    files = os.listdir(args.o)
    num_fungals = 55 # TODO read from directory?
    distr = np_rand.lognormal(1,2, num_fungals)
    for f in files:
        if f.startswith("abundance"):
            ab_file = os.path.join(args.o, f)
            create_metadata(ab_file, distr, args.f, args.o, args.size)
    new_plasmids = remove_used_plasmids(args.e, args.m, args.o)
    md = add_plasmids.read_metadata(new_plasmids)
    add_plasmids.add_plasmids(args.o, args.p, md, 399, 1, 0.1, True)
    # adding the remaining 399 plasmids wih default noise and short_read (option does not do anything)

# adds the metadata of the fungal genomes to the genome_to_id and metadata files
def add_fungal_metadata(out, fungal_path):
    files = os.listdir(fungal_path)
    metadata_file = os.path.join(out, "metadata.tsv")
    gid_file = os.path.join(out, "genome_to_id.tsv")
    fungal_md = fungal_metadata.get_metadata(fungal_path)
    for f in files:
        if f.endswith(".fasta"):
            if f.startswith("GCF"): # arabidopsis genome
                with open(os.path.join(out, metadata_file), 'a+') as md:
                    md.write("\t".join((f[:-6], "3702", "3702", "known_strain"))) # ends with .fasta and has taxid 3702
                    md.write('\n')
                with open(os.path.join(out, gid_file), 'a+') as gid:
                    gid.write("\t".join((f[:-6], os.path.join(fungal_path, f))))
                    gid.write('\n')
            else:
                with open(os.path.join(out, metadata_file), 'a+') as md:
                    md.write("\t".join((f[:-14], str(fungal_md[f]), str(fungal_md[f]), "known_strain")))
                    md.write('\n')
                with open(os.path.join(out, gid_file), 'a+') as gid:
                    gid.write("\t".join((f[:-14], os.path.join(fungal_path, f)))) # end with contigs.fasta
                    gid.write('\n')

def remove_used_plasmids(exclude, plasmids, outpath):
    new_plasmid_file = os.path.join(outpath, "plasmids.tsv")
    with open(new_plasmid_file, 'a+') as pfile:
        remove = []
        with open(exclude, 'r') as efile:
            for line in efile:
                remove.append(line.strip().split('\t')[0])
        with open(plasmids, 'r') as f:
            for line in f:
                name, id1, id2, t = line.strip().split('\t')
                if name[:-6] not in remove:
                    pfile.write(line)
    return new_plasmid_file 

def create_metadata(abundance_file, initial_distr, fungal_path, out, size):
    files = os.listdir(fungal_path)
    abundance = 0.
    with open(abundance_file, 'r') as f:
        for line in f:
            try:
                otu, ab = line.strip().split('\t')
            except ValueError:
                print(line)
                print(abundance_file)
                raise ValueError
            abundance = abundance + float(ab)
    fungal_abundance = 0.09 * abundance
    arabidopsis_abundance = 0.01 * abundance #TODO parameter?
    noise = np_rand.normal(1, 0.1, len(initial_distr))
    distr = [x * y for x,y in zip(initial_distr, noise)] # add gaussian noise to initial value, parameter?
    distr = [abs(x)/sum(distr) for x in distr]
    i = 0
    for f in files:
        if f.endswith(".fasta"):
            if f.startswith("GCF"):
                with open(os.path.join(out, abundance_file),'a+') as ab:
                    filesize = os.path.getsize(os.path.join(fungal_path,f))
                    abundance_value = size * arabidopsis_abundance/filesize 
                    ab.write("%s\t%s\n" % (f[:-6], abundance_value))
            else:
                with open(os.path.join(out, abundance_file),'a+') as ab:
                    filesize = os.path.getsize(os.path.join(fungal_path,f))
                    abundance_value = size * distr[i] * fungal_abundance/filesize
                    ab.write("%s\t%s\n" % (f[:-14], abundance_value))
                i = i + 1
            
if __name__ == "__main__":
    main()
