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
from magD.plotMagD import PlotMagD


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
    args = parser.parse_args()
    MagD = get_pickle(args.path)
    pm = PlotMagD(MagD)
    pm.plot().figure(figsize=(int(args.plotwidth), int(args.plotheight)))
    # pm.plot().rc("font", size=14)

    bounds = (MagD.lat_min, MagD.lat_max, MagD.lon_min,
              MagD.lon_max)
    map = pm.basemap(bounds)
    map.drawcoastlines(zorder=2)
    map.drawstates(zorder=2)
    map.drawcountries(zorder=2)

    X, Y = pm.project_x_y(map)

    if args.levels is not None:
        levels = args.levels.split(',')
        levels = [float(x) for x in levels]
        levels = np.array(levels)
        plot_min = np.min(levels)
        plot_max = np.max(levels)

    else:
        plot_min = float(args.plot_min)
        plot_max = float(args.plot_max)
        levels = MaxNLocator(nbins=args.nbins).tick_values(plot_min, plot_max)
    # Z = np.clip(MagD.matrix, plot_min, plot_max)

    Z = MagD.matrix
    X = np.array(X) + 0.5 / 2.
    Y = np.array(Y) + 0.5 / 2.
    cmap = pm.plot().get_cmap(args.color)

    # norm = BoundaryNorm(levels, ncolors=cmap.N, clip=False)
    cf = pm.plot().contourf(X, Y, Z, levels=levels, cmap=cmap,
                            vmim=plot_min, vmax=plot_max)
    solutions = MagD.firstn_solutions
    unit = None
    if args.plotstas:
        if len(solutions) > 0:
            s_lats = [s.obj.lat for s in solutions]
            s_lons = [s.obj.lon for s in solutions]
            Sx, Sy = map(s_lons, s_lats)
            pm.plot().scatter(Sx, Sy, s=60, marker='D', c="k",
                              label="Contributing stations", zorder=12)
        for key in MagD.markers:
            lats = [dest.lat for dest in MagD.markers[key]['collection']]
            lons = [dest.lon for dest in MagD.markers[key]['collection']]
            # find index of list where stations did not contrib to any
            # solution (looosers)
            Sx, Sy = map(lons, lats)
            color = MagD.markers[key]['color']
            symbol = MagD.markers[key]['symbol']
            label = MagD.markers[key]['label']
            size = int(MagD.markers[key]['size'])
            # print(MagD.markers[key])
            # once set we don't want to unset units
            if 'unit' in MagD.markers[key] and unit is None:
                unit = MagD.markers[key]['unit']
            pm.plot().scatter(Sx, Sy, s=size, marker=symbol, c=color,
                              label=label, zorder=11)

    bbox = (0.0, float(args.legend_pad))
    pm.plot().legend(bbox_to_anchor=bbox, loc=3, borderaxespad=0.,
                     scatterpoints=1, fontsize=15)

    clb = pm.plot().colorbar(cf, fraction=float(args.colorbar_fraction),
                             pad=float(args.colorbar_pad))
    # if unit is not None:
    clb.ax.set_title(unit, fontsize=12)
    clb.ax.set_yticklabels(clb.ax.get_yticklabels(), fontsize=12)

    meridian_interval = pm.meridian_interval(MagD.lon_min, MagD.lon_max)
    # #set linewidth to 0  to get only labels
    map.drawmeridians(meridian_interval, labels=[0, 0, 0, 1], dashes=[90, 8],
                      linewidth=0.0, fontsize=12)
    # map.drawmapscale(lon=-120.0, lat= 45.0, lon0=-120.0, lat0=45.0,
    #    length=50,
    #     barstyle='simple', fontsize = 14, units='km', yoffset=1,
    #     labelstyle='simple', fontcolor='k', fillcolor1='w',
    #     fillcolor2='k', ax=1, format='%d', zorder=1 )
    parallel_interval = pm.parallel_interval(MagD.lat_min, MagD.lat_max)
    map.drawparallels(parallel_interval, labels=[1, 0, 0, 0], dashes=[90, 8],
                      linewidth=0.0, fontsize=12)
    title_arr = [args.title1, args.title2, args.title3]
    title_arr = [x for x in title_arr if x is not None]
    title = "\n".join(title_arr)
    pm.plot().title(title, fontsize=20)

    # map.drawmapscale(x, y, x, y, 40 , barstyle='fancy')

    # fig_name = pm.outfile_with_stamp('./plots/')
    # pm.plot().savefig(fig_name)
    pm.plot().show()

if __name__ == "__main__":
    main()
