import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib as mpl
import matplotlib.cm as cm
import cmocean
from colormaputil import truncate_colormap


def getMaxBracket(minYear, maxYear, data):
    curMax = 0
    for year in range(minYear, maxYear):
        ranges = data[str(year)]['ranges']
        for num in ranges:
            if num > curMax:
                curMax = num
    return curMax


def getColour(year, i, m, data):
    return m.to_rgba(data[year]['ranges'][i])


maxYear = 2018
minYear = 1985
json_data = open('canada.json').read()
data = json.loads(json_data)
norm = mpl.colors.Normalize(vmin=0, vmax=getMaxBracket(minYear, maxYear, data))
cmap = truncate_colormap(cmocean.cm.phase, 0.35, 1)
m = cm.ScalarMappable(norm=norm, cmap=cmap)
ind = np.arange(maxYear-minYear)
for year in range(minYear, maxYear):
    before = [0] * (year - minYear)
    after = [0] * (maxYear - year-1)
    rates = data[str(year)]['rates']
    previous = 0
    for i in range(len(rates)):
        height = [rates[i]-previous]
        plt.bar(ind, tuple(before + height + after), 1,
                color=getColour(str(year), i, m, data), bottom=previous, linewidth=0)
        previous = rates[i]
m._A = []

small = 9
medium = 11
large = 12

clb = plt.colorbar(m, format='>$%d', ticks=[a for a in range(0, getMaxBracket(minYear, maxYear, data), 10000)])
clb.set_label('Tax Bracket (CAD):', labelpad=-40, y=1.06, rotation=0, fontsize=large)
clb.ax.tick_params(labelsize=medium)
plt.xlim([0, maxYear-minYear])
plt.title('% Personal Income Federally Taxed in Canada, 1985-2017', fontsize=large)
plt.ylabel('% Tax\nApplied', fontsize=large, rotation=0, labelpad=25)
plt.xticks(ind, [a for a in range(minYear, maxYear)], rotation=60, fontsize=small, y=0.01)
plt.yticks(fontsize=medium)
plt.gca().yaxis.grid(which='major', linestyle='-', linewidth=0.8)
plt.gca().xaxis.grid(which='major', linestyle='-', linewidth=0.5)
plt.gca().yaxis.grid(which='minor', linestyle='-', linewidth=0)
plt.gca().xaxis.grid(False, which='minor')
plt.gca().tick_params(axis='x', which='both', length=0)

plt.xlabel("github.com/rosslh/historical-tax-rate-visualizor", fontsize=small, color='#777777')
plt.minorticks_on()
plt.savefig('figure.png', dpi=400)
