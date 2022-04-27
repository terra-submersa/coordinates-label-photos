from datetime import datetime, timezone
from unittest import TestCase

from coordinates_label_photos.coordinates import Coordinates
from coordinates_label_photos.gpx import gpx_parser


class TestCoordinatesCollection(TestCase):
    filename = 'resources/photo-gps/track.gpx'
    coords_collection = gpx_parser(filename)

    def test_start_time(self):
        got = self.coords_collection.start_time()
        self.assertEqual(datetime(2022, 3, 6, 10, 28, 49, tzinfo=timezone.utc), got)

    def test_end_time(self):
        got = self.coords_collection.end_time()
        self.assertEqual(datetime(2022, 3, 6, 10, 30, 13, tzinfo=timezone.utc), got)

    def test_interpolate_position_before(self):
        timestamp = datetime(2022, 3, 6, 10, 28, 0, tzinfo=timezone.utc)

        got = self.coords_collection.interpolate_position(timestamp)

        self.assertEqual(None, got)

    def test_interpolate_position_after(self):
        timestamp = datetime(2022, 3, 6, 10, 31, 0, tzinfo=timezone.utc)

        got = self.coords_collection.interpolate_position(timestamp)

        self.assertEqual(None, got)

    def test_interpolate_position_exact(self):
        timestamp = datetime(2022, 3, 6, 10, 30, 9, tzinfo=timezone.utc)

        got = self.coords_collection.interpolate_position(timestamp)

        expected = Coordinates(
            lat=46.119549,
            lon=7.021491,
            elevation=938.0,
            timestamp=timestamp
        )

        self.assertAlmostEqual(expected.lat, got.lat, 6)
        self.assertAlmostEqual(expected.lon, got.lon, 6)
        self.assertAlmostEqual(expected.elevation, got.elevation, 6)

        self.assertEqual(timestamp, got.timestamp)

    def test_interpolate_position_middle(self):
        timestamp = datetime(2022, 3, 6, 10, 30, 9, microsecond=250000, tzinfo=timezone.utc)
        got = self.coords_collection.interpolate_position(timestamp)

        expected = Coordinates(
            lat=46.119548,
            lon=7.021491,
            elevation=938.0,
            timestamp=timestamp
        )

        self.assertAlmostEqual(expected.lat, got.lat, 6)
        self.assertAlmostEqual(expected.lon, got.lon, 6)
        self.assertAlmostEqual(expected.elevation, got.elevation, 6)

        self.assertEqual(timestamp, got.timestamp)

    def test_lat_lon_boundaries(self):
        got = self.coords_collection.lat_lon_boundaries()

        self.assertEqual(46.11961992457509, got[0].lat)
        self.assertEqual(7.021400593221188, got[0].lon)
        self.assertEqual(46.11953526735306, got[1].lat)
        self.assertEqual(7.021564207971096, got[1].lon)
