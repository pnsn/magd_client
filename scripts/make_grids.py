'''
    Create MapGrid(s). Requries config file as input. See ./config for options
'''
import os
from magD.mapGrid import MapGrid
import argparse
import configparser

# 1) 48˚, -125˚, 20 km offshore
# 2) 47˚, -124˚, 55 km  aberdeen
# 3) 48.5˚, -121˚, 10 km buckner

parser = argparse.ArgumentParser(description="A routine to make mapgrids")
parser.add_argument('-n', '--name', help='unique name of magD run',
                    required=True)
parser.add_argument('-g', '--grid_type', help="type of grid", required=True)
parser.add_argument('-an', '--lat_min', help="min lat", required=True)
parser.add_argument('-ax', '--lat_max', help="max lat", required=True)
parser.add_argument('-on', '--lon_min', help="min lon", required=True)
parser.add_argument('-ox', '--lon_max', help="max lon", required=True)
parser.add_argument('-r', '--resolution', help="grid resolution in degrees",
                    required=True)
parser.add_argument('-ns', '--num_solutions', help="number of stations needed",
                    default=4)
parser.add_argument('-nq', '--nyquist_correction', help="nyquist_correction",
                    default=0)
parser.add_argument('-mu', '--mu', help="mu", default=0)
parser.add_argument('-q', '--qconst', help="q", default=0)
parser.add_argument('-b', '--beta', help='beta', default=0)

args = parser.parse_args()  # show values #
root_path = os.path.dirname(os.path.realpath(__file__))
config_path = root_path + "/../config/" + args.name + ".ini"
pickle_path = root_path + "/../pickle_jar"
data_conf = configparser.ConfigParser()
data_conf.read(config_path)
grid_type = args.grid_type
# create array and intatiate grid objecs
# for use in jupyter notebook
grid = MapGrid(grid_type, args.name, float(args.resolution),
               float(args.lat_min), float(args.lat_max),
               float(args.lon_min), float(args.lon_max),
               int(args.num_solutions), float(args.nyquist_correction),
               float(args.mu), float(args.qconst), float(args.beta),
               pickle_path)
data_srcs = {}
for key in data_conf.sections():
    data_srcs[key] = data_conf[key]
grid.build_markers(data_srcs)
grid.build_origins()
grid.build_matrix()
grid.save()
'''
    expose __grid_path to interpreter (jupyter)
'''
_grid_path = grid.get_path()
print("Path for " + grid.type + ":")
print("  " + grid.get_path())
