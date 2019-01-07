'''
    Create MapGrid(s). Requries config file as input. See ./config for options
'''
import sys
import os
from magD.magD import MagD
from magD.mapGrid import MapGrid
import configparser
if len(sys.argv)<2:
    print("provide config path as first arg and map output type ")
    print("Example: python scripts/ehz_profile.py config/ehz_profile")
    exit(1)
config_dir =sys.argv[1]
grid_conf= configparser.ConfigParser()
grid_conf.read(config_dir + "/grid.ini")

data_conf= configparser.ConfigParser()
data_conf.read(config_dir + "/data.ini")
grids=[]
#create array and intatiate grid objecs
for type in ['detection', 'dist_min', 'dist_med', 'dist_ave', 'dist_max', 'gap']:
    grids.append(MapGrid(grid_conf['grid'], type))
data_srcs={}
for key in data_conf.sections():
    data_srcs[key]=data_conf[key]
magD=MagD(grids, data_srcs)
magD.build_grids()
