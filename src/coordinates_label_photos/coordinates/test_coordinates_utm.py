from unittest import TestCase

from coordinates_label_photos.coordinates import Coordinates
from coordinates_label_photos.coordinates.coordinates_utm import utm_from_coordinates


class TestCoordinatesUTM(TestCase):
    def test_utm_from_coordinates(self):
        given = Coordinates(
            lat=37 + 22.2814 / 60,
            lon=23 + 13.1628 / 60
        )
        got = utm_from_coordinates(given)

        self.assertEqual(34, got.zone_number)
        self.assertEqual('S', got.zone_letter)
        self.assertAlmostEquals(696520.2662, got.easting, places=4)
        self.assertAlmostEquals(4138380.38, got.northing, places=4)

    def test_utm_from_coordinates_2(self):
        # cross check TestCrsTransformation.test_pyproj_transformer_deg_utm_32632_34N
        given = Coordinates(
            lat=37.4280617,
            lon=23.1336358
        )
        got = utm_from_coordinates(given)

        self.assertEqual(34, got.zone_number)
        self.assertEqual('S', got.zone_letter)
        self.assertAlmostEquals(688784.5156771592, got.easting, places=2)
        self.assertAlmostEquals(4144497.2610669266, got.northing, places=2)
