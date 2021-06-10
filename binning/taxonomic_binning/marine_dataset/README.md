## AMBER command for the binning of the gold standard assembly of the marine dataset

~~~BASH
amber.py -g ../../genome_binning/marine_dataset/data/ground_truth/gsa_pooled_mapping_short.binning \
data/submissions/short_read_pooled_gold_standard_assembly/hopeful_kirch_0.binning \
data/submissions/short_read_pooled_gold_standard_assembly/naughty_blackwell_0.binning \
data/submissions/short_read_pooled_gold_standard_assembly/kraken2.0.8beta_marine.binning \
data/submissions/short_read_pooled_gold_standard_assembly/diamond0.9.28_marine.binning \
data/submissions/short_read_pooled_gold_standard_assembly/megan6.15.2_marine.binning \
--ncbi_dir ../ \
-l "LSHVec cami2,PhyloPythiaS+ 1.4, Kraken 2.0.8 beta, DIAMOND 0.9.28, MEGAN 6.15.2" \
-o data/results/amber_marine_taxonomic/marine_contigs --filter 1
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
-l "LSHVec cami2,PhyloPythiaS+ 1.4, Kraken 2.0.8 beta, DIAMOND 0.9.28, MEGAN 6.15.2" \
-o data/results/amber_marine_taxonomic/marine_deep_branching/${x} --filter 1 \
; done
~~~

