# Coordinates label photos

**The problem we are trying to solve:** On the one hand, we have a photos with unlabeled GPS data, but only a timestamp.
In the other hand, we have a GPS track, with coordinates and timestamp. 
This situation is originally caused by the fact that pictures are taken underwater but we can position a GPS above the water.
Our purpose is to interpolate the GPS position from the track, with the photo timestamp and insert the information in the EXIF photo metadata.

A demo script can be found with `calibrate_photos.py`.

### License 
MIT

