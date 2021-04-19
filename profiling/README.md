## OPAL command for the marine dataset

~~~BASH
opal.py -g ./marine_dataset/data/ground_truth/gs_marine_short.filtered.profile \
-d "2nd CAMI Challenge Marine Dataset, short & long reads, assembly" \
./marine_dataset/data/submissions/assembly_or_averaged/insane_turing_0.profile \
./marine_dataset/data/submissions/assembly_or_averaged/tender_brown_0.profile \
./marine_dataset/data/submissions/short_read_samples/adoring_euclid_5.profile \
./marine_dataset/data/submissions/short_read_samples/angry_brattain_0.profile \
./marine_dataset/data/submissions/short_read_samples/distracted_jones_0.profile \
./marine_dataset/data/submissions/short_read_samples/ecstatic_nobel_0.profile \
./marine_dataset/data/submissions/short_read_samples/ecstatic_nobel_1.profile \
./marine_dataset/data/submissions/short_read_samples/ecstatic_nobel_2.profile \
./marine_dataset/data/submissions/short_read_samples/ecstatic_nobel_3.profile \
./marine_dataset/data/submissions/short_read_samples/ecstatic_nobel_4.profile \
./marine_dataset/data/submissions/short_read_samples/ecstatic_nobel_5.profile \
./marine_dataset/data/submissions/short_read_samples/ecstatic_nobel_6.profile \
./marine_dataset/data/submissions/short_read_samples/ecstatic_nobel_7.profile \
./marine_dataset/data/submissions/short_read_samples/ecstatic_nobel_8.profile \
./marine_dataset/data/submissions/short_read_samples/ecstatic_nobel_9.profile \
./marine_dataset/data/submissions/short_read_samples/insane_turing_0.profile \
./marine_dataset/data/submissions/short_read_samples/mad_yalow_0.profile \
./marine_dataset/data/submissions/short_read_samples/modest_yalow_0.profile \
./marine_dataset/data/submissions/short_read_samples/stoic_mclean_0.profile \
./marine_dataset/data/submissions/long_read_samples/distracted_mestorf_0.profile \
./marine_dataset/data/runtime_evaluated/cami1_tools/marmgCAMI2_short_read_sample_0-9.dudes_cami1.profile \
./marine_dataset/data/runtime_evaluated/cami1_tools/marmgCAMI2_short_read_sample_0-9.focus_cami1.profile \
./marine_dataset/data/runtime_evaluated/cami1_tools/marmgCAMI2_short_read_sample_0-9.metaphlan2_cami1.profile \
./marine_dataset/data/runtime_evaluated/cami1_tools/marmgCAMI2_short_read_sample_0-9.motus_cami1.profile \
./marine_dataset/data/runtime_evaluated/cami1_tools/marmgCAMI2_short_read_sample_0-9.tipp_cami1.profile \
./marine_dataset/data/runtime_evaluated/addition_tools/marmgCAMI2_short_read_sample_0-9.centrifuge_1.0.4_beta.profile \
./marine_dataset/data/runtime_evaluated/addition_tools/marmgCAMI2_short_read_sample_0-9.dudes_0.08.profile \
./marine_dataset/data/runtime_evaluated/addition_tools/marmgCAMI2_short_read_sample_0-9.focus_1.5.profile \
./marine_dataset/data/runtime_evaluated/addition_tools/marmgCAMI2_short_read_sample_0-9.metapalette_1.0.0.profile \
./marine_dataset/data/runtime_evaluated/addition_tools/marmgCAMI2_short_read_sample_0-9.metaphyler_1.25.profile \
./marine_dataset/data/runtime_evaluated/addition_tools/marmgCAMI2_short_read_sample_0-9.tipp_4.3.10.profile \
-l "Metalign 0.6.2 avg,LSHVec gsa,NBC++,Bracken 2.2,mOTUs 2.0.1_1,mOTUs 2.5.1_2,mOTUs 2.5.1_3,mOTUs 2.5.1_4,mOTUs 2.5.1_5,mOTUs 2.5.1_6,mOTUs 2.5.1_7,mOTUs 2.5.1_8,mOTUs 2.5.1_9,mOTUs 2.5.1_10,mOTUs 2.5.1_11,Metalign 0.6.2,MetaPhlAn 2.9.22,CCMetagen 1.1.3,LSHVec illumina,LSHVec pacbio,DUDes cami1,FOCUS cami1,MetaPhlAn cami1,mOTUs cami1,TIPP cami1,Centrifuge 1.0.4 beta,DUDes 0.08,FOCUS 1.5,MetaPalette 1.0.0,MetaPhyler 1.25,TIPP 4.3.10" \
-o ./marine_dataset/results/OPAL_short_long_noplasmids
~~~
Replace last line by the following for normalized and 1%-filtered results:
~~~BASH
-o ./marine_dataset/results/OPAL_short_long_noplasmids_normalized_filtered -n -f 1
~~~

