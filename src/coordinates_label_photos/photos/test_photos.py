from datetime import datetime, timezone
from unittest import TestCase

from coordinates_label_photos.photos import get_photo_timestamp


class TestPhoto(TestCase):
    def test_get_photo_timestamp(self):
        # BTW, the picture shows a watch displaying 11:29:10, but the EXIF tag is 11:29:11
        got = get_photo_timestamp('resources/photo-gps/IMG_4967.jpeg')

        self.assertEqual(datetime(2022, 3, 6, 10, 29, 11, tzinfo=timezone.utc), got)
