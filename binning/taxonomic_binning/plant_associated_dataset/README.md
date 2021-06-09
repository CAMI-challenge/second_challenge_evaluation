## AMBER command for the binning of the gold standard assembly of the plant-associated dataset

~~~BASH
amber.py -g ../../genome_binning/plant_associated_dataset/data/ground_truth/rhizosphere_short_read_pooled_gsa.binning \
data/submissions/short_read_pooled_gold_standard_assembly/kraken2.0.8beta_rhizosphere.binning \
data/submissions/short_read_pooled_gold_standard_assembly/kraken0.10.5-beta_rhizosphere.binning \
data/submissions/short_read_pooled_gold_standard_assembly/ppsp1.4_rhizosphere.binning \
data/submissions/short_read_pooled_gold_standard_assembly/diamond_rhizosphere.binning \
data/submissions/short_read_pooled_gold_standard_assembly/megan6.15.2_rhizosphere.binning \
--ncbi_dir ../ \
-l "Kraken 2.0.8 beta, Kraken 0.10.5-beta, PhyloPythiaS+ 1.4, DIAMOND 0.9.28, MEGAN 6.15.2" \
-o data/results/amber_rhizosphere_taxonomic/rhizosphere_contigs --filter 1
~~~
