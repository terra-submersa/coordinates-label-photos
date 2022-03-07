from coordinates.coordinates_collection import CoordinatesCollection
from PIL import Image, ImageDraw, ImageFont


def report_image_coordinates_collections(
        coords: CoordinatesCollection,
        filename: str,
        max_dim: int
):
    boundaries = coords.lat_lon_boundaries()
    dim_lat = boundaries[1].lat - boundaries[0].lat
    dim_lon = boundaries[0].lon - boundaries[1].lon
    dimensions = coords.dimensions()
    print(boundaries)
    print(dimensions)
    if dimensions[0] > dimensions[1]:
        width = max_dim * 0.8
        height = max_dim * dimensions[1] / dimensions[0]
    else:
        height = max_dim * 0.8
        width = max_dim * dimensions[1] / dimensions[0]

    margin = max_dim * 0.1

    img = Image.new('RGB', (int(width + 2 * margin), int(height + 2 * margin)), 'white')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('/System/Library/Fonts/Geneva.ttf', size=20)

    for c in coords.points:
        y = margin + int((c.lat - boundaries[0].lat) / dim_lat * height)
        x = margin + int((c.lon - boundaries[1].lon) / dim_lon * width)
        if c.label is not None:
            draw.text((x+4, y+4), c.label, fill='black', font=font)
        draw.ellipse((x-2, y-2, x+2, y+2), fill='red')

    img.save(filename)
