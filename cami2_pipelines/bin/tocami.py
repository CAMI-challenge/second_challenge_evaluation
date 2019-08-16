#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
File: tocami.py --- generate CAMI profile, currently supports bracken and motus
Created Date: July 17th 2019
Author: ZL Deng <dawnmsg(at)gmail.com>
---------------------------------------
Last Modified: 17th July 2019 4:36:44 pm
'''

import os
import sys
import click
import time
import re
from ete3 import NCBITaxa


@click.command()
@click.option(
    "-f",
    "--format",
    type=click.Choice(["bracken", "motus"]),
    help="The input profile format",
    required=True)
@click.argument(
    'profile',
    type=click.Path(exists=True),
    required=True)
@click.option(
    '-t',
    '--taxdump',
    type=click.Path(exists=True),
    default=None,
    help="The taxdump.tar.gz file to create database."
)
@click.option(
    '-d',
    '--db',
    type=str,
    help="The folder to store the taxa.sqlite file.",
    required=True)
@click.option(
    '-o', "--output",
    type=str,
    default="",
    help='output CAMI profile file.')
def to_cami(format, profile, taxdump, db, output):
    dump_file = taxdump
    dbfile = os.path.join(db, "taxa.sqlite")
    global ncbi
    if os.path.exists(dbfile):
        ncbi = NCBITaxa(dbfile=dbfile)
    else:
        if taxdump is None:
            raise IOError(
                "The db is empty, you must specify the taxdump.tar.gz file to create the database.")
        ncbi = NCBITaxa(dbfile=dbfile, taxdump_file=dump_file)
    if format == "bracken":
        bracken_to_cami(profile, output)
    elif format == "motus":
        motus_to_cami(profile, output)


def bracken_to_cami(profile, output):
    outstream = (open(output, "w")
                 if output else sys.stdout)
    header = generate_header(profile)
    outstream.write(header)
    # print("Converting {} to CAMI profiling format".format(profile))
    tax_level_dict = {"S": "species",
                      "G": "genus",
                      "F": "family",
                      "O": "order",
                      "C": "class",
                      "P": "phylum"}
    with open(profile, 'r') as fh:
        for line in fh:
            if not line.startswith("name\ttaxonomy_id"):
                cols = line.strip().split("\t")
                name, taxid, level, rel_abd = [
                    cols[i] for i in [0, 1, 2, 6]]
                level = tax_level_dict[level]
                try:
                    taxon_path = get_taxon_path(taxid)
                except ValueError:
                    continue
                out_cols = [taxid, level, taxon_path[0],
                            taxon_path[1], rel_abd]
                outline = "\t".join(out_cols)
                outstream.write(outline + '\n')
    if output:
        outstream.close()


def motus_to_cami(profile, output):
    outstream = (open(output, "w")
                 if output else sys.stdout)
    header = generate_header(profile)
    outstream.write(header)
    # print("Converting {} to CAMI profiling format".format(profile))
    with open(profile, 'r') as fh:
        p = re.compile(r" -k (\w+) ")
        for line in fh:
            if line.startswith("# git tag"):
                level = re.findall(p, line)[0]
            elif not line.startswith("#"):
                cols = line.strip().split("\t")
                name, rel_abd = cols
                taxid = get_taxid(name)
                if taxid:
                    taxon_path = get_taxon_path(taxid)
                    out_cols = [taxid, level, taxon_path[0],
                                taxon_path[1], rel_abd]
                    outline = "\t".join(out_cols)
                    outstream.write(outline + '\n')
            else:
                continue
    if output:
        outstream.close()


def generate_header(input_profile):
    sample = os.path.basename(input_profile).split('.')[0]
    date = time.strftime("%Y%m%d")

    header = '''# Taxonomic Profiling Output
@SampleID:{}
@Version:0.9.1
@Ranks:superkingdom|phylum|class|order|family|genus|species|strain
@TaxonomyID:ncbi-taxonomy_{}
@@TAXID	RANK	TAXPATH	TAXPATHSN	PERCENTAGE
'''.format(sample, date)
    return header


def get_taxid(name):
    taxid = ncbi.get_name_translator([name])
    try:
        return str(taxid[name][0])
    except KeyError:
        return None


def get_taxon_path(taxid):
    try:
        taxid_list = ncbi.get_lineage(taxid)
    except ValueError:
        raise
    kept_levels = ["superkingdom", "phylum", "class",
                   "order", "family", "genus", "species"]

    rank_dict = ncbi.get_rank(taxid_list)
    kept_taxids = []

    for level in kept_levels:
        for k, v in rank_dict.items():
            if v == level:
                kept_taxids.append(k)
    taxsn_dict = ncbi.get_taxid_translator(kept_taxids)
    taxid_path = "|".join(map(str, kept_taxids))
    taxsn_path = "|".join([taxsn_dict[tax] for tax in kept_taxids])
    return [taxid_path, taxsn_path]


if __name__ == "__main__":
    to_cami()
