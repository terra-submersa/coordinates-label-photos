import argparse
import logging
import gpxpy as gpxpy
from tqdm import tqdm

from coordinates_label_photos.coordinates import exif_to_coordinates
from coordinates_label_photos.photos import list_photo_filenames, get_photo_exif


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='extract GPS coordinates from an image folder and create a gpx track')

    parser.add_argument("--images", help="image directory (edited in place)", type=str, required=True,
                        metavar='/path/to/images')
    parser.add_argument("--output", help=".gpx coordinates file", type=str, required=True, metavar='/path/to/gpx')

    args = parser.parse_args()

    photos = list_photo_filenames(getattr(args, 'images'))

    gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    for photo in tqdm(photos, desc='Parsing images'):
        exif = get_photo_exif(photo)
        coord = exif_to_coordinates(exif)
        gpx_segment.points.append(
            gpxpy.gpx.GPXTrackPoint(coord.lat, coord.lon, elevation=coord.elevation, time=coord.timestamp))

    gpx_file=getattr(args, 'output')
    with open(gpx_file, 'w') as fd_out:
        fd_out.write(gpx.to_xml())
        fd_out.close()
        logging.info('Saved %s points in GPX %s' % (len(photos), gpx_file))

if __name__ == '__main__':
    main()
