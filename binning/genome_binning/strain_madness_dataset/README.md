## AMBER command for the binning of the gold standard assembly of the strain madness dataset

~~~BASH
amber.py -g data/ground_truth/gsa_pooled_mapping.binning \
data/short_read_pooled_gold_standard_assembly/sleepy_ptolemy_16.binning \
data/short_read_pooled_gold_standard_assembly/sleepy_ptolemy_17.binning \
data/short_read_pooled_gold_standard_assembly/metabat0.25.4-veryspecific_strain_madness.binning \
data/short_read_pooled_gold_standard_assembly/furious_ardinghelli_0.binning \
data/short_read_pooled_gold_standard_assembly/tender_sammet_0.binning \
data/short_read_pooled_gold_standard_assembly/furious_ardinghelli_17.binning \
data/short_read_pooled_gold_standard_assembly/furious_ardinghelli_7.binning \
data/short_read_pooled_gold_standard_assembly/sad_shockley_0.binning \
data/short_read_pooled_gold_standard_assembly/cranky_wright_0.binning \
data/short_read_pooled_gold_standard_assembly/furious_pare_1.binning \
data/short_read_pooled_gold_standard_assembly/stoic_torvalds_4.binning \
data/short_read_pooled_gold_standard_assembly/sleepy_bohr_0.binning \
data/short_read_pooled_gold_standard_assembly/sleepy_bohr_1.binning \
data/short_read_pooled_gold_standard_assembly/elated_bardeen_1.binning \
data/short_read_pooled_gold_standard_assembly/maxbin2.0.2_strain_madness.binning \
data/short_read_pooled_gold_standard_assembly/sleepy_mclean_2.binning \
data/short_read_pooled_gold_standard_assembly/concoct0.4.1_strain_madness.binning \
data/short_read_pooled_gold_standard_assembly/compassionate_brown_0.binning \
data/short_read_pooled_gold_standard_assembly/modest_tesla_0.binning \
data/short_read_pooled_gold_standard_assembly/elated_bohr_0.binning \
data/short_read_pooled_gold_standard_assembly/drunk_wilson_0.binning \
data/short_read_pooled_gold_standard_assembly/vamb_fa045c0_strain_madness_l2000.binning \
-l "MetaBAT 2.13-33 (A1),MetaBAT 2.13-33 (A2),MetaBAT 0.25.4 (A3),MetaBinner 1.0 (B1),MetaBinner 1.0 (B2),MetaBinner 1.0 (B3),MetaBinner 1.0 (B4),Autometa cami2-03e0d77 (C1),Autometa cami2-03e0d77 (C2),MetaWRAP 1.2.3 (D1),UltraBinner 1.0 (E1),UltraBinner 1.0 (E2),UltraBinner 1.0 (E3),MaxBin 2.2.7 (F1),MaxBin 2.0.2 (F2),CONCOCT 1.1.0 (G1),CONCOCT 0.4.1 (G2),SolidBin 1.3 (H1),SolidBin 1.3 (H2),SolidBin 1.3 (H3),LSHVec cami2 (I1),Vamb fa045c0 (J1)" \
-o results/amber_strain_madness
~~~

## AMBER command for the binning of unique strains

~~~BASH
amber.py -g data/ground_truth/gsa_pooled_mapping.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/sleepy_ptolemy_16.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/sleepy_ptolemy_17.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/metabat0.25.4-veryspecific_strain_madness.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/furious_ardinghelli_0.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/tender_sammet_0.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/furious_ardinghelli_17.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/furious_ardinghelli_7.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/sad_shockley_0.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/cranky_wright_0.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/furious_pare_1.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/stoic_torvalds_4.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/sleepy_bohr_0.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/sleepy_bohr_1.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/elated_bardeen_1.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/maxbin2.0.2_strain_madness.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/sleepy_mclean_2.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/concoct0.4.1_strain_madness.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/compassionate_brown_0.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/modest_tesla_0.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/elated_bohr_0.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/drunk_wilson_0.unique.binning \
data/short_read_pooled_gold_standard_assembly/unique_strains/vamb_fa045c0_strain_madness_l2000.unique.binning \
-l "MetaBAT 2.13-33 (A1),MetaBAT 2.13-33 (A2),MetaBAT 0.25.4 (A3),MetaBinner 1.0 (B1),MetaBinner 1.0 (B2),MetaBinner 1.0 (B3),MetaBinner 1.0 (B4),Autometa cami2-03e0d77 (C1),Autometa cami2-03e0d77 (C2),MetaWRAP 1.2.3 (D1),UltraBinner 1.0 (E1),UltraBinner 1.0 (E2),UltraBinner 1.0 (E3),MaxBin 2.2.7 (F1),MaxBin 2.0.2 (F2),CONCOCT 1.1.0 (G1),CONCOCT 0.4.1 (G2),SolidBin 1.3 (H1),SolidBin 1.3 (H2),SolidBin 1.3 (H3),LSHVec cami2 (I1),Vamb fa045c0 (J1)" \
-o results/amber_strain_madness_unique_strains
~~~

