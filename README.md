# Coordinates label photos

**The problem we are trying to solve:** On the one hand, we have a photos with unlabeled GPS data, but only a timestamp.
In the other hand, we have a GPS track, with coordinates and timestamp. 
This situation is originally caused by the fact that pictures are taken underwater but we can position a GPS above the water.
Our purpose is to interpolate the GPS position from the track, with the photo timestamp and insert the information in the EXIF photo metadata.

## Installation 

    pip install coordinates-label-photos

## Run
To label all images from `/path/to/images-directory/*` with the GPX track points from `path/to/your.gpx` or LLH (Reach RS 2) format:

    coordinates-label-photos --coords=/path/to/your.gpx --images=/path/to/images-directory

With optional arguments:
  * `--report-photo-locations=/path/to/report-photo-locations.jpeg` to generate an image with photo locations
  * `--report-track=/path/to/report-track.jpeg` to generate an image with the track points

## Other Utils

A few side tools may come handy in some situations

### Removing GPS infomration from pictures

    coordinates-clear-photos --images=/path/to/images-directory


### Selecting the closest images to a point list

During acquisition, excessive number of pictures can be taken (when strolling outside of the perimeter or moving not fast enough).
If we provide a list of positions where the images should have been taken, we can select only the closest images to each of those position.

    select-closest-photos \
         --coords=/path/to/perfect-positions.csv  \
         --images=/source/image/directory \
         --dest=/selected/image/directory \
         --report=/path/to/report.png

### Comparing GPX tracks

Compare various coords tracks, from .gpx, .llh, .pos (useful to plot the same track from different GPS):

    plot-coords-tracks --gpx="gps A:/path/to/a.gpx"  --gpx="gps B:/path/to/b.gpx" --output=/path/to/plot.jpeg

### Extracting photos coordinates to a GPX file

From a directory containing images (with GPS locations), create a GPX file:

    images-to-gpx --output=/path/to/a.gpx  --images=/path/to/images-directory

### License 
MIT

