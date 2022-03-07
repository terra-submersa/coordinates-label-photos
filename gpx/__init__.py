import gpxpy as gpxpy
from coordinates import Coordinates
from coordinates.coordinates_collection import CoordinatesCollection


def gpx_parser(filename) -> CoordinatesCollection:
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
        return CoordinatesCollection(coords)
