from datetime import timezone, datetime
from unittest import TestCase

from coordinates_label_photos.parsers import llh_line_parser


class TestParsers(TestCase):
    def test_llh_line_parser(self):
        given = '2022/08/03 07:35:30.600   37.413804352   23.350134190    44.1240   2  11   0.2400   0.2700   0.8700   0.0000   0.0000   0.0000   4.60    0.0'

        got = llh_line_parser(given)

        self.assertEqual(datetime(2022, 8, 3, 7, 35, 30, 600000, tzinfo=timezone.utc), got.timestamp)
        self.assertEqual(37.413804352, got.lat)
        self.assertEqual(23.350134190, got.lon)
        self.assertEqual(44.1240, got.elevation)
