'''
    Routine for plotting MagGrid objects using matplotlib
    Use --help for more info and see Jupyter notebook(s) ./notebooks
    For usage examples.
    Outputs a timestamped png file
'''

import sys
import os
import numpy as np
import math
import argparse
from argparse import RawTextHelpFormatter

from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
from magD.pickle import *
from magD.plotMagD import PlotMagD

#file path to pickled grid
#inputs should by min max vals (default scale data)
def main():
    parser = argparse.ArgumentParser(description="A routine to plot",
        formatter_class=RawTextHelpFormatter)
    parser.add_argument('-p','--path',
        help='Path to pickled magGrid file', required=True)
    parser.add_argument('-i','--plot_min', help="min plot value")
    parser.add_argument('-a','--plot_max', help="max plot value")
    parser.add_argument('-t1','--title1', help="title1 of plot", default="Why didn't you add a title?")
    parser.add_argument('-t2','--title2', help="title2 of plot")
    parser.add_argument('-t3','--title3', help="title3 of plot")
    parser.add_argument('-c', '--color', help="Matplotlib Color Pallette", default="Blues")
    parser.add_argument('-n', '--nbins', help="Number of contour bins", default=10)
    parser.add_argument('-d', '--depth', help='Focal Depth', default=0)
    parser.add_argument('-vp', '--velocity_p', help='velocity of P', default=None)
    parser.add_argument('-vs', '--velocity_s', help='Velocity of S', default=None)
    parser.add_argument('-l', '--levels',
        help='Contour levels, use instead of plot_min, plot_max, and nbins',
        default=None)
    args = parser.parse_args()## show values ##
    mapGrid=get_pickle(args.path)
    pm=PlotMagD(mapGrid)


    fig=pm.plot().figure(figsize=(10,12))
    pm.plot().rc("font", size=14)

    bounds=(mapGrid.lat_min, mapGrid.lat_max, mapGrid.lon_min, mapGrid.lon_max)
    map=pm.basemap(bounds)
    map.drawcoastlines(zorder=2)
    map.drawstates(zorder=2)
    map.drawcountries(zorder=2)



    X,Y=pm.project_x_y(map)

    #dirty way to check for blindzone
    #scale matrix in place
    if float(args.depth) > 0.0 and args.velocity_p is not None and args.velocity_s is not None:
        m = mapGrid.matrix
        for r in range(len(m)):
            for c in range(len(m[r])):
                m[r][c]=pm.calc_blindzone(m[r][c],
                    float(args.velocity_p), float(args.velocity_s), float(args.depth))


    if args.levels is not None:
        levels = args.levels.split(',')
        levels = [float(x) for x in levels]
        levels = np.array(levels)
        plot_min=np.min(levels)
        plot_max=np.max(levels)

    else:
        plot_min = float(args.plot_min)
        plot_max = float(args.plot_max)
        levels = MaxNLocator(nbins=args.nbins).tick_values(plot_min, plot_max)
    #Z = np.clip(mapGrid.matrix, plot_min, plot_max)
    Z= mapGrid.matrix
    X=np.array(X) + 0.5/2.
    Y=np.array(Y) + 0.5/2.


    cmap = pm.plot().get_cmap(args.color)

    # norm = BoundaryNorm(levels, ncolors=cmap.N, clip=False)

    # cmap.set_over('b')
    cmap.set_bad('red')

    cf = pm.plot().contourf(X, Y, Z, levels=levels, cmap=cmap,
            vmim=plot_min, vmax=plot_max)



    pm.plot().colorbar(cf)

    meridian_interval=pm.meridian_interval(mapGrid.lon_min, mapGrid.lon_max)
    # #set linewidth to 0  to get only labels
    map.drawmeridians(meridian_interval,labels=[0,0,0,1],
    dashes=[90,8], linewidth=0.0)
    parallel_interval=pm.parallel_interval(mapGrid.lat_min, mapGrid.lat_max)
    map.drawparallels(parallel_interval,labels=[1,0,0,0],
    dashes=[90,8], linewidth=0.0)
    title_arr = [args.title1, args.title2, args.title3]
    title_arr = [x for x in title_arr if x != None]
    title = "\n".join(title_arr)

    pm.plot().title(title)


    fig_name=pm.outfile_with_stamp('./plots/')
    pm.plot().savefig(fig_name)
    pm.plot().show()

if __name__ == "__main__":
    main()
