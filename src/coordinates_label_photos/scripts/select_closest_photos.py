import argparse
import logging
import os
import csv
import shutil
from pathlib import Path

from coordinates_label_photos.coordinates import exif_to_coordinates, Coordinates
from coordinates_label_photos.coordinates.coordinates_collection import CoordinatesCollection
from coordinates_label_photos.photos import list_photo_filenames, get_photo_exif
from PIL import Image, ImageDraw, ImageFont


def load_coords_csv(filename) -> CoordinatesCollection:
    logging.info('Loading CSV coordinates from %s' % filename)
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        coords = []

        for row in reader:
            coords.append(
                Coordinates(
                    lat=float(row['Latitude']),
                    lon=float(row['Longitude']),
                    elevation=float(row['Elevation']),
                    timestamp=None,
                    label=row['Name']
                )
            )
        collect = CoordinatesCollection(coords)
        logging.info('Loaded CSV with %d track points between %s and %s' % (
            len(collect), collect.start_time(), collect.end_time()))
        return collect


def report(
        all_photos,
        selected_photos,
        coords,
        filename,
        max_dim
):
    logging.info('Saving report in %s' % filename)
    all_coords = [c for c in coords.points]
    all_coords.extend(all_photos.values())
    all_coords = CoordinatesCollection(all_coords)

    boundaries = all_coords.lat_lon_boundaries()
    dim_lat = boundaries[1].lat - boundaries[0].lat
    dim_lon = boundaries[1].lon - boundaries[0].lon
    dimensions = all_coords.dimensions()
    if dimensions[0] > dimensions[1]:
        width = max_dim * 0.8
        height = max_dim * dimensions[1] / dimensions[0]
    else:
        height = max_dim * 0.8
        width = max_dim * dimensions[1] / dimensions[0]

    margin = max_dim * 0.1

    img = Image.new('RGB', (int(width + 2 * margin), int(height + 2 * margin)), 'white')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('/System/Library/Fonts/Geneva.ttf', size=10)

    def coord_xy(c: Coordinates):
        (x, y) = (margin + int((c.lon - boundaries[0].lon) / dim_lon * width),
                  margin + int((c.lat - boundaries[0].lat) / dim_lat * height))
        # print('%s\t%d\t%d' % (c, x, y))

        return x, y

    prev = None
    for c in coords.points:
        (x, y) = coord_xy(c)
        draw.text((x + 4, y + 4), c.label, fill='black', font=font)
        draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill='black')

        if prev is not None:
            draw.line([(x, y), (prev['x'], prev['y'])], fill='grey')
        prev = {
            'x': x,
            'y': y,
        }
    for (p, c) in all_photos.items():
        (x, y) = coord_xy(c)
        name = Path(p).stem
        draw.text((x + 4, y + 4), name, fill='black', font=font)
        draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill='red')

    for (p, c) in selected_photos.items():
        (x, y) = coord_xy(all_photos[p])
        draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill='green')
        (xc, yc) = coord_xy(c)
        draw.line([(x, y), (xc, yc)], fill='green')

    img.save(filename)


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(description='Select the closest pictures to a given list of positions')

    parser.add_argument(
        "--coords",
        help='emlid csv coordinate files',
        type=str,
        metavar='path/to/coords.csv'

    )
    parser.add_argument(
        "--images",
        help="image directory",
        type=str,
        required=True,
        metavar='/path/to/images'
    )
    parser.add_argument(
        "--dest",
        help="the destination directory for the selected images",
        type=str,
        required=True,
        metavar='/path/to/dir'
    )
    parser.add_argument(
        "--report",
        help="an image filename where to report matching photos",
        type=str,
        metavar='/path/to/report-photo-closest.jpeg'
    )
    args = parser.parse_args()

    photo_coords = {}
    for photo in list_photo_filenames(args.images):
        exif = get_photo_exif(photo)
        c = exif_to_coordinates(exif)
        c.elevation = 0
        photo_coords[photo] = c

    selected_photos = {}
    coords = load_coords_csv(args.coords)
    for coord in coords.points:
        # find closest
        closest_photo = min(photo_coords.keys(), key=lambda p: coord.distance(photo_coords[p]))

        if closest_photo not in selected_photos:
            # it must be the closest photo to the point, but the reciprocal must also be true
            closest_coords_to_photo = min(coords.points, key=lambda c1: c1.distance(photo_coords[closest_photo]))
            if closest_coords_to_photo == coord:
                selected_photos[closest_photo] = coord

    dest_dir = args.dest
    os.makedirs(dest_dir, exist_ok=True)
    for photo in selected_photos.keys():
        shutil.copy(photo, dest_dir)

    if args.report is not None:
        report(
            all_photos=photo_coords,
            selected_photos=selected_photos,
            coords=coords,
            max_dim=2500,
            filename=args.report
        )


if __name__ == '__main__':
    main()
