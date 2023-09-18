import argparse
import logging

import piexif
from piexif import TAGS

from coordinates_label_photos.photos import get_photo_timestamp, get_photo_exif


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='print EXIF information')

    parser.add_argument('files', nargs=argparse.REMAINDER)

    args = parser.parse_args()
    print(args.files)

    for f in args.files:
        print(f)
        print(get_photo_timestamp(f))
        exif = get_photo_exif(f)
        for p, f in [
            ['0th', piexif.ImageIFD.Model],
            ['0th', piexif.ImageIFD.DateTime],
            ['Exif', piexif.ExifIFD.SubSecTime],
            ['Exif', piexif.ExifIFD.OffsetTime],
            ['Exif', piexif.ExifIFD.DateTimeOriginal],
            ['Exif', piexif.ExifIFD.SubSecTimeOriginal],
            ['Exif', piexif.ExifIFD.OffsetTimeOriginal],
            ['Exif', piexif.ExifIFD.DateTimeDigitized],
            ['Exif', piexif.ExifIFD.SubSecTimeDigitized],
            ['Exif', piexif.ExifIFD.OffsetTimeDigitized],
        ]:
            print('%s/%s: %s' % (p, TAGS[p][f]['name'], exif[p][f].decode("utf-8")))


if __name__ == '__main__':
    main()
