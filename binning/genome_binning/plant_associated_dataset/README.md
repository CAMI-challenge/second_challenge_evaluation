## AMBER command for the rhizosphere gsa binning

~~~BASH
amber.py -g data/ground_truth/rhizosphere_short_read_pooled_gsa.binning \
data/short_read_pooled_gold_standard_assembly/distracted_hodgkin_1.binning \
data/short_read_pooled_gold_standard_assembly/focused_poincare_1.binning \
data/short_read_pooled_gold_standard_assembly/focused_poincare_4.binning \
data/short_read_pooled_gold_standard_assembly/focused_poincare_7.binning \
data/short_read_pooled_gold_standard_assembly/boring_fermi_0.binning \
data/short_read_pooled_gold_standard_assembly/modest_leakey_1.binning \
data/short_read_pooled_gold_standard_assembly/furious_mccarthy_0.binning \
data/short_read_pooled_gold_standard_assembly/furious_mccarthy_1.binning \
data/short_read_pooled_gold_standard_assembly/maxbin2.2.7_rhizosphere.binning \
data/short_read_pooled_gold_standard_assembly/concoct1.1.0_rhizosphere.binning \
data/short_read_pooled_gold_standard_assembly/concoct0.4.1_rhizosphere.binning \
data/short_read_pooled_gold_standard_assembly/romantic_poincare_2.binning \
-l "MetaBAT 2.15-5 (A1),MetaBAT 2.15-5 (A2),MetaBAT 2.15-5 (A3),MetaBAT 2.15-5 (A4),MetaBinner 1.0 (B1),MetaBinner 1.2 (B2),MetaBinner 1.3 (B3),MetaBinner 1.3 (B4),MaxBin 2.2.7 (F1),CONCOCT 1.1.0 (G1),CONCOCT 0.4.1 (G2),Vamb 3.0.1 (J1)" \
-r data/ground_truth/plasmids.tsv \
-o results/amber_rhizosphere_noplasmids
~~~

## AMBER command for the rhizosphere hybrid binning

~~~BASH
amber.py -g data/ground_truth/rhizosphere_hybrid_pooled_gsa.binning \
data/hybrid_assembly/distracted_hodgkin_0.binning \
data/hybrid_assembly/focused_poincare_0.binning \
data/hybrid_assembly/focused_poincare_3.binning \
data/hybrid_assembly/focused_poincare_6.binning \
data/hybrid_assembly/jolly_mayer_0.binning \
data/hybrid_assembly/cocky_jones_0.binning \
data/hybrid_assembly/romantic_poincare_4.binning \
-l "MetaBAT 2.15-5 (A1),MetaBAT 2.15-5 (A2),MetaBAT 2.15-5 (A3),MetaBAT 2.15-5 (A4),MetaBinner 1.0 (B1),MetaBinner 1.1 (B2),Vamb 3.0.1 (J1)" \
-r data/ground_truth/plasmids.tsv \
-o results/amber_rhizosphere_hybrid_noplasmids
~~~

## AMBER command for the rhizosphere MEGAHIT binning

~~~BASH
amber.py -g data/ground_truth/rhizosphere_megahit.binning \
data/megahit_assembly/distracted_hodgkin_2.binning \
data/megahit_assembly/focused_poincare_2.binning \
data/megahit_assembly/focused_poincare_5.binning \
data/megahit_assembly/focused_poincare_8.binning \
data/megahit_assembly/boring_fermi_1.binning \
data/megahit_assembly/modest_leakey_0.binning \
data/megahit_assembly/maxbin2.2.7_rhizosphere_megahit.binning \
data/megahit_assembly/concoct1.1.0_rhizosphere_megahit.binning \
data/megahit_assembly/concoct0.4.1_rhizosphere_megahit.binning \
data/megahit_assembly/romantic_poincare_3.binning \
-l "MetaBAT 2.15-5 (A1),MetaBAT 2.15-5 (A2),MetaBAT 2.15-5 (A3),MetaBAT 2.15-5 (A4),MetaBinner 1.0 (B1),MetaBinner 1.2 (B2),MaxBin 2.2.7 (F1),CONCOCT 1.1.0 (G1),CONCOCT 0.4.1 (G2),Vamb 3.0.1 (J1)" \
-r data/ground_truth/plasmids.tsv \
-o results/amber_rhizosphere_megahit_noplasmids
~~~
