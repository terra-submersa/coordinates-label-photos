import argparse
import logging

from coordinates_label_photos.parsers import coords_parser


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(description='Select the closest pictures to a given list of positions')

    parser.add_argument("coords", help='.GPX, .LLH or .POS  coordinate files', type=str, nargs='+',
                        metavar='path/to/coords.(gpx|llh|pos)')
    parser.add_argument("--dest", help="the destination directory for the selected images", type=str, required=True,
                        metavar='/path/to/dir')

    args = parser.parse_args()

    cs = coords_parser(args.coords)


if __name__ == '__main__':
    main()
