import sys
import os
import numpy as np
import math

from magD.plotMagD import PlotMagD
from magD.magD import MagD
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator


if len(sys.argv)<3:
    print("provide config path as first arg and map output type for second arg")
    print("Example: python scripts/ehz_profile.py config/ehz_profile/ehz_and_bb.ini detection")
    print("available map types are detection and gap and distance")
    exit(1)
config_path =sys.argv[1]
type=sys.argv[2]
magD=MagD(config_path,type)
pm=PlotMagD(magD,type)

magD.read_grids()

fig=pm.plot().figure(figsize=(10,12))
pm.plot().rc("font", size=14)

bounds=(magD.lat_min, magD.lat_max, magD.lon_min, magD.lon_max)
map=pm.basemap(bounds)
map.drawcoastlines(zorder=2)
map.drawstates(zorder=2)
map.drawcountries(zorder=2)



# levels=pm.create_contour_levels(detect_vector, 2)
X,Y=pm.project_x_y(map)

#make grids and compare if needed
grids=[]

for g in [magD.grid, magD.other_grid]:
    if g:
        grid=[]
        mat=g.matrix
        max=np.max(mat)
        for row in g.matrix:
            if g.type=="distance":
                r=[math.log(distance)/math.log(max) for distance in row]
            elif g.type=="gap":
                r=[gap/max for gap in row]
            else:
                r=row
            grid.append(r)
        grids.append(grid)


#are we comparing two grids?
if magD.other_grid:
    this_grid, other_grid= grids
    composite_grid=[]
    for i in range(len(this_grid)):
        if magD.compare_operator=='diff':
            r =[a - b  for a, b in zip(this_grid[i], other_grid[i])]
        if magD.compare_operator=='sum':
            r =[(a + b)*0.5  for a, b in zip(this_grid[i], other_grid[i])]
        composite_grid.append(r)
    Z=np.array(composite_grid)
else:
    Z=np.array(grids[0])
X=np.array(X) + 0.5/2.
Y=np.array(Y) + 0.5/2.
levels = MaxNLocator(nbins=10).tick_values(np.min(Z), np.max(Z))
cmap = pm.plot().get_cmap('Blues')
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

# if pm.type=="detection":
    # cm=pm.plot().pcolormesh(X,Y,Z,zorder=0, vmin=pm.mag_min, vmax=pm.mag_max)
# else:
cf = pm.plot().contourf(X, Y, Z, levels=levels, cmap=cmap)
    # cm=pm.plot().pcolormesh(X,Y,Z,zorder=0,cmap=cmap,norm=norm)
pm.plot().colorbar(cf)
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
header=""
if type=="detection":
    header="Minimum Magnitude Detection"
elif type=="gap":
    header="Largest Azimuthal Gap"
else:
    header="Distance to closest station"

pm.plot().title(
    "{}\n{}\n {} station detection {} deg. grid".format(
    header,pm.title, magD.num_detections, magD.grid_resolution))
# #should we add no solution symbol to legend?
# no_solution=False
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

# #create legend for no solutions
# if no_solution:
#   pm.plot().scatter([-1],[-1], s=30, marker='o',facecolors='none',edgecolor='k',label="No solution")
#bbox coords= x,y,width,height
# bbox=(0.0,-0.2)
# pm.plot().legend(bbox_to_anchor=bbox, loc=3, borderaxespad=0.,scatterpoints=1)

plot_path="./plots/{}".format(magD.name)
fig_name=pm.outfile_with_stamp(plot_path)
pm.plot().savefig(fig_name)
pm.plot().show()
