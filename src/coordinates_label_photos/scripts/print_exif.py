import argparse
import logging

from coordinates_label_photos.photos import get_photo_timestamp,get_photo_exif


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='print EXIF information')

    parser.add_argument('files', nargs=argparse.REMAINDER)

    args = parser.parse_args()
    print(args.files)

    for f in args.files:
        print(f)
        print(get_photo_timestamp(f))


if __name__ == '__main__':
    main()
