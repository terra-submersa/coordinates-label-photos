import argparse
import logging

from coordinates_label_photos.coordinates.crs_transformer import crs_epsg_code, crs_transformer_deg_epsg
from coordinates_label_photos.parsers import coords_parser
from coordinates_label_photos.photos import list_photo_filenames, calibrate_photo
from coordinates_label_photos.reports.coordinates_collection import report_image_coordinates_collections


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description='Labels photos with a GPS track points (.gpx)')

    parser.add_argument(
        "--coords",
        help=".gpx|.llh coordinates file",
        type=str,
        required=True,
        metavar='/path/to/coords'
    )
    parser.add_argument(
        "--images",
        help="image directory (edited in place) or glob",
        type=str,
        required=True,
        metavar='/path/to/images/*/*.JPG'
    )
    parser.add_argument(
        "--photo-timezone-offset",
        help="In case it's not in the photo EXIF (e.g. '+0300)",
        type=str,
        required=False,
        metavar='+0300'
    )
    parser.add_argument(
        "--photo-timestamp-correction",
        help="set the delta between the camera timestamp and the accurate time, in seconds."
             "This is done to counter a slightly off camera timer calibration."
             "If camera shows 7:42:22, when it 7:41:07.3 on the GPS, the error is -74.7",
        type=float,
        metavar='-74.7'
    )
    parser.add_argument(
        "--odm-geo",
        help="Image locations in a OpenDroneMap geo location format",
        type=str,
        metavar='/path/to/odm-geo.txt'
    )
    parser.add_argument(
        "--epsg-code",
        help="EPSG digit code. If none provided, it will be guessed from the coordinates",
        type=str,
        metavar='22332'
    )
    parser.add_argument(
        "--horizontal-accuracy",
        help="horizontal accuracy (GPS + device) in meters",
        type=float,
        metavar='0.4'
    )
    parser.add_argument(
        "--vertical-accuracy",
        help="vertical accuracy (GPS + device) in meters",
        type=float,
        metavar='0.3'
    )
    parser.add_argument(
        "--camera-fixed-elevation",
        help="fix the camera altitude (e.g. -0.3m)" +
             " in meters",
        type=float,
        metavar='-0.3'
    )
    parser.add_argument(
        "--skip-photo-edit",
        help="When not set, the photos are edited in place",
        action='store_true'
    )
    parser.add_argument(
        "--report-photo-locations",
        help="an image filename where to report the photo locations",
        type=str,
        metavar='/path/to/report-photo-locations.jpeg'
    )
    parser.add_argument(
        "--report-track",
        help="an image filename where to report the original GPS coordinates",
        type=str,
        metavar='/path/to/report-track.jpeg'
    )

    args = parser.parse_args()

    photos = list_photo_filenames(getattr(args, 'images'))
    track_coords = coords_parser(args.coords)
    print('%d recorded coordinates between %s and %s'%(
        len(track_coords),
        track_coords.start_time(),
        track_coords.end_time()
    ))
    photo_coords = calibrate_photo(
        photos=photos,
        track_coords=track_coords,
        photo_timezone_offset=args.photo_timezone_offset,
        photo_timestamp_correction = args.photo_timestamp_correction,
        camera_fixed_elevation=args.camera_fixed_elevation,
        horizontal_accuracy=args.horizontal_accuracy,
        vertical_accuracy=args.vertical_accuracy,
        edit_photo=not args.skip_photo_edit
    )

    if args.odm_geo:
        logging.info('Saving image locations in %s' % args.odm_geo)
        if args.epsg_code is not None:
            epsg_code = args.epsg_code
        else:
            epsg_code = crs_epsg_code(track_coords)
        csr_transfo = crs_transformer_deg_epsg(epsg_code)
        with open(args.odm_geo, 'w') as fd_geo:
            fd_geo.write('EPSG:%s\n' % epsg_code)
            for c in photo_coords.points:
                (x, y) = csr_transfo.transform(c.lon, c.lat)
                horiz_accuracy = c.horiz_accuracy
                if horiz_accuracy is None:
                    horiz_accuracy = 0
                vert_accuracy = c.vert_accuracy
                if vert_accuracy is None:
                    vert_accuracy = 0
                line = '%s\t%.10f\t%.10f\t%.3f\t0\t0\t0\t%.3f\t%.3f\n' % (
                    c.label,
                    x,
                    y,
                    c.elevation,
                    horiz_accuracy,
                    vert_accuracy
                )
                fd_geo.write(line)

    if getattr(args, 'report_track') is not None:
        logging.info('Saving track %s' % getattr(args, 'report_track'))
        report_image_coordinates_collections(track_coords, getattr(args, 'report_track'), 1000)
    if getattr(args, 'report_photo_locations') is not None:
        report_image_coordinates_collections(photo_coords, getattr(args, 'report_photo_locations'), 1000)


if __name__ == '__main__':
    main()
