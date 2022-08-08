import csv
import logging
from datetime import datetime, timezone

import gpxpy as gpxpy
import os

from coordinates_label_photos.coordinates import Coordinates
from coordinates_label_photos.coordinates.coordinates_collection import CoordinatesCollection

class NoParserForCoordinateFormatError:
    def __init__(self, extension: str):
        self.extension  = extension

    def __str__(self):
        return 'No parser is available for %s among %s'%(self.extension, ['.llh', '.gpx'])

def coords_parser(filename) -> CoordinatesCollection:
    logging.info('Loading coordinates track from %s' % filename)
    _, file_extension = os.path.splitext(filename)
    file_extension = file_extension.lower()
    if file_extension == '.gpx':
        return gpx_parser(filename)
    else:
        if file_extension == '.llh':
            return llh_parser(filename)
        else:
            raise NoParserForCoordinateFormatError(file_extension)



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

def llh_parser(filename) -> CoordinatesCollection:
    logging.info('Loading LLH from %s' % filename)
    with open (filename) as fd:
        coords = []
        for line in fd.readlines():
            c = llh_line_parser(line)
            coords.append(c)
        return CoordinatesCollection(coords)

def llh_line_parser(line:str) -> Coordinates:
    timestamp = datetime.strptime(line[0:23]+'000', '%Y/%m/%d %H:%M:%S.%f').replace(tzinfo = timezone.utc)
    lat = float( line[25:38])
    lon = float( line[39:53])
    elev = float( line[55:64])
    return  Coordinates(
        lat= lat,
        lon = lon,
        elevation = elev,
        timestamp = timestamp
    )
