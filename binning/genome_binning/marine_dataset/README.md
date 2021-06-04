## AMBER command for the binning of the gold standard assembly of the marine dataset

~~~BASH
amber.py -g data/ground_truth/gsa_pooled_mapping_short.binning \
data/submissions/short_read_pooled_gold_standard_assembly/sleepy_ptolemy_4.binning \
data/submissions/short_read_pooled_gold_standard_assembly/sleepy_ptolemy_4x.binning \
data/submissions/short_read_pooled_gold_standard_assembly/metabat0.25.4-veryspecific_marine.binning \
data/submissions/short_read_pooled_gold_standard_assembly/furious_ardinghelli_12.binning \
data/submissions/short_read_pooled_gold_standard_assembly/furious_ardinghelli_3.binning \
data/submissions/short_read_pooled_gold_standard_assembly/furious_ardinghelli_18.binning \
data/submissions/short_read_pooled_gold_standard_assembly/sharp_bardeen_0.binning \
data/submissions/short_read_pooled_gold_standard_assembly/grave_torvalds_1.binning \
data/submissions/short_read_pooled_gold_standard_assembly/furious_pare_0.binning \
data/submissions/short_read_pooled_gold_standard_assembly/pensive_sinoussi_0.binning \
data/submissions/short_read_pooled_gold_standard_assembly/elated_bardeen_0.binning \
data/submissions/short_read_pooled_gold_standard_assembly/maxbin2.0.2_marine.binning \
data/submissions/short_read_pooled_gold_standard_assembly/concoct1.1.0_marine.binning \
data/submissions/short_read_pooled_gold_standard_assembly/concoct0.4.1_marine.binning \
data/submissions/short_read_pooled_gold_standard_assembly/vamb_fa045c0_marine_l2000.binning \
-l "MetaBAT 2.13-33 (A1),MetaBAT 2.13-33 (A2),MetaBAT 0.25.4 (A3),MetaBinner 1.0 (B1),MetaBinner 1.0 (B2),MetaBinner 1.0 (B3),Autometa cami2-146383e (C1),Autometa cami2-146383e (C2),MetaWRAP 1.2.3 (D1),UltraBinner 1.0 (E1),MaxBin 2.2.7 (F1),MaxBin 2.0.2 (F2),CONCOCT 1.1.0 (G1),CONCOCT 0.4.1 (G2),Vamb fa045c0 (J1)" \
-r data/marine_genome_cat.tsv -k "circular element" \
-o results/amber_marine_nocircular/
~~~

## AMBER command for the binning of unique strains

~~~BASH
amber.py -g data/ground_truth/gsa_pooled_mapping_short.unique.binning \
data/submissions/short_read_pooled_gold_standard_assembly/unique_strains/sleepy_ptolemy_4.unique.binning \
data/submissions/short_read_pooled_gold_standard_assembly/unique_strains/sleepy_ptolemy_4x.unique.binning \
data/submissions/short_read_pooled_gold_standard_assembly/unique_strains/metabat0.25.4-veryspecific_marine.unique.binning \
data/submissions/short_read_pooled_gold_standard_assembly/unique_strains/furious_ardinghelli_12.unique.binning \
data/submissions/short_read_pooled_gold_standard_assembly/unique_strains/furious_ardinghelli_3.unique.binning \
data/submissions/short_read_pooled_gold_standard_assembly/unique_strains/furious_ardinghelli_18.unique.binning \
data/submissions/short_read_pooled_gold_standard_assembly/unique_strains/sharp_bardeen_0.unique.binning \
data/submissions/short_read_pooled_gold_standard_assembly/unique_strains/grave_torvalds_1.unique.binning \
data/submissions/short_read_pooled_gold_standard_assembly/unique_strains/furious_pare_0.unique.binning \
data/submissions/short_read_pooled_gold_standard_assembly/unique_strains/pensive_sinoussi_0.unique.binning \
data/submissions/short_read_pooled_gold_standard_assembly/unique_strains/elated_bardeen_0.unique.binning \
data/submissions/short_read_pooled_gold_standard_assembly/unique_strains/maxbin2.0.2_marine.unique.binning \
data/submissions/short_read_pooled_gold_standard_assembly/unique_strains/concoct1.1.0_marine.unique.binning \
data/submissions/short_read_pooled_gold_standard_assembly/unique_strains/concoct0.4.1_marine.unique.binning \
data/submissions/short_read_pooled_gold_standard_assembly/unique_strains/vamb_fa045c0_marine_l2000.unique.binning \
-l "MetaBAT 2.13-33 (A1),MetaBAT 2.13-33 (A2),MetaBAT 0.25.4 (A3),MetaBinner 1.0 (B1),MetaBinner 1.0 (B2),MetaBinner 1.0 (B3),Autometa cami2-146383e (C1),Autometa cami2-146383e (C2),MetaWRAP 1.2.3 (D1),UltraBinner 1.0 (E1),MaxBin 2.2.7 (F1),MaxBin 2.0.2 (F2),CONCOCT 1.1.0 (G1),CONCOCT 0.4.1 (G2),Vamb fa045c0 (J1)" \
-r data/marine_genome_cat.tsv -k "circular element" \
-o results/amber_marine_unique_strains_nocircular
~~~

## AMBER command for the binning of common strains

