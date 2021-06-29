#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
File: focus2cami.py --- convert FOCUS combined output to CAMI profiling format
Created Date: July 17th 2019
Author: ZL Deng <dawnmsg(at)gmail.com>
---------------------------------------
Last Modified: 17th July 2019 4:36:44 pm
'''

import sys
import click
import time
import re
import pandas as pd
from os import path
from ete3 import NCBITaxa


@click.command()
@click.option(
    "-f",
    "--format",
    type=click.Choice(["focus"]),
    default='focus',
    help="The input profile format")
@click.argument(
    'profiles',
    type=click.Path(exists=True),
    nargs=-1,
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
    '-o',
    '--outdir',
    type=click.Path(exists=True),
    default=path.dirname(path.abspath(__file__)),
    help='The output dir for profile files.'
)
def to_cami(format, profiles, taxdump, db, outdir):
    dump_file = taxdump
    dbfile = path.join(db, "taxa.sqlite")
    global ncbi
    if path.exists(dbfile):
        ncbi = NCBITaxa(dbfile=dbfile)
    else:
        if taxdump is None:
            raise IOError(
                "The db is empty, you must specify the taxdump.tar.gz file to create the database.")
        ncbi = NCBITaxa(dbfile=dbfile, taxdump_file=dump_file)

    if format == "focus":
        focus_to_cami(profiles, outdir)


def focus_to_cami(profile, outdir):

    sample_profile_dict = {}
    uid_pattern = re.compile(' uid[0-9]+$')
    for pf in profile:
        df = pd.read_csv(pf, index_col=0)
        rank = df.index.name.lower()
        df.index = df.index.str.replace('_', ' ')
        df.columns = [sample.split('.')[0] for sample in df.columns]
        # print(df.head())
        for taxon, samples in df.iterrows():
            if rank == 'strain':
                taxon = uid_pattern.sub('', taxon)
                print(taxon)
            taxid = get_taxid(taxon)
            if not taxid:
                continue

            taxon_path = get_taxon_path(taxid)

            for sample, rel_abd in samples.iteritems():
                out_line = '\t'.join(
                    [taxid, rank, taxon_path[0], taxon_path[1], str(rel_abd)]) + '\n'
                if sample in sample_profile_dict:
                    sample_profile_dict[sample] += out_line
                else:
                    header = generate_header(sample)
                    sample_profile_dict[sample] = header + out_line
    for sample, pf_data in sample_profile_dict.items():
        out_fh = open(path.join(outdir, sample + '.focus.profile'), 'w')
        out_fh.write(pf_data)
        out_fh.close()


def generate_header(sampleid):
    date = time.strftime("%Y%m%d")

    header = '''# Taxonomic Profiling Output
@SampleID:{}
@Version:0.9.1
@Ranks:superkingdom|phylum|class|order|family|genus|species|strain
@TaxonomyID:ncbi-taxonomy_{}
@@TAXID	RANK	TAXPATH	TAXPATHSN	PERCENTAGE
'''.format(sampleid, date)
    return header


def get_taxid(name):
    taxid = ncbi.get_name_translator([name])
    try:
        return str(taxid[name][0])
    except KeyError:
        return None


def get_name(taxid):
    name = ncbi.get_taxid_translator([taxid])
    try:
        return str(name[taxid][0])
    except KeyError:
        return None


def get_level(taxid):
    taxid = int(taxid)
    level = ncbi.get_rank([taxid])
    try:
        return str(level[taxid])
    except KeyError:
        return None


def get_taxon_path(taxid):
    try:
        taxid_list = ncbi.get_lineage(taxid)
    except ValueError:
        raise
    kept_levels = ["superkingdom", "phylum", "class",
                   "order", "family", "genus", "species", "strain"]

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
