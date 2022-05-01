import logging

from coordinates_label_photos.coordinates import Coordinates
from coordinates_label_photos.coordinates.coordinates_collection import CoordinatesCollection
from PIL import Image, ImageDraw, ImageFont

# From Color Brewer
_color_brewer_set3 = {
    3: ['rgb(141,211,199)', 'rgb(255,255,179)', 'rgb(190,186,218)'],
    4: ['rgb(141,211,199)', 'rgb(255,255,179)', 'rgb(190,186,218)', 'rgb(251,128,114)'],
    5: ['rgb(141,211,199)', 'rgb(255,255,179)', 'rgb(190,186,218)', 'rgb(251,128,114)', 'rgb(128,177,211)'],
    6: ['rgb(141,211,199)', 'rgb(255,255,179)', 'rgb(190,186,218)', 'rgb(251,128,114)', 'rgb(128,177,211)',
        'rgb(253,180,98)'],
    7: ['rgb(141,211,199)', 'rgb(255,255,179)', 'rgb(190,186,218)', 'rgb(251,128,114)', 'rgb(128,177,211)',
        'rgb(253,180,98)', 'rgb(179,222,105)'],
    8: ['rgb(141,211,199)', 'rgb(255,255,179)', 'rgb(190,186,218)', 'rgb(251,128,114)', 'rgb(128,177,211)',
        'rgb(253,180,98)', 'rgb(179,222,105)', 'rgb(252,205,229)'],
    9: ['rgb(141,211,199)', 'rgb(255,255,179)', 'rgb(190,186,218)', 'rgb(251,128,114)', 'rgb(128,177,211)',
        'rgb(253,180,98)', 'rgb(179,222,105)', 'rgb(252,205,229)', 'rgb(217,217,217)'],
    10: ['rgb(141,211,199)', 'rgb(255,255,179)', 'rgb(190,186,218)', 'rgb(251,128,114)', 'rgb(128,177,211)',
         'rgb(253,180,98)', 'rgb(179,222,105)', 'rgb(252,205,229)', 'rgb(217,217,217)', 'rgb(188,128,189)'],
    11: ['rgb(141,211,199)', 'rgb(255,255,179)', 'rgb(190,186,218)', 'rgb(251,128,114)', 'rgb(128,177,211)',
         'rgb(253,180,98)', 'rgb(179,222,105)', 'rgb(252,205,229)', 'rgb(217,217,217)', 'rgb(188,128,189)',
         'rgb(204,235,197)'],
    12: ['rgb(141,211,199)', 'rgb(255,255,179)', 'rgb(190,186,218)', 'rgb(251,128,114)', 'rgb(128,177,211)',
         'rgb(253,180,98)', 'rgb(179,222,105)', 'rgb(252,205,229)', 'rgb(217,217,217)', 'rgb(188,128,189)',
         'rgb(204,235,197)', 'rgb(255,237,111)']
}


def report_image_coordinates_collections(
        coords: CoordinatesCollection,
        filename: str,
        max_dim: int,
        color_by_label: bool = False
):
    logging.info('Saving report in %s' % filename)
    boundaries = coords.lat_lon_boundaries()
    dim_lat = boundaries[1].lat - boundaries[0].lat
    dim_lon = boundaries[1].lon - boundaries[0].lon
    dimensions = coords.dimensions()
    if dimensions[0] > dimensions[1]:
        width = max_dim * 0.8
        height = max_dim * dimensions[1] / dimensions[0]
    else:
        height = max_dim * 0.8
        width = max_dim * dimensions[1] / dimensions[0]

    margin = max_dim * 0.1

    img = Image.new('RGB', (int(width + 2 * margin), int(height + 2 * margin)), 'white')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('/System/Library/Fonts/Geneva.ttf', size=12)

    if color_by_label:
        labels = {c.label for c in coords.points}
        if len(labels) > 12:
            raise Exception('Too many labels (%d) or not enough colors' % len(labels))
        color_scale = _color_brewer_set3.get(max(len(labels), 3))
        colors = {}
        for i, l in enumerate(labels):
            colors[l] = color_scale[i]
            draw.text((30, 20 + 20 * i - 10), l, fill='black', font=font)
            draw.ellipse((15, 20 + 20 * i - 5, 25, 20 + 20 * i + 5), fill=color_scale[i])

        def color(c: Coordinates):
            return colors[c.label]
    else:
        def color(c: Coordinates):
            return 'red'

    prev = None
    for c in coords.points:
        y = margin + int((c.lat - boundaries[0].lat) / dim_lat * height)
        x = margin + int((c.lon - boundaries[0].lon) / dim_lon * width)
        if not color_by_label and c.label is not None:
            draw.text((x + 4, y + 4), c.label, fill='black', font=font)
        draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill=color(c))

        if color_by_label and prev is not None and prev['label'] == c.label:
            draw.line([(x, y), (prev['x'], prev['y'])], fill='grey')
        prev = {
            'label': c.label,
            'x': x,
            'y': y,
        }

    img.save(filename)
