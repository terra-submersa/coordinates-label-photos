import argparse
import logging

from coordinates_label_photos.gpx import gpx_parser
from coordinates_label_photos.photos import list_photo_filenames, calibrate_photo
from coordinates_label_photos.reports.coordinates_collection import report_image_coordinates_collections


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Labels photos with a GPS track points (.gpx)')

    parser.add_argument("--gpx", help=".gpx coordinates file", type=str, required=True, metavar='/path/to/gpx')
    parser.add_argument("--images", help="image directory (edited in place)", type=str, required=True,
                        metavar='/path/to/images')
    parser.add_argument("--report-photo-locations", help="an image filename where to report the photo locations",
                        type=str, metavar='/path/to/report-photo-locations.jpeg')
    parser.add_argument("--report-track", help="an image filename where to report the original GPS coordinates",
                        type=str, metavar='/path/to/report-track.jpeg')

    args = parser.parse_args()

    photos = list_photo_filenames(getattr(args, 'images'))
    track_coords = gpx_parser(args.gpx)
    photo_coords = calibrate_photo(photos=photos, track_coords=track_coords)
    if getattr(args, 'report_track') is not None:
        logging.info('Saving track %s' % getattr(args, 'report_track') )
        report_image_coordinates_collections(track_coords, getattr(args, 'report_track') , 1000)
    if getattr(args, 'report_photo_locations') is not None:
        logging.info('Saving photo locations %s' % getattr(args, 'report_photo_locations'))
        report_image_coordinates_collections(photo_coords, getattr(args, 'report_photo_locations'), 1000)


if __name__ == '__main__':
    main()
