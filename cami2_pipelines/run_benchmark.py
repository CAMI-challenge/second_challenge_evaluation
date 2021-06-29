#!/usr/bin/env python3
# -- coding: utf-8 --
'''
File: run_benchmark.py
Created Date: May 16th 2019
Author: ZL Deng <dawnmsg(at)gmail.com>
---------------------------------------
Last Modified: 29th July 2019 12:03:45 pm
'''

import os
import sys
import click
import snakemake

wd = os.path.dirname(os.path.realpath(__file__))
VERSION = '0.1'


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo("Version {}".format(VERSION))
    ctx.exit()


@click.command(help="Benchmarking for CAMI dataset")
@click.option("-e",
              "--evaluation",
              required=True,
              # "binning"]),
              type=click.Choice(["all", "profile", "assembly"]),
              help="The evaluation to run."
              )
@click.option("-t",
              "--threads",
              type=int,
              default=2,
              show_default=True,
              help="The number of threads to use.")
@click.option("-d",
              "--dryrun",
              is_flag=True,
              default=False,
              show_default=True,
              help="Print the details without run the pipeline."
              )
@click.option("-c",
              "--conda_prefix",
              type=click.Path(exists=True),
              default=None,
              help="The prefix of conda ENV. [default: in the working directory].")
@click.option("-o",
              "--out_dir",
              type=click.Path(),
              default=None,
              help="The directory for outputs. \
The path can be specified either in the CLI here as option or in the config file.")
@click.option("--version", is_flag=True, callback=print_version,
              expose_value=False, is_eager=True, help="Print the version.")
def execute(evaluation, dryrun=False, conda_prefix=None, **kwargs):
    profile_smk = os.path.join(wd, "profiling.smk")
    assembly_smk = os.path.join(wd, "assembly.smk")
    #binning_smk = os.path.join(wd, "binning.smk")
    # snake_kwargs = dict(runOnReads=slow)
    snake_kwargs = {}
    for arg, val in kwargs.items():
        if val != None:
            snake_kwargs[arg] = val
    if evaluation == "profile":
        snakes = [profile_smk]
    elif evaluation == "assembly":
        snakes = [assembly_smk]
    # elif evaluation == "binning":
    #     snakes = [binning_smk]
    else:
        snakes = [profile_smk, assembly_smk]  # , binning_smk]
    for snake in snakes:
        run_snake(snake, dryrun, conda_prefix, **snake_kwargs)


def run_snake(snake, dryrun=False, conda_prefix=None, **kwargs):
    try:
        # Unlock the working directory
        unlocked = snakemake.snakemake(
            snakefile=snake,
            # unlock=False,
            unlock=True,
            workdir=wd,
            config=kwargs
        )
        if not unlocked:
            raise Exception('Could not unlock the working directory!')

        # Start the snakemake pipeline
        success = snakemake.snakemake(
            snakefile=snake,
            restart_times=3,
            cores=kwargs.get("threads", 2),
            workdir=wd,
            use_conda=True,
            conda_prefix=conda_prefix,
            dryrun=dryrun,
            printshellcmds=True,
            force_incomplete=True,
            config=kwargs
        )
        if not success:
            raise Exception('Snakemake pipeline failed!')
    except Exception as e:
        from datetime import datetime
        print('ERROR ({})'.format(snake))
        print('{}\t{}\n'.format(
            datetime.now().isoformat(' ', timespec='minutes'),
            e))
        raise RuntimeError(e)
    except:
        from datetime import datetime
        print('ERROR ({})'.format(snake))
        print('{}\t{}\n'.format(
            datetime.now().isoformat(' ', timespec='minutes'),
            sys.exc_info()))
        raise RuntimeError(
            'Unknown problem occured when lauching Snakemake!')


if __name__ == "__main__":
    execute()
