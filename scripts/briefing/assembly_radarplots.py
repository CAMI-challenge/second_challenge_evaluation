from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
import numpy as np
import seaborn as sns
import math
import itertools


FILES = ['../../assembly/scripts/data/Common_marine.tsv',
         '../../assembly/scripts/data/Unique_marine.tsv',
         '../../assembly/scripts/data/Common_strain_madness.tsv',
         '../../assembly/scripts/data/Unique_strain_madness.tsv']


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
            return lines

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


def get_results():
    assemblers = {}
    metrics = []
    subsets = []
    min_m = {}
    max_m = {}
    for filename in FILES:
        # filename = f.name
        typ = filename.split("/")[-1].split(".")[0]
        subsets.append(typ)
        header = True
        print(filename)
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith("assembler"):
                    metrics = line.strip().split('\t')[1:]
                    metrics = metrics[:-1] # exclude Duplication ratio at pos 3
                    for m in metrics:
                        if m not in min_m:
                            min_m[m] = -1
                            max_m[m] = 0
                    continue
                metrics = ['Genome fraction (%)']
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
    return assemblers, metrics, subsets, min_m


def do_plot(ax, theta):
    assemblers, metrics, subsets, min_m = get_results()

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

    print(len(assemblers.keys()))

    # theta = radar_factory(len(assemblers.keys()), frame='polygon')
    colors = [sns.color_palette('colorblind')[x] for x in [0, 1, 2, 4, 7, 8]]

    metric = 'Genome fraction (%)'
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
    plot_handles = []
    for color, d in zip(colors, vals):
        plot_handles += ax.plot(theta, d, color=color, linewidth=3, dashes=(it,2))
        it += 1
    all_max = max([np.nanmax(np.array(x, dtype=np.float64)) for x in vals])
    all_min = min([np.nanmin(np.array(x, dtype=np.float64)) for x in vals])

    diff = all_max - all_min
    percent = ["Genome fraction (%)", "Strain recall", "Strain precision"]
    if all_max > 0 and all_min >= 0:
        rgrids = (round(math.exp(all_min + diff/3),2),round(math.exp(all_min+2*diff/3),2),round(math.exp(all_max),2))
        if metric in percent:
            rgrids = [int(100*x) for x in rgrids]
        ax.set_rgrids([all_max - 2*all_max/3,all_max-all_max/3,all_max], rgrids, fontsize=18)
    else:
        rgrids = (round(math.exp(all_min + diff/3),2),round(math.exp(all_min+2*diff/3),2),round(math.exp(all_max),2))
        if metric in percent:
            rgrids = [int(100*x) for x in rgrids]
        ax.set_rgrids([all_min + diff/3,all_min+2*diff/3,all_max], rgrids, fontsize=18)
    ax.set_title(metric, size=20, position=(0.5, 1.12), horizontalalignment='center', verticalalignment='center')
    labels = assemblers.keys()
    ax.set_varlabels(labels, fontsize=16)
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]
    for label, angle in zip(ax.get_xticklabels(), angles):
        if angle in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('right')
        else:
            label.set_horizontalalignment('left')

    subsets = [x.replace('_', ' ') for x in subsets]

    def flip(items, ncol):
        return itertools.chain(*[items[i::ncol] for i in range(ncol)])

    leg = ax.legend(flip(plot_handles, 2), flip(subsets, 2), loc='lower left', bbox_to_anchor=(-0.25, -0.35), fontsize=18, ncol=2, frameon=False,
                    handletextpad=0.2, columnspacing=0.5, borderaxespad=0.5, handlelength=1.5)

    for line in leg.get_lines():
        line.set_linewidth(4)
