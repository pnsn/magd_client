import sys
import os
from pathlib import Path

from magD.plotMagD import PlotMagD
from magD.magD import MagD
if len(sys.argv)<2:
    print("provide config path as first arg")
    print("Example: python scripts/ehz_profile.py config/ehz_profile/ehz_and_bb.ini")
    exit(1)
config_path =sys.argv[1]
magD=MagD(config_path)
other_mag_grid_path=None
if magD.diff_with:
    other_mag_grid_path=magD.get_pickle_grid_path('mag_grid',
                magD.diff_with, magD.grid_resolution)
    other_mag_grid_file= Path(other_mag_grid_path)
    if not other_mag_grid_file.is_file():
        print("Other diff file not found!")
        print("Expected: {}".format(other_mag_grid_path))
        exit(1)

magD.get_noise()
#only go through find detections if pickle file doesn't exist
this_mag_grid_path=magD.get_pickle_grid_path('mag_grid',
            magD.name, magD.grid_resolution)
this_mag_grid_file= Path(this_mag_grid_path)
if this_mag_grid_file.is_file():
    mag_grid= magD.get_pickle(this_mag_grid_path)
else:
    print("no file here...")
    magD.find_detections()
    mag_grid=magD.get_mag_grid()
    magD.pickle_mag_grid()
    sum=magD.print_summary()
    print(sum)


pm=PlotMagD(magD)
fig=pm.plot().figure(figsize=(10,12))
pm.plot().rc("font", size=14)

bounds=(magD.lat_min, magD.lat_max, magD.lon_min, magD.lon_max)
map=pm.basemap(bounds)
map.drawcoastlines(zorder=1)
map.drawstates(zorder=2)
map.drawcountries(zorder=2)

# diff the two matrices
if other_mag_grid_path:
    other_path=magD.get_pickle_grid_path('mag_grid',
        magD.diff_with, magD.grid_resolution)
    other_mag_grid=magD.get_pickle(other_path)
    mag_grid = [a - b  for a, b in zip(mag_grid, other_mag_grid)]

# levels=pm.create_contour_levels(mag_grid, 2)
X,Y=pm.project_x_y(map)
Z= pm.mag_matrix(mag_grid)
min=float(magD.plot_mag_min)
max=float(magD.plot_mag_max)

pm.plot().pcolormesh(X,Y,Z,zorder=0, vmin=min, vmax=max)
pm.plot().colorbar()
# cs =map.contour(X,Y,Z,levels, colors="k")#,colors="k",zorder=3,linewidths=0.5)

# #incresing from 10 t0a
# pm.plot().clabel(cs, inline=1, fontsize=12,fmt='%1.1f')

meridian_interval=pm.meridian_interval(magD.lon_min, magD.lon_max)
# #set linewidth to 0  to get only labels
map.drawmeridians(meridian_interval,labels=[0,0,0,1],
dashes=[90,8], linewidth=0.0)
parallel_interval=pm.parallel_interval(magD.lat_min, magD.lat_max)
map.drawparallels(parallel_interval,labels=[1,0,0,0],
dashes=[90,8], linewidth=0.0)

# #zorder puts it at lowest plot level
# map.fillcontinents(color='0.95',zorder=1)
pm.plot().title(
    "{}\n {} station detection {} deg. grid".format(
    magD.title, magD.num_detections, magD.grid_resolution))
# #should we add no solution symbol to legend?
no_solution=False
#iterate through sets and assign color

# for key in magD.scnl_collections():
#   #plot station data
#   lats, lons, sols=magD.get_xyz_lists(key)
#   #find index of list where stations did not contrib to any solution (looosers)
#   no_i=magD.get_no_solution_index(key)
#
#
#   if no_i < len(lons)-1:
#       no_solution=True
#   #contributed to solution
#   Sx,Sy=map(lons[:no_i], lats[:no_i])
#   #did not contrib to solution
#   Sxn,Syn=map(lons[no_i:], lats[no_i:])
#
#   color,label=pm.plot_color_label(key)
#   stas=pm.plot().scatter(Sx, Sy, s=70, marker='^', c=color, label=label,zorder=11)
#   #plot no solutions but don't create a legend entry for each
#   pm.plot().scatter(Sxn, Syn, s=30, marker='o', facecolors='none', edgecolors=color,zorder=11)

#create legend for no solutions
if no_solution:
  pm.plot().scatter([-1],[-1], s=30, marker='o',facecolors='none',edgecolor='k',label="No solution")
#bbox coords= x,y,width,height
bbox=(0.0,-0.2)
# pm.plot().legend(bbox_to_anchor=bbox, loc=3, borderaxespad=0.,scatterpoints=1)

plot_path="./plots/{}".format(magD.name)
fig_name=pm.outfile_with_stamp(plot_path)
pm.plot().savefig(fig_name)
pm.plot().show()
