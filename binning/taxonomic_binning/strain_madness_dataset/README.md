## AMBER command for the binning of the gold standard assembly of the strain madness dataset

~~~BASH
amber.py -g ../../genome_binning/strain_madness_dataset/data/ground_truth/gsa_pooled_mapping.binning \
data/submissions/short_read_pooled_gold_standard_assembly/hopeful_kirch_3.binning \
data/submissions/short_read_pooled_gold_standard_assembly/ppsp1.4_strain_madness.binning \
data/submissions/short_read_pooled_gold_standard_assembly/kraken2.0.8beta_strain_madness.binning \
data/submissions/short_read_pooled_gold_standard_assembly/diamond0.9.28_strain_madness.binning \
data/submissions/short_read_pooled_gold_standard_assembly/megan6.15.2_strain_madness.binning \
--ncbi_dir ../ \
-l "LSHVec cami2,PhyloPythiaS+ 1.4,Kraken 2.0.8-beta,DIAMOND 0.9.28,MEGAN" \
-o data/results/amber_strain_madness_contigs --filter 1
~~~

## AMBER command for the binning of the gold standard assembly of the strain madness dataset (by novelty category)

~~~BASH
myvars=("new_genus" "new_order" "new_species" "new_strain"); \
for x in "${myvars[@]}"; do \
amber.py -g data/ground_truth/gsa_pooled_mapping.${x}.binning \
data/submissions/short_read_pooled_gold_standard_assembly/hopeful_kirch_3.${x}.binning \
data/submissions/short_read_pooled_gold_standard_assembly/ppsp1.4_strain_madness.${x}.binning \
data/submissions/short_read_pooled_gold_standard_assembly/kraken2.0.8beta_strain_madness.${x}.binning \
data/submissions/short_read_pooled_gold_standard_assembly/diamond0.9.28_strain_madness.${x}.binning \
data/submissions/short_read_pooled_gold_standard_assembly/megan6.15.2_strain_madness.${x}.binning \
--ncbi_dir ../ \
-l "LSHVec cami2,PhyloPythiaS+ 1.4,Kraken 2.0.8-beta,DIAMOND 0.9.28,MEGAN" \
-o data/results/amber_strain_madness_deep_branching/${x} --filter 1 \
; done
~~~

## AMBER command for the binning of the strain madness short-read samples

Binnings are available at [Zenodo](https://zenodo.org/communities/cami/).

~~~BASH
for i in {0..99}; do \
amber.py -g strain_madness_short_reads.strmgCAMI2_short_read_sample_${i}.binning \
grave_ritchie_2_sample_${i}.tax.binning \
kraken2.0.8beta_strain_madness_short_read_sample_${i}.binning \
kraken0.10.5beta_strain_madness_short_read_sample_${i}.binning \
--ncbi_dir ../ \
-l "Ganon 0.1.4,Kraken 2.0.8-beta,Kraken 0.10.5-beta" \
-o data/results/amber_strain_madness_short_reads_sample_${i} --filter 1 & done
~~~

## AMBER command for the binning of the strain madness long-read samples

~~~BASH
amber.py -g strmgCAMI2_long_read.binning \
stupefied_feynman_1.binning \
--ncbi_dir ../ \
-l "LSHVec cami2" \
-o data/results/amber_strain_madness_long_reads --filter 1
~~~
