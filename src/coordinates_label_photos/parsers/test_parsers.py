from datetime import timezone, datetime
from unittest import TestCase

from coordinates_label_photos.parsers import emlid_fwf_line_parser


class TestParsers(TestCase):
    def test_emlid_llh_line_parser(self):
        given = '2022/08/03 07:35:30.600   37.413804352   23.350134190    44.1240   2  11   0.2400   ' \
                '0.2700   0.8700   0.0000   0.0000   0.0000   4.60    0.0'

        got = emlid_fwf_line_parser(given)

        self.assertEqual(datetime(2022, 8, 3, 7, 35, 30, 600000, tzinfo=timezone.utc), got.timestamp)
        self.assertEqual(37.413804352, got.lat)
        self.assertEqual(23.350134190, got.lon)
        self.assertEqual(44.1240, got.elevation)

    def test_pos_line_parser(self):
        given = '2022/08/08 05:24:20.200   37.428194740   23.134118977    39.6114   2  16   0.8445   0.6919   ' \
                '2.4424  -0.1155   0.5825   0.8769   0.00    0.0'

        got = emlid_fwf_line_parser(given)

        self.assertEqual(datetime(2022, 8, 8, 5, 24, 20, 200000, tzinfo=timezone.utc), got.timestamp)
        self.assertEqual(37.428194740, got.lat)
        self.assertEqual(23.134118977, got.lon)
        self.assertEqual(39.6114, got.elevation)
        self.assertAlmostEqual(1.65522, got.horiz_accuracy, 8)
        self.assertAlmostEqual(4.787104, got.vert_accuracy, 8)
