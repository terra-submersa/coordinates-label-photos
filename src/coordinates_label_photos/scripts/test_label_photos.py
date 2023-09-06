import unittest

from coordinates_label_photos.coordinates import Coordinates
from coordinates_label_photos.parsers import coords_parser
from coordinates_label_photos.photos import get_photo_timestamp


class TestLabelPhoto(unittest.TestCase):
    photo_filename = 'resources/photo-gps-timing/G0160150-tile-11.JPG'
    photo_timestamp = get_photo_timestamp(
        photo_filename,
        timezone_offset='+0300',
        timestamp_correction=-74.5
    )
    tile_coords = Coordinates(
        lon=23.13363763,
        lat=37.42803984
    )

    def test_photo_should_be_above_tile_11_pos(self):
        """
        We use a picture and correct the time with time zone + gopro offset.
        The returned position should correspond to the measured tile.
        """
        track_coords = coords_parser('resources/photo-gps-timing/ts_reach_ro.pos')

        photo_coords = track_coords.interpolate_position(self.photo_timestamp)

        got_dist = photo_coords.distance(self.tile_coords)
        self.assertLessEqual(got_dist, 1)

    #
    # def test_photo_should_be_above_tile_11_llh(self):
    #     """
    #     We use a picture and correct the time with time zone + gopro offset.
    #     The returned position should correspond to the measured tile.
    #     """
    #     track_coords = coords_parser('resources/photo-gps-timing/ts_reach_ro.LLH')
    #
    #     photo_coords = track_coords.interpolate_position(self.photo_timestamp)
    #
    #     got_dist = photo_coords.distance(self.tile_coords)
    #     self.assertLessEqual(got_dist, 1)
