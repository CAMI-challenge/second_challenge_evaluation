#!/usr/bin/env python

import sys
import os
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", help="Path of input genomes", required=True)
    parser.add_argument("-c", help="Path of camitax results", required=True)
    parser.add_argument("-o", help="reference outfile", required=True)
    args = parser.parse_args()
    cmap = create_camitax_mapping(args.c)
    create_reference_file(args.g, cmap, args.o)
    
def create_camitax_mapping(camitax_file_path):
    ranks = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain']
    cmap = {}
    with open(camitax_file_path, 'r') as f:
        for line in f:
            if not line.startswith("Genome"):
                split = line.strip().split('\t')
                name = split[0]
                taxid = split[1]
                try:
                    novelty = "new_" + ranks[ranks.index(split[3]) + 1]
                except IndexError:
                    novelty = "new_strain"
                cmap[name] = (taxid, novelty)
    return cmap

def create_reference_file(path, cmap, outfile):
    files = os.listdir(path)
    with open(outfile, 'a+') as write_file:
        for f in files:
            split = f.strip().split('.')
            if len(split) > 2: # reference genomes (have their taxid as first part)
                name = split[1]
                taxid = split[0]
                novelty = "known_strain"
            else:
                name = split[0]
                taxid, novelty = cmap[name]
            file_path = os.path.join(path, f)
            to_write = "%s\t%s\t%s\t%s\n" % (taxid, name, file_path, novelty)
            write_file.write(to_write)

if __name__ == "__main__":
    main()
