'''
    Routine for plotting MagGrid objects using matplotlib
    Use --help for more info and see Jupyter notebook(s) ./notebooks
    For usage examples.
    Outputs a timestamped png file
    # pip install -e matplotlib-scalebar
'''
import numpy as np
import argparse
from argparse import RawTextHelpFormatter
from matplotlib.ticker import MaxNLocator
from magD.pickle import get_pickle
import cartopy.crs as ccrs
import cartopy.feature as cf
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


# notes for cartopy
# conda install -c conda-forge cartopy
# uninstall brew geos
# brew uninstall geos

def main():
    parser = argparse.ArgumentParser(description="A routine to plot",
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('-p', '--path', help='Path to pickled magGrid file',
                        required=True)
    parser.add_argument('-i', '--plot_min', help="min plot value")
    parser.add_argument('-a', '--plot_max', help="max plot value")
    parser.add_argument('-t1', '--title1', help="title1 of plot",
                        default="")
    parser.add_argument('-t2', '--title2', help="title2 of plot")
    parser.add_argument('-t3', '--title3', help="title3 of plot")
    parser.add_argument('-c', '--color', help="Matplotlib Color Pallette",
                        default="Blues")
    parser.add_argument('-n', '--nbins', help="Number of contour bins",
                        default=10)
    parser.add_argument('-d', '--depth', help='Focal Depth', default=0)
    parser.add_argument('-vp', '--velocity_p', help='velocity of P',
                        default=None)
    parser.add_argument('-vs', '--velocity_s', help='Velocity of S',
                        default=None)
    parser.add_argument('-l', '--levels', help='Contour levels," \
                        "use instead of plot_min, plot_max, and nbins',
                        default=None)
    parser.add_argument('-pw', '--plotwidth', help='Plot width in inches',
                        default=10)
    parser.add_argument('-ph', '--plotheight', help='Plot height in inches',
                        default=12)
    parser.add_argument('-ps', '--plotstas', help='Plot Stations',
                        default=False)

    parser.add_argument('-lp', '--legend_pad', help='Legend Padding',
                        default=0.0)
    parser.add_argument('-cp', '--colorbar_pad', help='Colorbar Padding',
                        default=0.2)
    parser.add_argument('-cf', '--colorbar_fraction', help='Colorbar fraction',
                        default=0.1)
    parser.add_argument('-lnn', '--lon_min', help='lon_min for plot',
                        required=True)
    parser.add_argument('-lnx', '--lon_max', help='lon_max for plot',
                        required=True)
    parser.add_argument('-ltn', '--lat_min', help='lat_min for plot',
                        required=True)
    parser.add_argument('-ltx', '--lat_max', help='lat_max for plot',
                        required=True)
    parser.add_argument('-u', '--unit', help='unit to display on colorbar')
    args = parser.parse_args()

    MagD = get_pickle(args.path)

    plt.figure(figsize=(int(args.plotwidth), int(args.plotheight)))
    bounds = [float(args.lon_min), float(args.lon_max),
              float(args.lat_min), float(args.lat_max)]
    ax = plt.axes(projection=ccrs.Mercator())
    ax.set_extent(bounds)
    ax.add_feature(cf.STATES.with_scale('10m'))
    ax.add_feature(cf.BORDERS.with_scale('10m'))

    # grid lines and ticks
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=0)
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlabel_style = {'size': 12}
    gl.ylabel_style = {'size': 12}

    # only plot every 4th starting 1 in from the ends
    xlabel_steps = range(int(MagD.lon_list()[1]),
                         int(MagD.lon_list()[-2]))[::4]

    ylabel_steps = range(int(MagD.lat_list()[1]),
                         int(MagD.lat_list()[-2]))[::4]
    gl.xlocator = mticker.FixedLocator(xlabel_steps)
    gl.ylocator = mticker.FixedLocator(ylabel_steps)

    # plot station markers
    solutions = MagD.firstn_solutions
    unit = args.unit
    if args.plotstas:
        if len(solutions) > 0:
            s_lats = [s.obj.lat for s in solutions]
            s_lons = [s.obj.lon for s in solutions]
            ax.scatter(s_lons, s_lats, s=60, marker='D', c="k",
                       label="Contributing stations", zorder=12,
                       transform=ccrs.Geodetic())
        for key in MagD.markers:
            lats = [dest.lat for dest in MagD.markers[key]['collection']]
            lons = [dest.lon for dest in MagD.markers[key]['collection']]
            # find index of list where stations did not contrib to any
            # solution (looosers)
            # Sx, Sy = map(lons, lats)
            color = MagD.markers[key]['color']
            symbol = MagD.markers[key]['symbol']
            label = MagD.markers[key]['label']
            size = int(MagD.markers[key]['size'])
            # print(MagD.markers[key])
            # once set we don't want to unset units
            if 'unit' in MagD.markers[key] and unit is None:
                unit = MagD.markers[key]['unit']
            ax.scatter(lons, lats, s=size, marker=symbol, c=color,
                       label=label, zorder=11, transform=ccrs.Geodetic())

            bbox = (0.0, float(args.legend_pad))
            plt.legend(bbox_to_anchor=bbox, loc=3, borderaxespad=0.,
                       scatterpoints=1, fontsize=15)
    # contours
    if args.levels is not None:
        levels = args.levels.split(',')
        levels = [float(x) for x in levels]
        levels = np.array(levels)
        plot_min = np.min(levels)
        plot_max = np.max(levels)

        X, Y = np.meshgrid(MagD.lon_list(), MagD.lat_list())
        Z = MagD.matrix
        X = np.array(X)
        Y = np.array(Y)
        cmap = plt.get_cmap(args.color)
        clf = ax.contourf(X, Y, Z, levels=levels, cmap=cmap, vmim=plot_min,
                          vmax=plot_max, transform=ccrs.PlateCarree())
        # colorbar
        clb = plt.colorbar(clf, fraction=float(args.colorbar_fraction),
                           pad=float(args.colorbar_pad))
        if unit is not None:
            clb.ax.set_title(unit, fontsize=12)
            clb.ax.set_yticklabels(clb.ax.get_yticklabels(), fontsize=12)

    title_arr = [args.title1, args.title2, args.title3]
    title_arr = [x for x in title_arr if x is not None]
    title = "\n".join(title_arr)
    plt.title(title, fontsize=20)
    plt.show()

if __name__ == "__main__":
    main()
