from . import to_abs_deg_min_sec, Coordinates
from unittest import TestCase


class TestCoordinates(TestCase):
    coords = Coordinates(-12.34567, 98.7654)

    def test_to_abs_deg_min_sec(self):
        got = to_abs_deg_min_sec(self.coords.lat)

        self.assertEqual(got, (12, 20, 44.412))

    def test_exiv_lat(self):
        self.assertEqual('S', self.coords.lat_dir())
        self.assertEqual([(12, 1), (20, 1), (11103, 250)], self.coords.exiv_lat())

    def test_exiv_lon(self):
        self.assertEqual('W', self.coords.lon_dir())
        self.assertEqual([(98, 1), (45, 1), (1386, 25)], self.coords.exiv_lon())

    def test_distance(self):
        c1 = Coordinates(52.2296756, 21.0122287)
        c2 = Coordinates(52.406374, 16.9251681)

        got = c1.distance(c2)

        self.assertAlmostEqual(279352.9, got, 1)
