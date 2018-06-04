import sys
import os
import numpy as np
import math
import argparse

from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
from magD.pickle import *
from magD.plotMagD import PlotMagD

#file path to pickled grid
#inputs should by min max vals (default scale data)
def main():
    parser = argparse.ArgumentParser(description="A routine to plot")
    parser.add_argument('-p','--path',
        help='Path to pickled magGrid file', required=True)
    parser.add_argument('-i','--plot_min', help="min plot value")
    parser.add_argument('-a','--plot_max', help="max plot value")
    parser.add_argument('-t','--title', help="title of plot")
    parser.add_argument('-d','--description', help="Description of plot (2nd line)")
    parser.add_argument('-c', '--color', help="Matplotlib Color Pallette", default="Blues")

    args = parser.parse_args()## show values ##
    mapGrid=get_pickle(args.path)
    plot_title = args.title
    if not plot_title:
        plot_title = mapGrid.type
    plot_desc = args.description
    if not plot_desc:
        plot_desc = mapGrid.name
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
    Z=mapGrid.matrix
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

    levels = MaxNLocator(nbins=10).tick_values(plot_min, plot_max)
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

    # # #zorder puts it at lowest plot level
    # map.fillcontinents(color='0.95',zorder=1)
    # header=""
    # if type=="detection":
    #     header="Minimum Magnitude Detection"
    # elif type=="gap":
    #     header="Largest Azimuthal Gap"
    # else:
    #     header="Distance to closest station"
    #
    pm.plot().title(
        "{}\n{}\n {} station detection {} deg. grid".format(
        plot_title, plot_desc, mapGrid.num_detections, mapGrid.resolution))
    # # #should we add no solution symbol to legend?
    # # no_solution=False
    # #iterate through sets and assign color
    #
    # # for key in mapGrid.scnl_collections():
    # #   #plot station data
    # #   lats, lons, sols=mapGrid.get_xyz_lists(key)
    # #   #find index of list where stations did not contrib to any solution (looosers)
    # #   no_i=mapGrid.get_no_solution_index(key)
    # #
    # #
    # #   if no_i < len(lons)-1:
    # #       no_solution=True
    # #   #contributed to solution
    # #   Sx,Sy=map(lons[:no_i], lats[:no_i])
    # #   #did not contrib to solution
    # #   Sxn,Syn=map(lons[no_i:], lats[no_i:])
    # #
    # #   color,label=pm.plot_color_label(key)
    # #   stas=pm.plot().scatter(Sx, Sy, s=70, marker='^', c=color, label=label,zorder=11)
    # #   #plot no solutions but don't create a legend entry for each
    # #   pm.plot().scatter(Sxn, Syn, s=30, marker='o', facecolors='none', edgecolors=color,zorder=11)
    #
    # # #create legend for no solutions
    # # if no_solution:
    # #   pm.plot().scatter([-1],[-1], s=30, marker='o',facecolors='none',edgecolor='k',label="No solution")
    # #bbox coords= x,y,width,height
    # # bbox=(0.0,-0.2)
    # # pm.plot().legend(bbox_to_anchor=bbox, loc=3, borderaxespad=0.,scatterpoints=1)

    fig_name=pm.outfile_with_stamp('./plots/')
    pm.plot().savefig(fig_name)
    pm.plot().show()

if __name__ == "__main__":
    main()
