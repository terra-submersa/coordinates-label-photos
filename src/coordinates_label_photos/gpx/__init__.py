import csv
import logging

import gpxpy as gpxpy

from coordinates_label_photos.coordinates import Coordinates
from coordinates_label_photos.coordinates.coordinates_collection import CoordinatesCollection


def gpx_parser(filename) -> CoordinatesCollection:
    logging.info('Loading GPX track from %s' % filename)
    with open(filename) as fd:
        gpx = gpxpy.parse(fd)

        coords = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    coords.append(Coordinates(
                        lat=point.latitude,
                        lon=point.longitude,
                        elevation=point.elevation,
                        timestamp=point.time
                    ))
        collect = CoordinatesCollection(coords)
        logging.info('Loaded GPX with %d track points between %s and %s' % (
            len(collect), collect.start_time(), collect.end_time()))
        return collect


def csv_parser(filename) -> CoordinatesCollection:
    logging.info('Loading CSV track from %s' % filename)
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        coords = []

        for row in reader:
            coords.append(
                Coordinates(
                    lat=float(row['latitude_decimal_degree']),
                    lon=float(row['longitude_decimal_degree']),
                    elevation=float(row['ellipsoidal_height_m']),
                    timestamp=None,
                )
            )
        collect = CoordinatesCollection(coords)
        logging.info('Loaded CSV with %d track points between %s and %s' % (
            len(collect), collect.start_time(), collect.end_time()))
        return collect
