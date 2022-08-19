import utm

from coordinates_label_photos.coordinates import Coordinates


class CoordinatesUTM:
    easting: float
    northing: float
    zone_number: int
    zone_letter: str

    def __init__(self,
                 easting: float,
                 northing: float,
                 zone_number: int,
                 zone_letter: str,
                 ):
        self.easting = easting
        self.northing = northing
        self.zone_number = zone_number
        self.zone_letter = zone_letter

    def zone(self):
        return '%d%s' % (self.zone_number, self.zone_letter)


def utm_from_coordinates(c: Coordinates) -> CoordinatesUTM:
    (e, n, zn, zl) = utm.from_latlon(c.lat, c.lon)
    return CoordinatesUTM(
        easting=e,
        northing=n,
        zone_number=zn,
        zone_letter=zl
    )


class IncompatibleUTMZoneError(BaseException):
    c1: CoordinatesUTM
    c2: CoordinatesUTM

    def __init__(self, c1: CoordinatesUTM, c2: CoordinatesUTM):
        self.super().__init__()
        self.c1 = c1
        self.c2 = c2

    def __str__(self):
        return 'Incompatible UTM Zone error: %d%s/%d%s' % (
            self.c1.zone_number,
            self.c1.zone_letter,
            self.c2.zone_number,
            self.c2.zone_letter
        )
