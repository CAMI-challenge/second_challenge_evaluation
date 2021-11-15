#!/usr/bin/env python

from matplotlib_venn import venn3, venn3_circles
from matplotlib import pyplot as plt

venn3(subsets = (2,7,4,19,0,5,37), set_labels = ('Finder', 'CRT', 'ML'), alpha = 0.5)
plt.savefig("CRISPR_venn.png")
