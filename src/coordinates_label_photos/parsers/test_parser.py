from datetime import datetime, timezone
from unittest import TestCase

from coordinates_label_photos.parsers import coords_parser


class TestParser(TestCase):
    def test_emlid_pos_parser(self):
        coords = coords_parser('resources/photo-gps-timing/ts_reach_ro.pos')

        got_timestamp = coords.start_time()
        self.assertEqual(datetime(2022, 8, 8, 6, 33, 42, tzinfo=timezone.utc), got_timestamp)

    def test_emlid_llh_parser(self):
        coords = coords_parser('resources/photo-gps-timing/ts_reach_ro.LLH')

        got_timestamp = coords.start_time()
        self.assertEqual(datetime(2022, 8, 8, 6, 34, 0, tzinfo=timezone.utc), got_timestamp)

