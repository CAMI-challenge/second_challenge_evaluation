Handling of the genomes provided (called "new genomes") and the genomes from the database (called "database genomes"):
1. Downloaded metadata and genomes from database (MarRef, ProGenomes), assemble other genomes
    1. Metadata:
        1. Marine: https://s1.sfb.uit.no/public/mar/MarRef/Metadatabase/Current.tsv
        2. Terrestrial: header of the terrestrial contig file
    2. Reference genomes:  
        1. Marine: https://s1.sfb.uit.no/public/mar/MarRef/Genomes/
        2. Terrestrial: http://progenomes.embl.de/data/habitats/terrestrial/terrestrial.repr.contigs.fasta.gz
    3. New genomes:
        1. Marine: Reads + Standard SPAdes 3.12 (--careful flag)
        2. Strain madness: Reads + Standard SPAdes 3.12 (--careful), filter failed assemblies
        3. Terrestrial: Reads + Standard SPAdes 3.12 (--careful)
2. Size filtration, remove all contigs <1000bp (“seqtk seq -L 1000”)
3. Match genomes to Metadata via script "/net/sgi/cami/data/CAMI2/scripts/create_metadata.py" (if required, for marine genomes)
    1. python create_metadata.py -m metadata_full.tsv -g genomes_to_be_used -o out_path 2> erroneous_genomes.log
    2. Some genomes didn't map because of naming inconsistencies and special characters, these were discarded (erroneous_genomes.log)
