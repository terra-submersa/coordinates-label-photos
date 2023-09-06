
from coordinates_label_photos.coordinates.crs_transformer import crs_transformer_deg_epsg
from coordinates_label_photos.parsers import coords_parser

if __name__ == '__main__':
    file_in = 'measures/emlid-localhost_solution_20230812112902.LLH'
    coords = coords_parser(file_in)
    transfo = crs_transformer_deg_epsg('32634')
    for c in coords.points:
        (x, y) = transfo.transform(c.lon, c.lat)
        print('%s,%f,%f,%f,%f' % (c.timestamp,c.lon, c.lat, x, y))
