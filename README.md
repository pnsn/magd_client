# magd_client
A client for running magD and storing MapGrids (for plotting) and plots

https://github.com/pnsn/magD

To run locally, clone MagD, then

pip install .

# MagD plot steps
See notebooks/* for real examples
## Create initial csv of SCNLs you want to profile
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

## Make MapGrid objects
This is the CPU intensive step
### Types of mapGrids:
 * **detection**: detection Grid, uses largest magnitude of n stations)
 * **gap**: largest azimuthal gap of n stations
 * **Distance** grids (only considers the n stations)
   * **dist_min**: closest station
   * **dist_med**: median station
   * **dist_ave**: average station
   * **dist_max**: furthest station
   * **blindzone**: radius of blindzone
* **time**:
    * **trigger_time**: Time to trigger once n station reports
    * **warning_time**: p arrival - trigger_time

### Process  
* Process above csv
* Step through all points (origins) on map and evaluate:
* If profiling by noise:
    * Get noise PDF from pickle (if exists) or IRIS Mustang
    * Save all PDFs locally with pickle
    * For each origin
        * Evaluate each station's PDF to find lowest detectable mag.
        * Sort all solutions by mag (low to high) from each origin
        * Consider only [0:num_solutions] of sorted list
            * Lowest detection is last solution
            * Azimuthal gap is largest gap of new list
            * Distance stat only considers new list
* If profiling only spatially:
    * For each origin
        * Sort all stations by distance from each origin
        * Consider only [0:num_solutions] of sorted list
            * Azimuthal gap is largest gap of new list
            * Distance stat only considers new list


  ## Create aggregate MapGrids if needed.
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

## Plot MapGrids
Use PlotMapD class to plot MapGrids

The script scripts/plot_heatmap.py gives plot examples.

To create time use distance matrix and PlotMagD functions to transform matrix
* blindzone: calc_blindzone(self, epi_distance, velocity_p, velocity_s, depth)
  * epi_distance, float, km
  * velocity_p, float, km/s
  * velocity_s, float, km/s
  * depth, float, km

* trigger_time(self,epi_distance, velocity_p, depth, processing_time)
  * epi_distance, float, km
  * velocity_p, float, km/s
  * depth, float, km
  * processing_time, float, seconds

* warning_time(self,epi_distance, velocity_p, velocity_s, depth, processing_time)
  * epi_distance, float, km
  * velocity_p, float, km/s
  * velocity_s, float, km/s
  * depth, float, km
  * processing_time, float, seconds

PlotMagD uses matplotlib but you can use any plotting library you please.

See https://github.com/pnsn/magD for class details
