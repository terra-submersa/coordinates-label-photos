import argparse
import logging

from coordinates_label_photos.gpx import gpx_parser
from coordinates_label_photos.reports.coordinates_collection import CoordinatesCollection, \
    report_image_coordinates_collections


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(description='Plot gpx tracks')

    parser.add_argument("gpx", help='label and path to GPX file', type=str, nargs='+',
                        metavar='label:path/to/file.gpx')
    parser.add_argument("--output", help="output image with track points comparisons", type=str, required=True,
                        metavar='/path/to/output.jpeg')

    args = parser.parse_args()

    all_coords = CoordinatesCollection([])
    for e in getattr(args, 'gpx'):
        tmp = e.split(':', maxsplit=2)
        label = tmp[0]
        gpx_file = tmp[1]
        cs = gpx_parser(gpx_file)
        cs.label_all(label)
        all_coords.add(cs)
    report_image_coordinates_collections(all_coords, getattr(args, 'output'), 1000, color_by_label=True)


if __name__ == '__main__':
    main()
