import logging

from gpx import gpx_parser
from photos import list_photo_filenames, get_photo_timestamp, set_photo_exif, calibrate_photo
from reports.coordinates_collection import report_image_coordinates_collections
import yaml
from yaml import CLoader as Loader

if __name__ == '__main__':
    logging.basicConfig( level=logging.DEBUG)
    config_file = 'config/salvan-wall-20220312-gpsmap86i.yaml'
    #config_file = 'config/salvan-wall-20220312-fenix5.yaml'
    with open(config_file, 'r') as f:
        conf = yaml.load(f.read(), Loader=Loader)
    photos = list_photo_filenames(conf['input']['image_directory'])
    track_coords = gpx_parser(conf['input']['gpx'])
    photo_coords = calibrate_photo(photos=photos, track_coords=track_coords)
    report_image_coordinates_collections(photo_coords, conf['output']['photo_position_plot'], 1000)
    report_image_coordinates_collections(track_coords, conf['output']['track_plot'], 1000)