4. Remove contaminated genomes from database/new genomes
    1. Remove if ((Completeness <90% or Contamination > 5%) and #contigs > 1), command `cat camitax.tsv | awk 'BEGIN {FS="\t"} ($7 >= 90 && $8 <= 5) || $11 == 1' > camitax_filtered.tsv`
    2. If single contig, we believe higher continuity over CheckM contamination score
5. Checking consistency of genome assignments versus the CAMITAX assignment via script "/net/sgi/cami/data/CAMI2/scripts/check_consistency.py"
    1. e.g. python check_consistency.py --nodes taxonomy/nodes_20180510.dmp --camitax camitax_filtered.tsv --camisim camisim.tsv --path /net/sgi/cami/data/CAMI2/nwillassen_data/marine/marine_filtered > camisim_references.tsv (add --unknown flag if the database/metadata is not public)
    2. Assign genomes the lowest consistent assignment between CAMITAX and MarRef/other annotation, has to be legal rank (i.e. losing strain, because it is not a NCBI rank)
    3. Prints mapping which can be used as reference genome input for CAMISIM or alternatively, if not from_profile is run: use the script split_metadata.py camisim_reference.tsv simulation_path/ to append the genomes to genome_to_id.tsv and metadata.tsv for CAMISIM in de novo mode
    4. If so desired (i.e. for adding plasmids afterwards), run a community design only run of CAMISIM (new feature) to create metadata.tsv and genome_to_id.tsv and abundance files from which a “de novo” CAMISIM run can be started after plasmid addition
        1. Rhizosphere only (5.4.1 and 5.4.2): For the further elucidation of the effects of strain variability and the difference between single-sample versus cross-sample assemblies, a subset of genomes were manually selected and their abundance was also set manually.
        2. For testing strain variability, 5 clusters of more than 2 genomes with a within-cluster similarity of more than 97% were selected
        3. For testing low abundance/single vs cross-assembly, 5 genomes which did not have any closely related strains (no significant ANI matches at any %) were selected and their abundance distributed among the 20 samples the following way: https://docs.google.com/spreadsheets/d/1yM397miZR9N1RBGOt1X89XBuGF5EZG23ml2TW8_F0Ik/edit#gid=1374755187
        4. Additionally, 10% of the data set were reserved for host genome data (1% A. thaliana reads) as well as fungal (9%) data. To this end a dry-run was performed with 99.9% ANI similarity filtered genomes (Choose only one representative genome for every cluster with within-cluster similarities of >99.9% - dRep) as well as filtered from the genomes chosen in steps 5.4.1.1 and 5.4.1.2. Using the total abundances of the dry-run plus added plasmids (see 6.) as 100%, the 9% (for 55 fungal genomes) and 1% (A. thaliana) are added. Since the fungal genomes are much longer, they - similar to the plasmids - need an abundance factor such that they contribute 9% of reads/sequence data and not 9% of abundance which would be roughly 10x more data.

```python create_rhizosphere_data.py -g /net/sgi/cami/data/dRep/drep-outout_directory-LOTUS-999/dereplicated_genomes/ -c /net/sgi/cami/data/CAMI2/roter_data/lotus_rhizosphere/CAMISIM_dryrun/camitax.tsv -o /net/sgi/cami/data/CAMI2/roter_data/lotus_rhizosphere/CAMISIM_dryrun/references.tsv```

Dry-run:

```python metagenome_from_profile.py -p /net/sgi/cami/data/CAMI2/roter_data/lotus_rhizosphere/16Snew/final_otutab_taxonomy.biom -o /net/sgi/cami/data/CAMI2/roter_data/lotus_rhizosphere/CAMISIM_run/ -ref /net/sgi/cami/data/CAMI2/roter_data/lotus_rhizosphere/CAMISIM_run/empty_references -ar /net/sgi/cami/data/CAMI2/roter_data/lotus_rhizosphere/CAMISIM_run/references.tsv -c /net/sgi/cami/data/CAMI2/roter_data/lotus_rhizosphere/CAMISIM_run/input_config.ini -tmp /tmp -nr -f -dr --seed 9092019```

Adding fungal genomes:

```./add_extra_genomes_to_rhizosphere.py -m /net/sgi/cami/data/CAMI2/lhansen_data/plasmids/assembly/metadata.tsv -p /net/sgi/cami/data/CAMI2/lhansen_data/plasmids/assembly/long_read -e /net/sgi/cami/data/CAMI2/nwillassen_data/marine/simulation_short_read/metadata.tsv -f /net/sgi/cami/data/CAMI2/fungal_genomes/assemblies/ -md /net/sgi/cami/data/CAMI2/roter_data/lotus_rhizosphere/CAMISIM_run/metadata.tsv -id /net/sgi/cami/data/CAMI2/roter_data/lotus_rhizosphere/CAMISIM_run/genome_to_id.tsv -s 9092019 -o /net/sgi/cami/data/CAMI2/roter_data/lotus_rhizosphere/CAMISIM_run/ -size 5000000```
This also adds the remaining plasmids to the data set (replacing point 6). The fungal genomes’ distribution is drawn from a lognormal distribution with mean 1 and variance 2 (values from CAMI1) for the first sample, for all the other samples this abundance value is multiplied with gaussian noise of the form N(1,0.1) (mean 1, standard deviation 0.1)

Using the table /net/sgi/cami/data/CAMI2/roter_data/lotus_rhizosphere/CAMISIM_run/added_genomes.tsv (manually created after https://docs.google.com/spreadsheets/d/1yM397miZR9N1RBGOt1X89XBuGF5EZG23ml2TW8_F0Ik/edit#gid=1374755187):
```./add_manual_genomes.py -o /net/sgi/cami/data/CAMI2/roter_data/lotus_rhizosphere/CAMISIM_run/ -m /net/sgi/cami/data/CAMI2/roter_data/lotus_rhizosphere/CAMISIM_run/added_genomes.tsv -g /net/sgi/cami/data/dRep/drep-outout_directory-LOTUS-999/dereplicated_genomes/ -s 5000000000```

5. add manually selected genomes using the script add_manual_genomes.py
6. Add plasmids/circular elements with add_plasmids.py script
    1. e.g. python add_plasmids.py -i /net/sgi/cami/data/CAMI2/nwillassen_data/marine/simulation_long_read/ -m /net/sgi/cami/data/CAMI2/lhansen_data/plasmids/assembly/metadata.tsv -s 6082018 -n 200 -mu 1 -sd 0.1 -p /net/sgi/cami/data/CAMI2/lhansen_data/plasmids/assembly/long_read/
    2. Plasmids treated as below in this file for short/long read simulation
    3. Randomly select x plasmids (i.e. 200 for marine) to be added
    4. From the first sample, select 200 highest abundant genomes, “map” selected plasmids to the genomes and add plasmids to sample with the following abundance calculation
    5. Choose as abundance: original abundance x abundance factor x gaussian noise
        1. with abundance factor = 1.5x for (for all 10 “sub-plasmids”) and gaussian noise = Normal(1,0.1), low variance so no 0 values occur.
    6. Update config.ini with number of additional plasmids (genomes_total/genomes_real numbers)
7. Run CAMISIM with ./metagenomesimulation config.ini
8. Move required subsets of output to desired format and location with
```./move_reads in_folder out_folder read_type prefix```

With “prefix” being: 3 letters for the origin of the dataset, 2 letters for the type of dataset, followed by CAMI and the number of the challenge, i.e. marmgCAMI2 for MARine MetaGenome CAMI 2
“in_folder” is the original CAMISIM run (absolute path)
“out_folder” the desired output root folder (absolute path)
“read_type” is one of “short_read”, “long_read” or “hybrid”
This script creates the folder specified with “out_folder” with subdirectories
reads
assembly
simulation_${read_type}

The reads folder contains all the reads in the nomenclature “${prefix}_${read_type}_sample_${sample_nr}_reads.fq.gz”

The assembly folder contains all assemblies in the nomenclature
“${prefix}_${read_type}_${sample}_gsa.fasta.gz” as well as the pooled gsa
“${prefix}_${read_type}_pooled_gsa.fasta.gz”

The simulation folder contains the original/complete CAMISIM output sans the read and assembly files. Instead it contains a script which calculates the root path of the downloaded data within that script - found under /net/sgi/cami/data/CAMI2/scripts/create_symlinks.py -, creates symbolic links to the read and assembly files stored in the corresponding folder.
