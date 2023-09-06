# Do we have the correct image positions, after the `label_photos` post processing?
When we take pictures with a GoPro Hero 8 underwater, we do not have the camera coordinates, but we have:
  * the timestamp of the image with high precision is the camera is update with the GoPro Lab formware and we calibrate it with https://gopro.github.io/labs/control/precisiontime/
  * the delta between when the picture is triggered (click) and actually recorded (~880ms)
  * The high precision GPS coordinates of the boat (Reach RS2), recorded every 0.2 seconds

We can use the GPS coordinates of the boat to interpolate the position of the camera at the time the picture was taken.

The experiment is to validate if we actually record the actual position

## Setup
 
* We set up a target and record its position with the Reach RS2
* We set scale the ground every ten centimeters, going north
* We move the camera over the ground at roughly 2km/h (0.56 m/s), taking pictures every 1 second
* The camera is under the GPS, but with the handle, shifted southwards by 7 centimeters
* We look at the picture taken, somewhere along the scale (as we do not master when the /1s picture is taken) 

## Hypothesis
The computed position is the actual one (within a couple centimeters), because we do all the magic in the right way.
If the inferred position, through the process pipeline, is not correct, we have a problem.
This experiment is simply a test of the `label_photos.py` process. No big science here, simply a check.

## Results
### Data
  * The collected images are in the [images](measures/images) folder, and their estimated position along a south/north axis  in the [image-estimated-positions.csv](measures/image-estimated-positions.csv) file.
  * The position of the target middle (the 2.0m mark on the ladder) is measured several times in [emlid-0-positions.csv](measures/emlid-0-positions.csv).
  * The Emlid LLH track is in [emlid-localhost_solution_20230812112902.LLH](measures/emlid-localhost_solution_20230812112902.LLH)


### Processing
All coordinates are in EPSG:32634 (WGS 84 / UTM zone 34N).

#### Interpolate the image positions

We apply the `coordinates-label-photos` scripts and push the estimated positions of the images in the [images-computed-positions.csv](results/images-computed-positions.csv) file. 
    coordinates-label-photos \
      --coords=measures/emlid-localhost_solution_20230812112902.LLH \     # the Emlid track
      --images='measures/images/*.JPG' \                                  # all images in the folder
      --photo-timestamp-correction=18.88 \                                # 18 seconds for the GPS "timezone" offset + 880ms for the camera delay
      --photo-timezone-offset=+03:00 \                                    # Images were shot in Greece
      --skip-photo-edit \                                                 # We do not alter the image EXIF
      --odm-geo=results/images-computed-positions.csv                     # save image coordinates in a separate file

#### Computing the deltas       

Simply running the `get_delta.py` script returns:

    name          computedPosition  MeasuredPosition   delta
    G0272859.JPG            -0.535            -0.520  -0.015
    G0272860.JPG            -0.367            -0.350  -0.017
    G0272861.JPG            -0.153            -0.120  -0.033
    G0272862.JPG             0.046             0.080  -0.034
    G0272863.JPG             0.248             0.300  -0.052
    G0272864.JPG             0.550             0.560  -0.010
    G0272869.JPG            -0.501            -0.490  -0.011
    G0272870.JPG            -0.114            -0.110  -0.004
    G0272871.JPG             0.328             0.320   0.008
    G0272876.JPG            -0.207            -0.250   0.043
    G0272877.JPG             0.527             0.530  -0.003
    G0272882.JPG            -0.112            -0.150   0.038
    G0272883.JPG             0.505             0.510  -0.005
    G0272889.JPG            -0.125            -0.090  -0.035
    G0272890.JPG             0.464             0.470  -0.006

For each image, the last column is the difference between the computed and the measured position.

## Discussion
The delta standard deviation is 2.6 centimeters. This is totally tolerable, regarding the DGPS precision and the approximate experimental setup (moving speed and setup verticality).
Again, our goal here is to validate the `label_photos` process, not to get to the best precision.

### Magic 880ms: the photo trigger timestamp vs the actual picture taken estimation
Any digital camera has a delay between the moment the picture is triggered and the moment it is actually taken.
On the Gropro Hero 8, this delay is not neglectible.
At a swimming speed of 2 km/h, a one second delay is roughly 0.56 meters.
#### Empirical estimation
We can estimate this delay by taking a picture of a precise clock, and compare the time on the picture with the actual time.
This delta was estimated at roughly 600ms, but the setup is different than the one used in this experiment. At least, it shows how large the delta can be.
#### Numerical estimation
We used the experiment collected data to estimate the delay.
This was done using a solver to minimize the error between the estimated position and the actual position.
The result is that the delay is roughly 880ms.

#### How to solve this key problem?
The 880ms delay is a problem, because it is not constant. It depends many factors such as luminosity, speed, focus complexity, etc.

The first solution is to use a camera with a lower delay. The GoPro Hero 8 is not the best choice, but it was the only one we had on the field. 
But except if this delay is below 50 ms, we will still have a problem.

The second solution is to check if some water-proof camera populate the image exif meta data with relevant attributes, such as `DateTimeDigitized` or `DateTimeOffset`.

A third solution would be to have a high precision clock and drop it in the water, to compare picture time with the actual one.
After the Ground Control Points, we might need Time Control Points.


