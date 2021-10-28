import pandas as pd

# df = pd.read_csv('../marine_dataset/results/OPAL_short_long_noplasmids/results.tsv', sep='\t')
df = pd.read_csv('../strain_madness_dataset/results/OPAL_short_long/results.tsv', sep='\t')

for x, dfgroup in df.groupby('tool'):
    dfunifrac = dfgroup[dfgroup['metric'] == 'Weighted UniFrac error']
    print("{}\t{:10.2f}".format(x, dfunifrac['value'].median()))

