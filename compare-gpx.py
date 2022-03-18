import logging

from gpx import gpx_parser, csv_parser
from reports.coordinates_collection import CoordinatesCollection, report_image_coordinates_collections
import yaml
from yaml import CLoader as Loader

if __name__ == '__main__':
    logging.basicConfig( level=logging.DEBUG)
    config_file = 'config/salvan-parking-20220312.yaml'
    with open(config_file, 'r') as f:
        conf = yaml.load(f.read(), Loader=Loader)
    all_coords = CoordinatesCollection([])
    for e in conf['input']:
        if 'gpx' in e:
            cs = gpx_parser(e['gpx'])
        if 'csv' in e:
            cs = csv_parser(e['csv'])
        cs.label_all(e['name'])
        all_coords.add(cs)
    report_image_coordinates_collections(all_coords, conf['output']['plot'], 1000, color_by_label=True)

