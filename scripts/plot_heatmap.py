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



    # levels=pm.create_contour_levels(detect_vector, 2)
    X,Y=pm.project_x_y(map)

    #r=[math.log(distance)/math.log(max) for distance in row]

    #r=[gap/max for gap in row]
    Z = np.clip(mapGrid.matrix, float(args.plot_min), float(args.plot_max))
    # Z= mapGrid.matrix
    X=np.array(X) + 0.5/2.
    Y=np.array(Y) + 0.5/2.
    if not args.plot_min:
        plot_min = np.min(Z)
    else:
        plot_min=float(args.plot_min)
    if not args.plot_max:
        plot_max = np.max(Z)
    else:
        plot_max=float(args.plot_max)

    levels = MaxNLocator(nbins=args.nbins).tick_values(plot_min, plot_max)

    cmap = pm.plot().get_cmap(args.color)
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

    # if pm.type=="detection":
        # cm=pm.plot().pcolormesh(X,Y,Z,zorder=0, vmin=pm.mag_min, vmax=pm.mag_max)
    # else:

    cf = pm.plot().contourf(X, Y, Z, levels=levels, cmap=cmap,
            vmim=plot_min, vmax=plot_max)


        # cm=pm.plot().pcolormesh(X,Y,Z,zorder=0,cmap=cmap,norm=norm)
    pm.plot().colorbar(cf)
    # cs =map.contour(X,Y,Z,levels, colors="k")#,colors="k",zorder=3,linewidths=0.5)

    # #incresing from 10 t0a
    # pm.plot().clabel(cs, inline=1, fontsize=12,fmt='%1.1f')

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
