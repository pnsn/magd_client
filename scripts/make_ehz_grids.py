import sys
import os
import re
from magD.magD import MagD
from magD.mapGrid import MapGrid
import configparser
if len(sys.argv)<2:
    print("provide config path as first arg and map output type for second arg")
    print("Example: python scripts/ehz_profile.py config/ehz_profile/ehz_and_bb.ini")
    exit(1)
config_path =sys.argv[1]

conf= configparser.ConfigParser()
conf.read(config_path)

grids=[]
for type in ['detection', 'dist_min', 'dist_med', 'dist_ave', 'dist_max','gap']:
    grids.append(MapGrid(conf['main'], type))
data_srcs={}
for key in conf.sections():
    if re.match(r'noise', key):
        data_srcs[key]=conf[key]
magD=MagD(grids, data_srcs)
magD.build_grids()
# print(out)
