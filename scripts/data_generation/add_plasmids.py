#!/usr/bin/env python

import os
import sys
import random
from numpy import random as np_rand
import argparse
import shutil

def parse_options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i",help="CAMISIM dry-run path", type=str)
    parser.add_argument("-m",help="Path to plasmid metadata tsv file (path, OTU, NBCI, novelty", type=str)
    parser.add_argument("-s",help="random seed", type=int)
    parser.add_argument("-n",help="Number of plasmids to be added (<= plasmids in metadata file", type=int)
    parser.add_argument("-mu",help="Gaussian noise mean",default=1,type=float)
    parser.add_argument("-sd",help="Gaussian noise sd",default=0.1,type=float)
    parser.add_argument("-r",help="True if short read, False if long read", default=True, action='store_true')
    parser.add_argument("-p",help="Path to plasmid genomes fasta files",type=str)
    if not len(sys.argv) > 8: #TODO
        parser.print_help()
        return None
    args = parser.parse_args()
    return args

def init(seed):
    random.seed(seed)
    np_rand.seed(seed)

def get_factor(short_read): #calculate factor s.t. plasmids are covered 15x more than genomes on average
    return 1.5 # for all data sets we chose the 10 files per plasmids
    #if short_read: # if short_read: files are 6x concatenated
    #    factor = 2.5
    #else: # if long read: 10 files per plasmid
    #    factor = 1.5
    #return factor

def read_metadata(p_metadata):
    metadata = []
    with open(p_metadata, 'r') as md:
        for line in md:
            plasmid, otu, ncbi, nov = line.strip().split('\t')
            metadata.append((plasmid, otu, ncbi, nov))
    return metadata

def copy_plasmids(chosen_plasmids, out_path, in_path, short_read):
    plasmid_out = os.path.join(out_path,'genomes')
    for plasmid, otu, ncbi, nov in chosen_plasmids:
        shutil.copy2(os.path.join(in_path,plasmid),plasmid_out)
        with open(os.path.join(out_path,"metadata.tsv"),'a+') as md:
            md.write("%s\t%s\t%s\t%s\n" % (plasmid.rstrip(".fasta"), otu, ncbi, nov))
        with open(os.path.join(out_path, "genome_to_id.tsv"), 'a+') as gid:
            gid.write("%s\t%s\n" % (plasmid.rstrip(".fasta"), os.path.join(out_path,'genomes', plasmid)))
        
def add_plasmids(out_path, in_path, metadata, num_plasmids, mu, sd, short_read):
    indices = np_rand.choice(len(metadata), num_plasmids, replace=False) # select indices of plasmids to add
    chosen = [metadata[i] for i in indices]
    copy_plasmids(chosen, out_path, in_path, short_read) # also writes to metadata and genome_to_id
    abundances = []
    plasmid_map = {}
    first_sample = True
    files = os.listdir(out_path)
    to_add = []
    for f in files:
        if (f.startswith("abundance")):
            abundances = []
            with open(os.path.join(out_path,f),'r+') as abundance:
                for line in abundance:
                    gen, ab = line.strip().split('\t')
                    abundances.append((gen,float(ab)))
            with open(os.path.join(out_path,f),'a+') as abundance:
                if first_sample:
                    abundances.sort(key=lambda x : x[1], reverse=True) # add plasmids for highest abundant genomes from first sample
                    for i in range(len(indices)): 
                        plasmid_map[abundances[i][0]] = metadata[indices[i]] # match genomes and plasmids
                    first_sample = False
                to_write = ""
                for g, abun in abundances:
                    if g in plasmid_map:
                        ab = float(abun)
                        plasmid,x,y,z = plasmid_map[g] # we dont need the other information
                        normal_abundance = ab * get_factor(short_read) * np_rand.normal(mu, sd, 1)[0]
                        to_write += "{plasmid}\t{ab}\n".format(plasmid=plasmid.rstrip(".fasta"),ab=normal_abundance)
                abundance.write(to_write) 

def main():
    args = parse_options()
    if args is None:
        return
    out_path = args.i
    md = args.m
    seed = args.s
    nr = args.n
    mu = args.mu
    sd = args.sd
    r = args.r
    in_path = args.p
    init(args.s)
    metadata = read_metadata(md)
    add_plasmids(out_path, in_path, metadata, nr, mu, sd, False) # r should always be false, makes no difference as of yet

if __name__ == "__main__":
    main()

