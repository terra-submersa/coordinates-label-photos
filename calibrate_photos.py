from gpx import gpx_parser
from photos import list_photo_filenames, get_photo_timestamp, set_photo_exif, calibrate_photo
from reports.coordinates_collection import report_image_coordinates_collections

if __name__ == '__main__':
    directory = '/tmp/photo-gps'
    photos = list_photo_filenames(directory)
    track_coords = gpx_parser('%s/track.gpx' % directory)
    photo_coords = calibrate_photo(photos=photos, track_coords=track_coords)
    report_image_coordinates_collections(photo_coords, '/tmp/photo-positions.jpeg', 1000)
    report_image_coordinates_collections(track_coords, '/tmp/track-positions.jpeg', 1000)


