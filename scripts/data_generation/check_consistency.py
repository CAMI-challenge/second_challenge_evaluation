#!/usr/bin/env python

import argparse
import os
import sys
from collections import Counter

defined_ranks = {}
parent_id_map = {}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nodes", help="NCBI Taxonomy file: nodes.dmp", required=True)
    parser.add_argument("--camitax", help="CAMITAX classification of genomes", required=True)
    parser.add_argument("--camisim", help="Database classification of genomes (form taxid\tname\tpath)")
    parser.add_argument("--path", help="Root path of the genomes")
    parser.add_argument("--unknown", help="Whether the database is public", action='store_false', default=True)
    parser.add_argument("-o", help="Output file name")
    args = parser.parse_args()
    define_ranks(args.nodes)
    if args.camisim is not None:
        genome_map = read_marref(args.camisim)
    else:
        genome_map = {}
        args.unknown = False
    create_camisim_input(genome_map, args.camitax, args.path, args.o, args.unknown)

def read_marref(marref):
    genome_map = {}
    with open(marref,'r') as mr:
        for line in mr:
            if line.startswith("Error"):
                continue
            taxid, name, path = line.strip().split('\t')
            genome_name = path.split("/")[-1].rstrip(".fasta")
            genome_map[genome_name] = (taxid, name, path, "known_strain")
    return genome_map

def create_camisim_input(genome_map, camitax, root_path, out, known):
    ranks = {'superkingdom':1, 'phylum':2, 'class':3, 'order':4, 'family':5, 'genus':6, 'species':7}
    ranks_rev = {1:'superkingdom', 2:'phylum', 3:'class', 4:'order', 5:'family', 6:'genus', 7:'species', 8:'strain'}
    with open(camitax,'r') as ct:
        for line in ct:
            spl = line.strip().split('\t')
            genome_name = spl[0]
            taxid_camitax = spl[1]
            seqLvl = spl[4]
            if genome_name in genome_map:
                taxid_marref, name, path, novelty = genome_map[genome_name]
                taxid = getLowNode([int(taxid_camitax), int(taxid_marref)])
            else:
                taxid = taxid_camitax # this is the only ID we have
                name = genome_name # or scientific name?
                path = os.path.join(root_path, "%s.fasta" % name)
            if not known:
                novelty = "new_%s" % (ranks_rev[ranks[seqLvl] + 1]) #get "real" novelty
            if not out:
                print "%s\t%s\t%s\t%s" % (taxid, name, path, novelty)
            else:
                with open(out, 'a+') as o:
                    o.write("%s\t%s\t%s\t%s\n" % (taxid, name, path, novelty))
           
"""
The following code is adapted (to Python 2.x) from CAMITAX (https://github.com/abremges/CAMITAX/blob/master/bin/camitaxonomy.py)
Thanks to abremges
"""
def getParent(ncbi_id):
    """Returns a node's parent node (or zero for the root node)"""
    parent_id = 0
    if ncbi_id in parent_id_map:
        parent_id = parent_id_map[ncbi_id]
    return parent_id if ncbi_id > 1 else 0
 
def define_ranks(nodes):
    with open(nodes) as f:
        ranks = {'superkingdom':1, 'phylum':2, 'class':3, 'order':4, 'family':5, 'genus':6, 'species':7}
        for line in f:
            spl = line.split('|')
            ncbi_id = spl[0]
            parent_id = spl[1]
            rank = spl[2]
            ncbi_id, parent_id, rank = int(ncbi_id.strip()), int(parent_id.strip()), rank.strip()
            parent_id_map[ncbi_id] = parent_id
            if rank in ranks:
                defined_ranks[ncbi_id] = ranks[rank]

def getLineage(ncbi_id):
    """Returns the defined full lineage (as NCBI IDs) of a taxon"""
    lineage = []
    while ncbi_id != 0:
        if ncbi_id in defined_ranks:
            lineage.insert(0, ncbi_id)
        ncbi_id = getParent(ncbi_id)
    return lineage

def getLowNode(taxon_list):
    """Get the lowest node without siblings in the tree spanned by taxon_list"""
    if not taxon_list:
        return 1
    ranks = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
    for taxon in taxon_list:
        for ncbi_id in getLineage(taxon):
            ranks[defined_ranks[ncbi_id]].append(ncbi_id)
    low_node = 1
    for rank in range(1, 8):
        rank_counter = Counter(ranks[rank])
        n = len(rank_counter)
        if n == 1:
            low_node = ranks[rank][0]
        elif n > 1:
            break
        # n == 0: incomplete lineage, skip gaps (e.g. for members of candidate phyla)
    return low_node

if __name__ == "__main__":
    main()
