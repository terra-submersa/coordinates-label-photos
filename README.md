# Coordinates label photos

**The problem we are trying to solve:** On the one hand, we have a photos with unlabeled GPS data, but only a timestamp.
In the other hand, we have a GPS track, with coordinates and timestamp. 
This situation is originally caused by the fact that pictures are taken underwater but we can position a GPS above the water.
Our purpose is to interpolate the GPS position from the track, with the photo timestamp and insert the information in the EXIF photo metadata.

## Installation 

    pip install coordinates-label-photos

## Run
To label all images from `/path/to/images-directory/*` with the GPX track points from `path/to/your.gpx`:

    coordinates-label-photos --gpx=/path/to/your.gpx --images=/path/to/images-directory

With optional arguments:
  * `--report-photo-position=/path/to/report-photo-positions.jpeg` to generate an image with photo positions
  * `--report-track=/path/to/report-track.jpeg` to generate an image with the track points

### Comparing GPX tracks

A side tool is available to compared various .gpx tracks (useful to plot the same track from different GPS)

    plot-gpx-tracks --gpx="gps A:/path/to/a.gpx"  --gpx="gps B:/path/to/b.gpx" --output=/path/to/plot.jpeg

### License 
MIT

