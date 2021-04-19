#!/usr/bin/env python

import sys
import os
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", help="Genomes path", required=True)
    parser.add_argument("-m", help="Metadata file (for MarRef)")
    parser.add_argument("-o", help="Output file")
    args = parser.parse_args()
    create_metadata(args)

def remove_special_chars(word, chars, strings = None):
    new_word = word
    for char in chars:
        new_word = new_word.replace(char," ")
    if strings is not None:
        for string in strings:
            new_word = new_word.replace(string[0],string[1])
    return " ".join(new_word.split())

def create_metadata(args): #genomes, used_genomes, metadata):
    genomes = os.listdir(args.g)
    md_map = {}
    if (args.m is not None):
        with open(args.m,'r') as md:
            for line in md:
                l = line.strip().split('\t')
                taxid = l[11]
                fname = remove_special_chars(l[13].replace("(T)",""),"=/\,()'_",[("--","-"),(".","")]) # clunky removal of special characters
                md_map[fname.lower()] = taxid # lowercase so its case-insensitive
    for genome in genomes:
        if genome == "index.html" or not genome.endswith("_genomic.fa"):
            continue
        name = " ".join(genome.strip().split("_")[:-1]) #remove _genomic.fasta
        if (args.m is not None):
            path = os.path.join(args.g,genome)
            try:
                md_map[name.lower()]
                with open(args.o,'a+') as out:
                    out.write(md_map[name.lower()] + '\t' + name + '\t' + path + '\n')
            except KeyError:
                sys.stderr.write("Error for %s\n" % name)
        else: #TODO
            genome_name = genome
            name = genome
            path = os.path.join(args.g, genome)
            out.write(genome_name + '\t' + name + '\t' + path + '\n')

if __name__ == "__main__":
    main()
