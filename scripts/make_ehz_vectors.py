import sys
import os

from magD.magD import MagD
if len(sys.argv)<2:
    print("provide config path as first arg and map output type for second arg")
    print("Example: python scripts/ehz_profile.py config/ehz_profile/ehz_and_bb.ini")
    exit(1)
config_path =sys.argv[1]
magD=MagD(config_path)
out=magD.create_grids()
print(out)
