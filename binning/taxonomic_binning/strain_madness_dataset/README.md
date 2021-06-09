## AMBER command for the binning of the gold standard assembly of the strain madness dataset

~~~BASH
~/tmp/AMBER/amber.py -g ../../genome_binning/strain_madness_dataset/data/ground_truth/gsa_pooled_mapping.binning \
data/submissions/short_read_pooled_gold_standard_assembly/hopeful_kirch_3.binning \
data/submissions/short_read_pooled_gold_standard_assembly/ppsp1.4_strain_madness.binning \
data/submissions/short_read_pooled_gold_standard_assembly/kraken2.0.8beta_strain_madness.binning \
data/submissions/short_read_pooled_gold_standard_assembly/diamond0.9.28_strain_madness.binning \
data/submissions/short_read_pooled_gold_standard_assembly/megan6.15.2_strain_madness.binning \
--ncbi_dir ../ \
-l "LSHVec cami2,PhyloPythiaS+ 1.4, Kraken 2.0.8 beta, DIAMOND 0.9.28,MEGAN" \
-o data/results/strain_madness_contigs --filter 1
~~~

## AMBER command for the binning of the gold standard assembly of the strain madness dataset ((by novelty category))

~~~BASH
myvars=("new_genus" "new_order" "new_species" "new_strain"); \
for x in "${myvars[@]}"; do \
~/tmp/AMBER/amber.py -g data/ground_truth/gsa_pooled_mapping.${x}.binning \
data/submissions/short_read_pooled_gold_standard_assembly/hopeful_kirch_3.${x}.binning \
data/submissions/short_read_pooled_gold_standard_assembly/ppsp1.4_strain_madness.${x}.binning \
data/submissions/short_read_pooled_gold_standard_assembly/kraken2.0.8beta_strain_madness.${x}.binning \
data/submissions/short_read_pooled_gold_standard_assembly/diamond0.9.28_strain_madness.${x}.binning \
data/submissions/short_read_pooled_gold_standard_assembly/megan6.15.2_strain_madness.${x}.binning \
--ncbi_dir ../ \
-l "LSHVec cami2,PhyloPythiaS+ 1.4, Kraken 2.0.8 beta, DIAMOND 0.9.28,MEGAN" \
-o data/results/strain_madness_deep_branching/${x} --filter 1 \
; done
~~~
