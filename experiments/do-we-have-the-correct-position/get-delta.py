import csv

from coordinates_label_photos.coordinates.crs_transformer import crs_transformer_deg_epsg
from coordinates_label_photos.parsers import coords_parser
from coordinates_label_photos.photos import list_photo_filenames, calibrate_photo

# 18s for the GPS time + 0.88s for the delay between the EXIF time and the time the image was actually taken
time_shift = 18 + 0.88

# the camera is not right under the GPS, but, with the fixing system, 7cm north
camera_shift = 0.07


def read_csv(file_name):
    with open(file_name, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)


def get_0_position():
    rows = read_csv('measures/emlid-0-positions.csv')
    eastings = [float(row['Easting']) for row in rows]
    northings = [float(row['Northing']) for row in rows]

    avg_easting = sum(eastings) / len(eastings)
    avg_nothing = sum(northings) / len(northings)
    std_easting = (sum([(e - avg_easting) ** 2 for e in eastings]) / len(eastings)) ** 0.5
    std_northings = (sum([(n - avg_nothing) ** 2 for n in northings]) / len(northings)) ** 0.5
    return avg_easting, avg_nothing, std_easting, std_northings


def get_image_estimated_positions():
    rows = read_csv('measures/image-estimated-positions.csv')
    return {
        row['name']: float(row['dy'])
        for row in rows
    }


def get_image_computed_positions():
    with open('results/images-computed-positions.csv', 'r') as f:
        f.readline()
        rows = [line.split('\t') for line in f.readlines()]
        return {
            row[0]: {
                'easting': float(row[1]),
                'northing': float(row[2]),
            }
            for row in rows
        }


def std_deviation(values):
    avg = sum(values) / len(values)
    avg_abs=sum([abs(x) for x in values])/ len(values)
    return avg_abs, (sum([(v - avg) ** 2 for v in values]) / len(values)) ** 0.5


def print_delta_direct_call(track_coords, delta_ts):
    avg_easting, avg_northing, std_easting, std_northings = get_0_position()

    photos = list_photo_filenames('measures/images/*.JPG')

    photo_coords = calibrate_photo(
        photos=photos,
        track_coords=track_coords,
        photo_timezone_offset='+03:00',
        photo_timestamp_correction=time_shift+ delta_ts,
        camera_fixed_elevation=0,
        horizontal_accuracy=0,
        vertical_accuracy=0,
        edit_photo=False
    )
    photo_coords.points.sort(key=lambda p: p.label)
    estimated_positions = get_image_estimated_positions()

    csr_transfo = crs_transformer_deg_epsg('32634')
    dys = []
    for photo_coords in photo_coords.points:
        name = photo_coords.label
        computed_easting, computed_northing = csr_transfo.transform(photo_coords.lon, photo_coords.lat)
        # print(photo_coords)
        computed_delta = computed_northing + camera_shift - avg_northing
        dys.append(computed_delta - estimated_positions[name])

    avg, stdev = std_deviation(dys)
    print('%.3f %.3f %.3f' % (delta_ts, avg, stdev))


if __name__ == '__main__':
    avg_easting, avg_northing, std_easting, std_northings = get_0_position()
    print('avg easting/northing (stddev): %f (%f), %f (%f)' % (avg_easting, std_easting, avg_northing, std_northings))

    computed_positions = list(get_image_computed_positions().items())
    computed_positions.sort(key=lambda p: p[0])
    # name = 'G0272871.JPG'
    # photos = list_photo_filenames('measures/images/%s' % name)
    track_coords = coords_parser('measures/emlid-localhost_solution_20230812112902.LLH')

    estimated_positions = get_image_estimated_positions()

    print('name\tcomputedNorthing\tcomputedPosition\tMeasuredPosition\tdelta')
    for computed_position in computed_positions:
        name = computed_position[0]
        computed_easting, computed_northing = computed_position[1]['easting'], computed_position[1]['northing']
        # print(photo_coords)
        computed_delta = computed_northing + camera_shift - avg_northing
        print('%s\t%.3f\t%.3f\t%.3f\t%.3f' % (
            name,
            computed_northing,
            computed_delta,
            estimated_positions[name],
            computed_delta - estimated_positions[name])
              )

    print('time shift error error abs average error stddev')
    for ts in [-2, -1, -0.5, -0.25, -0.1, 0, 0.1, 0.25, 0.5, 1, 2]:
        print_delta_direct_call(track_coords, ts)

