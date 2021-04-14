#!/usr/bin/env python

import sys
import argparse
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
import numpy as np
import seaborn as sns
import math

parser = argparse.ArgumentParser()
parser.add_argument("-files", type=argparse.FileType('r'), nargs='+')
# Here we don't need scales and will do the scaling ourselves!
# multiple files, these will get merged via their assemblers
parser.add_argument("-o", type=str, help="out folder")
# one file/plot per metric is created
args = parser.parse_args()

def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels, *args, **kwargs):
            self.set_thetagrids(np.degrees(theta), labels, *args, **kwargs)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta

def create_colors_list():
    colors_list = []
    for color in plt.cm.tab10(np.linspace(0, 1, 10))[:-1]:
        colors_list.append(tuple(color))
    colors_list.append("black")
    for color in plt.cm.Set2(np.linspace(0, 1, 8)):
        colors_list.append(tuple(color))
    for color in plt.cm.Set3(np.linspace(0, 1, 12)):
        colors_list.append(tuple(color))
    return colors_list

assemblers = {}
metrics = []
subsets = []
min_m = {}
max_m = {}
for f in args.files:
    filename = f.name
    typ = f.name.split("/")[-1].split(".")[0]
    subsets.append(typ)
    header = True
    for line in f:
        if line.startswith("assembler"):
            metrics = line.strip().split('\t')[1:]
            metrics = metrics[:-1] # exclude Duplication ratio at pos 3
            for m in metrics:
                if m not in min_m:
                    min_m[m] = -1
                    max_m[m] = 0
            continue
        spl = line.strip().split('\t')
        spl = spl[:-1] # excluding Dup (is 3 here because starts at 0)
        assembler = spl[0]
        if assembler not in assemblers:
            assemblers[assembler] = {}
        i = 1
        for m in metrics:
            if m not in assemblers[assembler]:
                assemblers[assembler][m] = []
            try:
                val = float(spl[i])
            except ValueError:
                val = None
            assemblers[assembler][m].append(val)
            if val is not None:
                if val > max_m[m]:
                    max_m[m] = val
                if (val < min_m[m] or min_m[m] == -1) and val > 0:
                    min_m[m] = val
            i += 1

#small_good = ["Duplication ratio", "# mismatches per 100 kbp", "# contigs", "# misassemblies"]
small_good = ["# mismatches per 100 kbp", "# contigs", "# misassemblies"]
for assembler in assemblers:
    for metric in assemblers[assembler]:
        i = 0
        for value in assemblers[assembler][metric]:
            #if metric in small_good:
            #    if value == 0:
            #        assemblers[assembler][metric][i] = -math.log(min_m[metric]/math.e) 
            #    else:
            #        assemblers[assembler][metric][i] = -math.log(value)
            #else:
            if value is not None:
                if value == 0:
                    assemblers[assembler][metric][i] = math.log(min_m[metric]/math.e)
                else:
                    assemblers[assembler][metric][i] = math.log(value)
            i += 1

#for assembler in assemblers:
#    print(assembler)
#    for metric in assemblers[assembler]:
#        print(metric)
#        print(assemblers[assembler][metric])

theta = radar_factory(len(assemblers.keys()), frame='polygon')
colors = [sns.color_palette('colorblind')[x] for x in [0, 1, 2, 4, 7, 8]]
fig, axes = plt.subplots(figsize=(17, 17), nrows=2, ncols=3, subplot_kw=dict(projection='radar'))
fig.subplots_adjust(wspace=0.2, hspace=0.4, top=0.87, bottom=0.45)
# how can we change the size automatically if more/less metrics are evaluated?
for ax, metric in zip(axes.flat, metrics):
    vals = []
    names = []
    for assembler in assemblers:
        names.append(assembler)
        i = 0
        for v in assemblers[assembler][metric]:
            if i >= len(vals):
                vals.append([v])
            else:
                vals[i].append(v)
            i += 1
    it = 1
    for color, d in zip(colors, vals):
        ax.plot(theta, d, color=color, linewidth=3, dashes=(it,2))
        it += 1
    all_max = max([np.nanmax(np.array(x, dtype=np.float64)) for x in vals])
    all_min = min([np.nanmin(np.array(x, dtype=np.float64)) for x in vals])
    #print(metric)
    #print(all_max)
    #print(all_min)
    diff = all_max - all_min
    percent = ["Genome fraction (%)", "Strain recall", "Strain precision"]
    if (all_max > 0 and all_min >= 0):
        rgrids = (round(math.exp(all_min + diff/3),2),round(math.exp(all_min+2*diff/3),2),round(math.exp(all_max),2))
        if metric in percent:
            rgrids = [int(100*x) for x in rgrids]
        #print(rgrids)
        ax.set_rgrids([all_max - 2*all_max/3,all_max-all_max/3,all_max], rgrids, fontsize=14)
    else:
        rgrids = (round(math.exp(all_min + diff/3),2),round(math.exp(all_min+2*diff/3),2),round(math.exp(all_max),2))
        if metric in percent:
            rgrids = [int(100*x) for x in rgrids]
        #print(rgrids)
        ax.set_rgrids([all_min + diff/3,all_min+2*diff/3,all_max], rgrids, fontsize=14)
    ax.set_title(metric, weight='bold', size=15, position=(0.5, 1.1), horizontalalignment='center', verticalalignment='center')
    labels = assemblers.keys()
    ax.set_varlabels(labels, fontsize=14)
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]
    for label, angle in zip(ax.get_xticklabels(), angles):
        if angle in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('right')
        else:
            label.set_horizontalalignment('left')
    ax = axes[0, 0]
    ax.legend(subsets, loc=(2.0 - 0.353 * len(subsets), 1.25), labelspacing=0.1, fontsize=15, ncol=len(subsets), frameon=False)
plt.savefig(args.o, dpi=150, format='png', bbox_inches='tight')
