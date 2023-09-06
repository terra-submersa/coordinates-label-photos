from datetime import datetime, timezone, timedelta
from unittest import TestCase

from coordinates_label_photos.photos import get_photo_timestamp


class TestPhoto(TestCase):
    def test_get_photo_timestamp(self):
        # BTW, the picture shows a watch displaying 11:29:10, but the EXIF tag is 11:29:11
        got = get_photo_timestamp('resources/photo-gps/IMG_4967.jpeg')

        self.assertEqual(datetime(2022, 3, 6, 10, 29, 11, 880000, tzinfo=timezone.utc), got)

    def test_get_photo_timestamp_correction(self):
        # recorded EXIF data: 2022-08-08 09:36:13.145000+00:00
        # TZ +0300
        # GoPro clock running 74.3 seconds to early
        print(get_photo_timestamp(
            'resources/photo-gps-timing/G0160150-tile-11.JPG'
        ))
        got = get_photo_timestamp(
            'resources/photo-gps-timing/G0160150-tile-11.JPG',
            timezone_offset='+0300',
            timestamp_correction=-74.3
        )

        got_delta = datetime(2022, 8, 8, 6, 34, 58, 700000 + 145000, tzinfo=timezone.utc) - got
        self.assertEqual(timedelta(seconds=0), got_delta)
