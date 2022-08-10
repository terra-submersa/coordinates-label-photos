import argparse
import logging

from coordinates_label_photos.parsers import coords_parser
from coordinates_label_photos.photos import list_photo_filenames, calibrate_photo, clear_photo_exif
from coordinates_label_photos.reports.coordinates_collection import report_image_coordinates_collections


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Clear GPS information from photos')

    parser.add_argument(
        "--images",
        help="image directory (edited in place)",
        type=str,
        required=True,
        metavar='/path/to/images'
    )

    args = parser.parse_args()

    for p in list_photo_filenames(getattr(args, 'images')):
        clear_photo_exif(p, 'GPS')
        logging.info('Cleared GPS from %s' % p)


if __name__ == '__main__':
    main()
