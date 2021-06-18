## AMBER command for the binning of the gold standard assembly of the marine dataset

~~~BASH
amber.py -g ../../genome_binning/marine_dataset/data/ground_truth/gsa_pooled_mapping_short.binning \
data/submissions/short_read_pooled_gold_standard_assembly/hopeful_kirch_0.binning \
data/submissions/short_read_pooled_gold_standard_assembly/naughty_blackwell_0.binning \
data/submissions/short_read_pooled_gold_standard_assembly/kraken2.0.8beta_marine.binning \
data/submissions/short_read_pooled_gold_standard_assembly/diamond0.9.28_marine.binning \
data/submissions/short_read_pooled_gold_standard_assembly/megan6.15.2_marine.binning \
--ncbi_dir ../ \
-l "LSHVec cami2,PhyloPythiaS+ 1.4, Kraken 2.0.8-beta, DIAMOND 0.9.28, MEGAN 6.15.2" \
-o data/results/amber_marine_contigs --filter 1
~~~

## AMBER command for the binning of the gold standard assembly of the marine dataset (by novelty category)

~~~BASH
myvars=("known_strain" "new_family" "new_genus" "new_order" "new_species" "new_strain" "plasmid" "unknown" "virus"); \
for x in "${myvars[@]}"; do \
amber.py -g data/ground_truth/gsa_pooled_mapping_short.${x}.binning \
data/submissions/short_read_pooled_gold_standard_assembly/hopeful_kirch_0.${x}.binning \
data/submissions/short_read_pooled_gold_standard_assembly/naughty_blackwell_0.${x}.binning \
data/submissions/short_read_pooled_gold_standard_assembly/kraken2.0.8beta_marine.${x}.binning \
data/submissions/short_read_pooled_gold_standard_assembly/diamond0.9.28_marine.${x}.binning \
data/submissions/short_read_pooled_gold_standard_assembly/megan6.15.2_marine.${x}.binning \
--ncbi_dir ../ \
-l "LSHVec cami2,PhyloPythiaS+ 1.4, Kraken 2.0.8-beta, DIAMOND 0.9.28, MEGAN 6.15.2" \
-o data/results/amber_marine_deep_branching/${x} --filter 1 \
; done
~~~

## AMBER command for the binning of the marine short-read samples

Binnings are available at [Zenodo](https://zenodo.org/communities/cami/).

~~~BASH
for i in {0..9}; do \
amber.py -g marmgCAMI2_short_read_reads_mapping_sample_${i}.binning \
grave_ritchie_0.tax.marmgCAMI2_short_read_sample_${i}.binning \
nbcpp_marine_short_read_sample_${i}.binning \
hopeful_lovelace_0.marmgCAMI2_short_read_sample_${i}.binning \
kraken2.0.8beta_marine_short_read_sample_${i}.binning \
kraken0.10.5beta_marine_sample_${i}.binning \
diamond0.9.28_marine_short_read_sample_${i}.binning \
--ncbi_dir ncbi_taxonomy \
-l "Ganon 0.1.4,NBCpp,LSHVec cami2,Kraken 2.0.8-beta,Kraken 0.10.5-beta,Diamond 0.9.28" \
-o data/results/amber_marine_short_reads_sample_${i} --filter 1 & done
~~~

## AMBER command for the binning of the marine long-read samples

~~~BASH
amber.py -g marmgCAMI2_long_read.binning \
stupefied_feynman_0.binning \
--ncbi_dir ../ \
-l "LSHVec cami2" \
-o data/results/amber_marine_long_reads --filter 1
~~~