## AMBER command for the binning of common strains

~~~BASH
amber.py -g data/ground_truth/gsa_pooled_mapping.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/sleepy_ptolemy_16.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/sleepy_ptolemy_17.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/metabat0.25.4-veryspecific_strain_madness.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/furious_ardinghelli_0.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/tender_sammet_0.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/furious_ardinghelli_17.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/furious_ardinghelli_7.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/sad_shockley_0.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/cranky_wright_0.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/furious_pare_1.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/stoic_torvalds_4.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/sleepy_bohr_0.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/sleepy_bohr_1.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/elated_bardeen_1.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/maxbin2.0.2_strain_madness.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/sleepy_mclean_2.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/concoct0.4.1_strain_madness.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/compassionate_brown_0.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/modest_tesla_0.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/elated_bohr_0.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/drunk_wilson_0.strains.binning \
data/short_read_pooled_gold_standard_assembly/common_strains/vamb_fa045c0_strain_madness_l2000.strains.binning \
-l "MetaBAT 2.13-33 (A1),MetaBAT 2.13-33 (A2),MetaBAT 0.25.4 (A3),MetaBinner 1.0 (B1),MetaBinner 1.0 (B2),MetaBinner 1.0 (B3),MetaBinner 1.0 (B4),Autometa cami2-03e0d77 (C1),Autometa cami2-03e0d77 (C2),MetaWRAP 1.2.3 (D1),UltraBinner 1.0 (E1),UltraBinner 1.0 (E2),UltraBinner 1.0 (E3),MaxBin 2.2.7 (F1),MaxBin 2.0.2 (F2),CONCOCT 1.1.0 (G1),CONCOCT 0.4.1 (G2),SolidBin 1.3 (H1),SolidBin 1.3 (H2),SolidBin 1.3 (H3),LSHVec cami2 (I1),Vamb fa045c0 (J1)" \
-o results/amber_strain_madness_common_strains
~~~

## AMBER command for the binning of the MEGAHIT assembly

~~~BASH
amber.py -g data/ground_truth/strain_madness_megahit.binning \
data/short_read_pooled_megahit_assembly/metabat0.25.4-veryspecific_strain_madness_megahit.binning \
data/short_read_pooled_megahit_assembly/furious_ardinghelli_2.binning \
data/short_read_pooled_megahit_assembly/furious_ardinghelli_8.binning \
data/short_read_pooled_megahit_assembly/furious_ardinghelli_9.binning \
data/short_read_pooled_megahit_assembly/furious_ardinghelli_2x.binning \
data/short_read_pooled_megahit_assembly/furious_ardinghelli_13.binning \
data/short_read_pooled_megahit_assembly/furious_ardinghelli_15.binning \
data/short_read_pooled_megahit_assembly/furious_ardinghelli_16.binning \
data/short_read_pooled_megahit_assembly/autometa_strain_madness_megahit_l500.binning \
data/short_read_pooled_megahit_assembly/clever_bohr_1.binning \
data/short_read_pooled_megahit_assembly/stoic_torvalds_2.binning \
data/short_read_pooled_megahit_assembly/stoic_torvalds_3.binning \
data/short_read_pooled_megahit_assembly/maxbin2.2.7_strain_madness_megahit.binning \
data/short_read_pooled_megahit_assembly/maxbin2.0.2_strain_madness_megahit.binning \
data/short_read_pooled_megahit_assembly/concoct1.1.0_strain_madness_megahit.binning \
data/short_read_pooled_megahit_assembly/concoct0.4.1_strain_madness_megahit.binning \
data/short_read_pooled_megahit_assembly/naughty_sammet_1.binning \
-l "MetaBAT 0.25.4 (A3),MetaBinner 1.0 (B2),MetaBinner 1.0 (B3),MetaBinner 1.0 (B4),MetaBinner 1.0 (B5),MetaBinner 1.0 (B6),MetaBinner 1.0 (B7),MetaBinner 1.0 (B8),Autometa cami2-146383e (C2),MetaWRAP 1.2.3 (D1),UltraBinner 1.0 (E1),UltraBinner 1.0 (E2),MaxBin 2.2.7 (F1),MaxBin 2.0.2 (F2),CONCOCT 1.1.0 (G1),CONCOCT 0.4.1 (G2),Vamb fa045c0 (J1)" \
-o results/amber_strain_madness_megahit
~~~
