'''
File: make_strain_profile.py
Created Date: February 27th 2020
Author: ZL Deng <dawnmsg(at)gmail.com>
---------------------------------------
Last Modified: 27th February 2020 3:49:29 pm
'''

import sys
import click
from collections import defaultdict


@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('-o', '--output', type=str, help='The output CAMI2 profiling file')
def modify_profile(input, output):
    out_fh = open(output, 'w') if output else sys.stdout
    strain_count_dict = defaultdict(int)
    with open(input, 'r') as fh:
        for line in fh:
            if not line.startswith('@') and line.strip():
                if line.split('\t')[1] == 'strain':
                    cols = line.split('\t')
                    species = cols[0].split('.')[0]
                    strain_count_dict[species] += 1
                    cols[0] = '{}.{}'.format(
                        species, strain_count_dict[species])
                    line = '\t'.join(cols)
            out_fh.write(line)

    out_fh.close()


if __name__ == "__main__":
    modify_profile()