## OPAL command for the strain madness dataset
~~~BASH
opal.py -g ./strain_madness_dataset/data/ground_truth/gs_strain_madness_short_long.profile \
-d "2nd CAMI Challenge Strain Madness Dataset, short & long reads, assembly" \
./strain_madness_dataset/data/submissions/short_read_samples/strmgCAMI2_short_read_sample_0-99.bracken_2.2.profile \
./strain_madness_dataset/data/submissions/assembly_or_averaged/focused_lalande_0.profile \
./strain_madness_dataset/data/submissions/assembly_or_averaged/tender_brown_2.profile \
./strain_madness_dataset/data/submissions/short_read_samples/condescending_cori_0.profile \
./strain_madness_dataset/data/submissions/short_read_samples/ecstatic_nobel_10.profile \
./strain_madness_dataset/data/submissions/short_read_samples/ecstatic_nobel_11.profile \
./strain_madness_dataset/data/submissions/short_read_samples/ecstatic_nobel_12.profile \
./strain_madness_dataset/data/submissions/short_read_samples/ecstatic_nobel_13.profile \
./strain_madness_dataset/data/submissions/short_read_samples/ecstatic_nobel_14.profile \
./strain_madness_dataset/data/submissions/short_read_samples/ecstatic_nobel_15.profile \
./strain_madness_dataset/data/submissions/short_read_samples/ecstatic_nobel_16.profile \
./strain_madness_dataset/data/submissions/short_read_samples/ecstatic_nobel_17.profile \
./strain_madness_dataset/data/submissions/short_read_samples/ecstatic_nobel_18.profile \
./strain_madness_dataset/data/submissions/short_read_samples/ecstatic_nobel_19.profile \
./strain_madness_dataset/data/submissions/short_read_samples/insane_turing_1.strains.profile \
./strain_madness_dataset/data/submissions/short_read_samples/mad_yalow_1.profile \
./strain_madness_dataset/data/submissions/short_read_samples/stoic_mclean_1.profile \
./strain_madness_dataset/data/submissions/long_read_samples/distracted_mestorf_1.profile \
./strain_madness_dataset/data/runtime_evaluated/cami1_tools/strmgCAMI2_short_read_sample_0-99.dudes_cami1.profile \
./strain_madness_dataset/data/runtime_evaluated/cami1_tools/strmgCAMI2_short_read_sample_0-99.focus_cami1.profile \
./strain_madness_dataset/data/runtime_evaluated/cami1_tools/strmgCAMI2_short_read_sample_0-99.metaphlan2_cami1.profile \
./strain_madness_dataset/data/runtime_evaluated/cami1_tools/strmgCAMI2_short_read_sample_0-99.motus_cami1.profile \
./strain_madness_dataset/data/runtime_evaluated/cami1_tools/strmgCAMI2_short_read_sample_0-99.tipp_cami1.profile \
./strain_madness_dataset/data/runtime_evaluated/addition_tools/strmgCAMI2_short_read_sample_0-99.centrifuge_1.0.4_beta.profile \
./strain_madness_dataset/data/runtime_evaluated/addition_tools/strmgCAMI2_short_read_sample_0-99.dudes_0.08.profile \
./strain_madness_dataset/data/runtime_evaluated/addition_tools/strmgCAMI2_short_read_sample_0-99.focus_1.5.profile \
./strain_madness_dataset/data/runtime_evaluated/addition_tools/strmgCAMI2_short_read_sample_0-99.metaphyler_1.25.profile \
./strain_madness_dataset/data/runtime_evaluated/addition_tools/strmgCAMI2_short_read_sample_0-99.tipp_4.3.10.profile \
./strain_madness_dataset/data/runtime_evaluated/reproduce/strmgCAMI2_short_read_sample_0-99.ccmetagen_1.1.3.profile \
-l "Bracken 2.2,LSHVec strain gsa,LSHVec gsa, mOTUs 2.0.1_1,mOTUs 2.5.1_2,mOTUs 2.5.1_3,mOTUs 2.5.1_4,mOTUs 2.5.1_5,mOTUs 2.5.1_6,mOTUs 2.5.1_7,mOTUs 2.5.1_8,mOTUs 2.5.1_9,mOTUs 2.5.1_10,mOTUs 2.5.1_11,Metalign 0.6.2,MetaPhlAn 2.9.22,LSHVec illumina,LSHVec pacbio,DUDes cami1,FOCUS cami1,MetaPhlAn cami1,mOTUs cami1,TIPP cami1,Centrifuge 1.0.4 beta,DUDes 0.08,FOCUS 1.5,MetaPhyler 1.25,TIPP 4.3.10,CCMetagen 1.1.3" \
-o ./strain_madness_dataset/results/OPAL_short_long
~~~
Replace last line by the following for normalized and 1%-filtered results:
~~~BASH
-o ./strain_madness_dataset/results/OPAL_short_long_normalized_filtered -n -f 1
~~~

