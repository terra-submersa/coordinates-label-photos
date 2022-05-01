from datetime import datetime
from fractions import Fraction

from piexif import GPSIFD, ImageIFD
import geopy.distance


class Coordinates:
    lat: float
    lon: float
    elevation: float
    timestamp: datetime
    label: str

    def __init__(self,
                 lat: float,
                 lon: float,
                 elevation: float = None,
                 timestamp: datetime = None,
                 label: str = None
                 ):
        self.lat = lat
        self.lon = lon
        self.elevation = elevation
        self.timestamp = timestamp
        self.label = label

    def distance(self, other):
        return geopy.distance.distance(
            (self.lat, self.lon),
            (other.lat, other.lon),
            ellipsoid='WGS-84'
        ).m

    def __repr__(self):
        return '(%f, %f, %s) %s %s' % (self.lat, self.lon, self.elevation, self.label, self.timestamp)

    def exif_gps(self):
        return {
            GPSIFD.GPSVersionID: (2, 0, 0, 0),
            GPSIFD.GPSAltitudeRef: 1,
            GPSIFD.GPSAltitude: _to_rational(self.elevation),
            GPSIFD.GPSDateStamp: u"2021:08:10 10:55:55",
            GPSIFD.GPSLatitudeRef: self.lat_dir(),
            GPSIFD.GPSLatitude: self.exiv_lat(),
            GPSIFD.GPSLongitudeRef: self.lon_dir(),
            GPSIFD.GPSLongitude: self.exiv_lon(),
        }

    def exiv_lat(self):
        return [_to_rational(x) for x in to_abs_deg_min_sec(self.lat)]

    def exiv_lon(self):
        return [_to_rational(x) for x in to_abs_deg_min_sec(self.lon)]

    def lat_dir(self) -> str:
        if self.lat > 0:
            return 'N'
        else:
            if self.lat < 0:
                return 'S'
            else:
                return ''

    def lon_dir(self) -> str:
        if self.lat > 0:
            return 'E'
        else:
            if self.lat < 0:
                return 'W'
            else:
                return ''


def _to_rational(number: float):
    """
    returns a numerator,denominator pair
    """
    f = Fraction(str(number))
    return f.numerator, f.denominator


def to_abs_deg_min_sec(value):
    """
    return the value to the absolute value in degree, minute, seconds
    """
    abs_value = abs(value)
    degrees = int(abs_value)
    rem = (abs_value - degrees) * 60
    minutes = int(rem)
    seconds = round((rem - minutes) * 60, 5)
    return degrees, minutes, seconds


def get_decimal_from_dms(dms, ref):
    """From https://developer.here.com/blog/getting-started-with-geocoding-exif-image-metadata-in-python3"""
    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)


def exif_to_coordinates(exif) -> Coordinates:
    if 'GPS' not in exif:
        raise Exception('not "GPS" tag in exif image')

    exif_gps = exif['GPS']
    lat = get_decimal_from_dms(exif_gps[GPSIFD.GPSLatitude], exif_gps[GPSIFD.GPSLatitudeRef].decode('utf-8'))
    lon = get_decimal_from_dms(exif_gps[GPSIFD.GPSLongitude], exif_gps[GPSIFD.GPSLongitudeRef].decode('utf-8'))
    elev = round(exif_gps[GPSIFD.GPSAltitude][0] / exif_gps[GPSIFD.GPSAltitude][1], 2)

    timestamp = datetime.strptime(exif['0th'][ImageIFD.DateTime].decode('utf-8'), '%Y:%m:%d %H:%M:%S')

    return Coordinates(
        lat=lat,
        lon=lon,
        elevation=elev,
        timestamp=timestamp,
    )