~~~BASH
amber.py -g data/ground_truth/gsa_pooled_mapping_short.strains.binning \
data/submissions/short_read_pooled_gold_standard_assembly/common_strains/sleepy_ptolemy_4.strains.binning \
data/submissions/short_read_pooled_gold_standard_assembly/common_strains/sleepy_ptolemy_4x.strains.binning \
data/submissions/short_read_pooled_gold_standard_assembly/common_strains/metabat0.25.4-veryspecific_marine.strains.binning \
data/submissions/short_read_pooled_gold_standard_assembly/common_strains/furious_ardinghelli_12.strains.binning \
data/submissions/short_read_pooled_gold_standard_assembly/common_strains/furious_ardinghelli_3.strains.binning \
data/submissions/short_read_pooled_gold_standard_assembly/common_strains/furious_ardinghelli_18.strains.binning \
data/submissions/short_read_pooled_gold_standard_assembly/common_strains/sharp_bardeen_0.strains.binning \
data/submissions/short_read_pooled_gold_standard_assembly/common_strains/grave_torvalds_1.strains.binning \
data/submissions/short_read_pooled_gold_standard_assembly/common_strains/furious_pare_0.strains.binning \
data/submissions/short_read_pooled_gold_standard_assembly/common_strains/pensive_sinoussi_0.strains.binning \
data/submissions/short_read_pooled_gold_standard_assembly/common_strains/elated_bardeen_0.strains.binning \
data/submissions/short_read_pooled_gold_standard_assembly/common_strains/maxbin2.0.2_marine.strains.binning \
data/submissions/short_read_pooled_gold_standard_assembly/common_strains/concoct1.1.0_marine.strains.binning \
data/submissions/short_read_pooled_gold_standard_assembly/common_strains/concoct0.4.1_marine.strains.binning \
data/submissions/short_read_pooled_gold_standard_assembly/common_strains/vamb_fa045c0_marine_l2000.strains.binning \
-l "MetaBAT 2.13-33 (A1),MetaBAT 2.13-33 (A2),MetaBAT 0.25.4 (A3),MetaBinner 1.0 (B1),MetaBinner 1.0 (B2),MetaBinner 1.0 (B3),Autometa cami2-146383e (C1),Autometa cami2-146383e (C2),MetaWRAP 1.2.3 (D1),UltraBinner 1.0 (E1),MaxBin 2.2.7 (F1),MaxBin 2.0.2 (F2),CONCOCT 1.1.0 (G1),CONCOCT 0.4.1 (G2),Vamb fa045c0 (J1)" \
-r data/marine_genome_cat.tsv -k "circular element" \
-o results/amber_marine_common_strains_nocircular
~~~

## AMBER command for the binning of the MEGAHIT assembly

~~~BASH
amber.py -g data/ground_truth/marine_megahit.binning \
data/submissions/short_read_pooled_megahit_assembly/sleepy_ptolemy_10.binning \
data/submissions/short_read_pooled_megahit_assembly/sleepy_ptolemy_11.binning \
data/submissions/short_read_pooled_megahit_assembly/metabat0.25.4-veryspecific_marine_megahit.binning \
data/submissions/short_read_pooled_megahit_assembly/furious_ardinghelli_4.binning \
data/submissions/short_read_pooled_megahit_assembly/furious_ardinghelli_5.binning \
data/submissions/short_read_pooled_megahit_assembly/furious_ardinghelli_11.binning \
data/submissions/short_read_pooled_megahit_assembly/furious_ardinghelli_6.binning \
data/submissions/short_read_pooled_megahit_assembly/furious_ardinghelli_14.binning \
data/submissions/short_read_pooled_megahit_assembly/furious_ardinghelli_19.binning \
data/submissions/short_read_pooled_megahit_assembly/furious_ardinghelli_10.binning \
data/submissions/short_read_pooled_megahit_assembly/autometa_marine_megahit_l2000.binning \
data/submissions/short_read_pooled_megahit_assembly/clever_bohr_0.binning \
data/submissions/short_read_pooled_megahit_assembly/stoic_torvalds_0.binning \
data/submissions/short_read_pooled_megahit_assembly/stoic_torvalds_1.binning \
data/submissions/short_read_pooled_megahit_assembly/maxbin2.2.7_marine_megahit.binning \
data/submissions/short_read_pooled_megahit_assembly/maxbin2.0.2_marine_megahit.binning \
data/submissions/short_read_pooled_megahit_assembly/concoct1.1.0_marine_megahit.binning \
data/submissions/short_read_pooled_megahit_assembly/concoct0.4.1_marine_megahit.binning \
data/submissions/short_read_pooled_megahit_assembly/naughty_sammet_0.binning \
-l "MetaBAT 2.13-33 (A1),MetaBAT 2.13-33 (A2),MetaBAT 0.25.4 (A3),MetaBinner 1.0 (B2),MetaBinner 1.0 (B3),MetaBinner 1.0 (B4),MetaBinner 1.0 (B5),MetaBinner 1.0 (B7),MetaBinner 1.0 (B8),MetaBinner 1.0 (B9),Autometa cami2-146383e (C2),MetaWRAP 1.2.3 (D1),UltraBinner 1.0 (E1),UltraBinner 1.0 (E2),MaxBin 2.2.7 (F1),MaxBin 2.0.2 (F2),CONCOCT 1.1.0 (G1),CONCOCT 0.4.1 (G2),Vamb fa045c0 (J1)" \
-r data/marine_genome_cat.tsv -k "circular element" \
-o results/amber_marine_megahit_nocircular
~~~
