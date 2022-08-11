from unittest import TestCase

from coordinates_label_photos.coordinates.crs_transformer import crs_wgs84_utm_tile, crs_epsg_code, \
    crs_transformer_deg_utm
from coordinates_label_photos.parsers import coords_parser


class TestCrsTransformation(TestCase):
    filename = 'resources/photo-gps/track.gpx'
    coords_collection = coords_parser(filename)

    def test_epsg(self):
        got = crs_epsg_code(self.coords_collection)

        self.assertEqual('32632', got)

    def test_wgs84_utm_zone(self):
        got = crs_wgs84_utm_tile(self.coords_collection)

        self.assertEqual('WGS84 UTM 32N', got)

    def test_pyproj_transformer_deg_utm_1(self):
        transfo = crs_transformer_deg_utm('22332')
        (got_x, got_y) = transfo.transform(23.13361000, 37.42807200)
        self.assertAlmostEqual(1753779.712, got_x, 2)
        self.assertAlmostEqual(4237153.604, got_y, 2)

    def test_pyproj_transformer_deg_utm_22332(self):
        # ref https://epsg.io/transform#s_srs=4326&t_srs=22332&x=23.1336358&y=37.4280617
        transfo = crs_transformer_deg_utm('22332')
        (got_x, got_y) = transfo.transform(23.1336358, 37.4280617)
        self.assertAlmostEqual(1753697.3216273494, got_x, 2)
        self.assertAlmostEqual(4236984.973854066, got_y, 2)

    def test_pyproj_transformer_deg_utm_32632(self):
        # checked with
        # * https://epsg.io/transform#s_srs=4326&t_srs=22332&x=23.1336358&y=37.4280617
        # * https://mygeodata.cloud/cs2cs/
        transfo = crs_transformer_deg_utm('32632')
        (got_x, got_y) = transfo.transform(23.1336358, 37.4280617)
        self.assertAlmostEqual(1753734.2744281862, got_x, 2)
        self.assertAlmostEqual(4237442.419149317, got_y, 2)
