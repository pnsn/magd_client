# magd_client
A client for running magD and storing MapGrids (for plotting) and plots

https://github.com/pnsn/magD

To run locally, clone MagD, then

pip install .

#MagD plot steps
See notebooks/* for real examples
##Create initial csv of SCNLs you want to profile
To request station data from fdsn the following csv format is needed:
* sta,
* seedchan,
* net,
* location

Example:
<pre>
sta,seedchan,net,location
"NLO","EHZ","UW",""
"GLDO","EHZ","UW",""
</pre>
##Run make_csv.py
To get the location and sample rate, use magD/make_csv.py, which takes the above
formated csv and outputs a csv file fomated for MagD:

`python magD/make_csv.py -i input_file -o output_file`

Example:

`python magD/make_csv.py -i csv/2017_EHZ_study/all_bb.csv -o csv/2017_EHZ_study/all_bb_fdsn.csv`

Output csv format:

* sta,
* chan,
* net,
* location,
* lat,
* lon,
* depth,
* on_date,
* off_date,
* rate

Example:
<pre>
sta,chan,net,location,lat,lon,depth,on_date,off_date,rate
GLDO,EHZ,UW,,45.838779,-120.814789,0.0,,,100.0
OSD,EHZ,UW,,47.816238,-123.705109,0.0,,,100.0
</pre>

Run
Run Example:

<pre>
  python magD/make_csv.py -i csv/2017_EHZ_study/all_bb.csv -o csv/2017_EHZ_study/all_bb_fdsn.csv
</pre>

This step can be skipped if you provide the above formatted csv

##Make MapGrid objects
This is the CPU intensive step. This process has the following steps:

* Process above csv
* Get noise PDF for IRIS Mustang
* Save all PDFs locally with pickle
* Step through all points on map and evaluate every PDF, sort by magnitude asc

Based on the above find the n stations (num_detections) with the lowest magnitude and produces the following mapGrids:
  * **detection**: detection Grid, uses largest magnitude of n stations)
  * **gap**: largest azimuthal gap of n stations
  * Distance grids (only considers the n stations)
    * **dist_min**: closest station
    * **dist_med**: median station
    * **dist_ave**: average station
    * **dist_max**: furthest station

  ##Create aggregate MapGrids if needed.
  Once MapGrids are saved, you can aggregate and save as needed. See notebooks for real examples. If you would like to diff two detection grids

  Instantiate both:

  `grid1=get_pickle('./pickle_jar/detection_grid/grid1.pickle')`

  `grid2=get_pickle('./pickle_jar/detection_grid/grid2.pickle')`

  Deep copy one and give it a name and type:

  `diff_grid=grid1.copy("diff_grid", "diff_grid")`

  Assign the new MapGrid matrix. Matrices are saved as 2dim numpy arrays:

  `diff_grid.matrix=grid1.matrix - grid2.matrix`

  save

  `diff_grid.save()`

##Plot MapGrids
Use PlotMapD class to plot MapGrids

The script scripts/plot_ehz_profile.py gives plot examples.

PlotMagD uses matplotlib but you can use any plotting library you please.

See https://github.com/pnsn/magD for class details