## OPAL command for the rhizosphere dataset

~~~BASH
opal.py -g ./rhizosphere_dataset/data/ground_truth/gs_rhizosphere.filtered.profile \
-d "2nd CAMI Challenge Rhizosphere Dataset, short & long reads" \
./rhizosphere_dataset/data/submissions/bracken2.6_rhizosphere.profile \
./rhizosphere_dataset/data/submissions/metaphlan2.9.21_rhizosphere.profile \
./rhizosphere_dataset/data/submissions/metaphlan3.0.7_rhizosphere.profile \
./rhizosphere_dataset/data/submissions/motus_cami1_rhizosphere.profile \
./rhizosphere_dataset/data/submissions/motus2.5.1_rhizosphere.profile \
./rhizosphere_dataset/data/submissions/jolly_bartik_0.profile \
./rhizosphere_dataset/data/submissions/jolly_bartik_1.profile \
./rhizosphere_dataset/data/submissions/jolly_bartik_2.profile \
./rhizosphere_dataset/data/submissions/jolly_bartik_3.profile \
./rhizosphere_dataset/data/submissions/jolly_bartik_4.profile \
./rhizosphere_dataset/data/submissions/jolly_bartik_5.profile \
./rhizosphere_dataset/data/submissions/jolly_bartik_6.profile \
./rhizosphere_dataset/data/submissions/jolly_bartik_7.profile \
-l "Bracken 2.6,MetaPhlAn 2.9.21,MetaPhlAn 3.0.7,mOTUs cami1,mOTUs 2.5.1, sourmash gather 3.3.2 k21 (sr),sourmash gather 3.3.2 k31 (sr),sourmash gather 3.3.2 k51 (sr),sourmash gather 3.3.2 k21 (nano),sourmash gather 3.3.2 k31 (nano),sourmash gather 3.3.2 k51 (nano),sourmash gather 3.3.2 k21 (pb),sourmash gather 3.3.2 k31 (pb)" \
-o ./rhizosphere_dataset/results/OPAL_short_long_noplasmids
~~~
Replace last line by the following for normalized and 1%-filtered results:
~~~BASH
-o ./rhizosphere_dataset/results/OPAL_short_long_normalized_filtered -n -f 1
~~~
