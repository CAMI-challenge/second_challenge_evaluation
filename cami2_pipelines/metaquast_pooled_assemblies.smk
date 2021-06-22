import pandas as pd
from io import BytesIO
import requests

include: "share/load_config.smk"

sheet_id = '1JTRjus4h5waYqynr1aCOr78ZJVQqEwAx6om6650TqNk'
r = requests.get('https://docs.google.com/spreadsheet/ccc?key={0}&output=csv'.format(sheet_id))
df = pd.read_csv(BytesIO(r.content), index_col=0)

df_filtered = df.loc[(df.Dataset=='Marine')&(df.Assembly_type=='pooled'),:]

base_dir = '/net/sgi/metagenomics/cami2_benchmark/submissions/assembly/results'

labels = ','.join(df_filtered.Assembly_name + "_" + df_filtered.Assembler_type) #','.join(df_filtered.Assembly_name)
assemblies = ' '.join((df_filtered.File_location).str.replace('/swift/v1/CAMI_UPLOAD/users', base_dir))

pooled_short_gsa = '/net/sgi/cami/data/CAMI2/nwillassen_data/marine/simulation_short_read//anonymous_gsa_pooled.fasta.gz'
pooled_long_gsa = '/net/sgi/cami/data/CAMI2/nwillassen_data/marine/simulation_long_read//anonymous_gsa_pooled.fasta.gz'
pooled_hybrid_gsa = '/net/sgi/cami/data/CAMI2/nwillassen_data/marine/simulation_hybrid//pooled/anonymous_gsa.fasta.gz'


ref_genomes = '/net/sgi/cami/data/CAMI2/nwillassen_data/marine/marmgCAMI2/simulation/simulation_short_read/genomes'
gs_genomes = '/net/sgi/metagenomics/cami2_benchmark/datasets/marine/gsa/genomes'

reference_names = ['ref_genomes']#, 'gs_genomes']
identity_params = ['95', '98', '99', '99.5']


rule all:
    input:
        metaquast = expand(
            results_dir + '/metaquast_marine_pooled_abyss_k32_vs_{reference}_uniq_map_min_identity{identity}/report.html',
            reference=reference_names,
            identity=identity_params)
        

rule metaquast:
    input:
        
    output:
        out = results_dir + '/metaquast_marine_pooled_abyss_k32_vs_{reference}_uniq_map_min_identity{identity}/report.html'
    benchmark:
        reports_dir + '/benchmarks/metaquast_marine_pooled_abyss_k32_vs_{reference}_uniq_map_min_identity{identity}.benchmark.txt'
    params:
        bin = '/net/sgi/metagenomics/cami2_benchmark/pipelines/lib/quast-5.1.0rc1/metaquast.py',
        assemblies = assemblies,
        labels = labels,

        reference = lambda wc: ref_genomes if wc.reference == 'ref_genomes' else gs_genomes,
        identity = lambda wc: '--min-identity ' + wc.identity,
        out_dir = results_dir + '/metaquast_marine_pooled_abyss_k32_vs_{reference}_uniq_map_min_identity{identity}'
    threads: 10
    shell:
        """
        {params.bin} --reuse-combined-alignments --no-icarus -t {threads} {params.identity} -o {params.out_dir} \
            -r {params.reference} {params.assemblies} -l {params.labels} --unique-mapping
        """

rule metaquast_frag:
    input:
        
    output:
        out = results_dir + '/metaquast_marine_pooled_assembles_vs_{reference}_uniq_map_min_identity{identity}_fragmented/report.html'
    benchmark:
        reports_dir + '/benchmarks/metaquast_marine_pooled_assembles_vs_{reference}_uniq_map_min_identity{identity}_fragmented.benchmark.txt'
    params:
        bin = '/net/sgi/metagenomics/cami2_benchmark/pipelines/lib/quast-5.1.0rc1/metaquast.py',
        assemblies = assemblies,
        labels = labels,

        reference = lambda wc: ref_genomes if wc.reference == 'ref_genomes' else gs_genomes,
        identity = lambda wc: '--min-identity ' + wc.identity,
        out_dir = results_dir + '/metaquast_marine_pooled_assembles_vs_{reference}_uniq_map_min_identity{identity}_fragmented'
    threads: 16
    shell:
        """
        {params.bin} --reuse-combined-alignments --no-icarus -t {threads} {params.identity} -o {params.out_dir} \
            -r {params.reference} {params.assemblies} -l {params.labels} --unique-mapping --no-plots --no-html \
            --no-html --fragmented
        """