import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import assembly_radarplots
import genome_b_boxplots
import runtime
import profiling_scatter
import tax_b


fig = plt.figure(figsize=(23, 15))
outer = gridspec.GridSpec(2, 11, wspace=4, hspace=0.3)

inner = gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=outer[0, 0:3])
theta = assembly_radarplots.radar_factory(9, frame='polygon')
ax = fig.add_subplot(inner[0], projection='radar')
assembly_radarplots.do_plot(ax, theta)
ax.set_ylabel('a', rotation='0', weight='bold', fontsize=24)
ax.yaxis.set_label_coords(-0.15, 1.125)

inner = gridspec.GridSpecFromSubplotSpec(2, 2, subplot_spec=outer[0, 4:8], wspace=0.35, hspace=0.22)
ax0 = fig.add_subplot(inner[0])
ax1 = fig.add_subplot(inner[1])
ax2 = fig.add_subplot(inner[2])
ax3 = fig.add_subplot(inner[3])
ax = np.array([[ax0, ax1], [ax2, ax3]])
genome_b_boxplots.main(ax)

inner = gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=outer[0:, 9:])
ax = fig.add_subplot(inner[0])
runtime.doit(*runtime.format_pd(pd.read_csv(runtime.FILE, sep=',').fillna(''), 'Runtime (hours)'), ax)
ax.set_ylabel('e', rotation='0', weight='bold', fontsize=24)
ax.yaxis.set_label_coords(-0.8, 0.99)


inner = gridspec.GridSpecFromSubplotSpec(2, 2, subplot_spec=outer[1, 0:4], wspace=0.1, hspace=0.2)
ax0 = fig.add_subplot(inner[0])
ax1 = fig.add_subplot(inner[1])
ax2 = fig.add_subplot(inner[2])
ax3 = fig.add_subplot(inner[3])
ax = np.array([[ax0, ax1], [ax2, ax3]])
tax_b.main('mar', ax)
ax0.set_ylabel('c', rotation='0', weight='bold', fontsize=24)
ax0.yaxis.set_label_coords(-0.22, 1.07)

inner = gridspec.GridSpecFromSubplotSpec(1, 1, subplot_spec=outer[1, 4:8])
ax = fig.add_subplot(inner[0])
profiling_scatter.main(ax)
ax.annotate('d', xy=(-20, 1.044), fontsize=24, weight='bold', xycoords=ax.get_xaxis_transform())

fig.savefig('briefing.pdf', dpi=100, format='pdf', bbox_inches='tight')
