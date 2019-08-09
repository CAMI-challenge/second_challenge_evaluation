#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
File: rm_invalid_taxa.py
Created Date: August 9th 2019
Author: ZL Deng <dawnmsg(at)gmail.com>
---------------------------------------
Last Modified: 9th August 2019 11:12:02 am
'''

import click


@click.command()
@click.argument(
    "camiprofiles",
    type=click.Path(exists=True),
    nargs=-1,
    required=True)
@click.option(
    '-n', "--nodedmp",
    type=click.File("r"),
    required=True,
    help='The nodes.dmp file to check the validity of profiling file')
def rm_invalid_taxa(camiprofiles, nodedmp):
    valid_taxids = taxid_set(nodedmp)
    for profile in camiprofiles:
        out_profile = ".valid.".join(profile.rsplit(".", 1))
        out_fh = open(out_profile, "w")
        with open(profile, "r") as fh:
            header, body = split_header_body(fh)
            out_fh.writelines(header)
            for line in body:
                cols = line.strip().split("\t")
                taxid = cols[0]
                taxid_path = cols[2]
                if taxid in valid_taxids:
                    new_taxid_path = "|".join((parent_taxid for parent_taxid in taxid_path.split(
                        "|") if parent_taxid in valid_taxids))
                    out_fh.write(
                        "\t".join(cols[:2] + [new_taxid_path] + cols[3:]) + "\n")
                else:
                    print(
                        "{} - found invalid taxid:\t{}\tabundance:\t{}".format(profile, taxid, cols[4]))
            out_fh.close()


def taxid_set(nodedmp):
    taxids = set()
    for line in nodedmp:
        taxid, _ = line.split("\t", 1)
        taxids.add(taxid)
    return taxids


# Split the file into header and body stream
def split_header_body(fh, comment_chars=('#', '@')):
    header = []
    while peek_line(fh).startswith(comment_chars):
        header.append(fh.readline())
    else:
        return header, fh


# Peek the line without advancing the position
def peek_line(fh):
    pos = fh.tell()
    line = fh.readline()
    fh.seek(pos)
    return line


if __name__ == "__main__":
    rm_invalid_taxa()
