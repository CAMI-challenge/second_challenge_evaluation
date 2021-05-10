## Scripts for generating the assembly evaluation

1. Running metaQUAST:  
`quast-5.1.0rc1/metaquast.py --reuse-combined-alignments --no-icarus -o ../strmgCAMI2_co_assembly_metaquast-5.1.0rc1 -r cat ../refs -t 28 --unique-mapping ../strmgCAMI2_pooled/GS_*`
2. Create subsets to be differentiated:  
`get_subsets.py metadata.tsv genome_to_id.tsv data/unique.tsv`  
`metadata.tsv` and `genome_to_id.tsv` are from the CAMISIM runs, `unique.tsv` are the genomes with ANI<95% from the dRep `Mdb.csv` table
4. Summarize metrics in table:  
`collect_metrics_assembler.py -dir metaquast/ -o out/ -sf subset_file ...`  
With the metaQUAST main directory, the subsets created in `2` and the desired options (excluding circular elements, suffix, metrics...)  
5. Plot radarplots:  
`create_radarplots_per_metric.py -files all.tsv summary.tsv files.tsv -o out`
