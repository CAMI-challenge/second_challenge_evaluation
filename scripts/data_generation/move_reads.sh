#!/bin/bash

# Script for moving the reads from CAMISIM to a new folder with new prefix which can be used online as challenge, only containing the read files of the input CAMISIM run

in_folder=$1
out_folder=$2
read_type=$3
prefix=$4

# symbolic link for read files
mkdir -p $out_folder/reads
if [[ $read_type != *"hybrid"* ]]
then
    for read_file in $in_folder/20*/reads/*.fq.gz
    do
    sample_nr=${read_file%/*/*}
    sample_nr=${sample_nr#*/*}
    sample_nr=${sample_nr##*_}
    file_name=${out_folder}/reads/${prefix}_${read_type}_sample_${sample_nr}_reads.fq.gz
    ln -s $read_file $file_name
    done
fi

# symbolic link for short/long read pooled gsa
mkdir -p $out_folder/assembly

# symbolic link for hybrid gsa per sample and pooled

if [[ $read_type == *'hybrid'* ]] # has different folder structure
then
    for sample in $in_folder/*
    do
        sample=${sample##*/}
        if [ $sample = 'pooled' ]
        then
            ln -s $in_folder/pooled/*.fasta.gz ${out_folder}/assembly/${prefix}_${read_type}_pooled_gsa.fasta.gz
        else
            sample=sample_${sample##*_}
            ln -s $in_folder/$sample/*.fasta.gz ${out_folder}/assembly/${prefix}_${read_type}_${sample}_gsa.fasta.gz
        fi
    done
else # similar to reads
    ln -s $in_folder/anonymous_gsa_pooled.fasta.gz ${out_folder}/assembly/${prefix}_${read_type}_pooled_gsa.fasta.gz
    for assembly_file in $in_folder/20*/contigs/*.fasta.gz # symbolic link for short/long read gsa per sample
    do
        sample_nr=${assembly_file%/*/*}
        sample_nr=${sample_nr#*/*}
        sample_nr=${sample_nr##*_}
        file_name=${out_folder}/assembly/${prefix}_${read_type}_sample_${sample_nr}_gsa.fasta.gz
        ln -s $assembly_file $file_name
    done
fi

#now symlink to the full folder without reads and assembly
mkdir -p $out_folder/simulation
cp -as $in_folder $out_folder/simulation/simulation_${read_type}
if [[ $read_type != *'hybrid'* ]]
then
    for reads in $out_folder/simulation/simulation_${read_type}/20*/reads/*.fq.gz
    do
        rm -f $reads
    done
    rm -f $out_folder/simulation/simulation_${read_type}/anonymous_gsa_pooled.fasta.gz
    for assembly in $out_folder/simulation/simulation_${read_type}/20*/contigs/*.fasta.gz
    do
        rm -f $assembly
    done
else
    for assembly in $out_folder/simulation/simulation_${read_type}/*/*.fasta.gz
    do
        rm -f $assembly
    done
fi
