import pandas as pd
from io import BytesIO
import requests

include: "share/load_config.smk"

sheet_id = '1JTRjus4h5waYqynr1aCOr78ZJVQqEwAx6om6650TqNk'
r = requests.get('https://docs.google.com/spreadsheet/ccc?key={0}&output=csv'.format(sheet_id))
df = pd.read_csv(BytesIO(r.content), index_col=0)

df_filtered = df.loc[(df.Dataset=='Marine')&(df.Assembly_type=='single')&(df.Run_single_sample=='Run 0'),:]

base_dir = '/net/sgi/metagenomics/cami2_benchmark/submissions/assembly/results'

labels = ','.join(df_filtered.Assembly_name + "_" + df_filtered.Assembler_type) #','.join(df_filtered.Assembly_name)
assemblies = ' '.join((df_filtered.File_location).str.replace('/swift/v1/CAMI_UPLOAD/users', base_dir))


#ref_genomes = '/net/sgi/cami/data/CAMI2/nwillassen_data/marine/marmgCAMI2/simulation/simulation_short_read/genomes'
#gs_genomes = '/net/sgi/metagenomics/cami2_benchmark/datasets/marine/gsa/genomes'
abundance = '/net/sgi/cami/data/CAMI2/nwillassen_data/marine/simulation_short_read/abundance0.tsv'
otu_genome_map = '/net/sgi/cami/data/CAMI2/nwillassen_data/marine/simulation_short_read/genome_to_id.tsv'
reference_names = ['ref_genomes']#, 'gs_genomes']
identity_params = ['95', '98', '99', '99.5']

otu_abd_df = pd.read_csv(abundance, index_col=0, header=None, names=['abundance'], sep='\t')
otu_genome_df = pd.read_csv(otu_genome_map, index_col=0, header=None, names=['genome'], sep='\t')

sample0_nonzero_genomes = otu_genome_df.loc[otu_abd_df.loc[otu_abd_df.abundance >0].index, 'genome'].tolist()
print(len(sample0_nonzero_genomes), 'genomes')
ref_genomes = ','.join(sample0_nonzero_genomes)

sample0_short_gsa = '/net/sgi/cami/data/CAMI2/nwillassen_data/marine/simulation_short_read/2018.08.15_09.49.32_sample_0/contigs/anonymous_gsa.fasta.gz'
sample0_long_gsa = '/net/sgi/cami/data/CAMI2/nwillassen_data/marine/simulation_long_read/2018.08.08_16.35.17_sample_0/contigs/anonymous_gsa.fasta.gz'
sample0_hybrid_gsa = '/net/sgi/cami/data/CAMI2/nwillassen_data/marine/simulation_hybrid/sample_0/anonymous_gsa.fasta.gz'



rule all:
    input:
        metaquast = expand(
            results_dir + '/metaquast_marine_sample0_assembles_vs_{reference}_uniq_map_min_identity{identity}/report.html',
            reference=reference_names,
            identity=identity_params)
        
rule metaquast:
    input:
        
    output:
        out = results_dir + '/metaquast_marine_sample0_assembles_vs_{reference}_uniq_map_min_identity{identity}/report.html'
    benchmark:
        reports_dir + '/benchmarks/metaquast_marine_sample0_assembles_vs_{reference}_uniq_map_min_identity{identity}.benchmark.txt'
    params:
        bin = 'lib/quast-5.1.0rc1/metaquast.py',
        assemblies = assemblies,
        labels = labels,

        reference = lambda wc: ref_genomes if wc.reference == 'ref_genomes' else gs_genomes,
        identity = lambda wc: '--min-identity ' + wc.identity,
        out_dir = results_dir + '/metaquast_marine_sample0_assembles_vs_{reference}_uniq_map_min_identity{identity}'
    threads: 8
    shell:
        """
        {params.bin} --reuse-combined-alignments --no-icarus -t {threads} {params.identity} -o {params.out_dir} \
            -r {params.reference} {params.assemblies} -l {params.labels} --unique-mapping
        """