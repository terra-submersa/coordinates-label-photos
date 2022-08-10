import glob
import os

import piexif
from datetime import datetime

from tqdm import tqdm

from coordinates_label_photos.coordinates.coordinates_collection import CoordinatesCollection


def list_photo_filenames(directory: str) -> 'list[str]':
    ls = glob.glob('%s/*.jpeg' % directory)
    ls.extend(glob.glob('%s/*.jpg' % directory))
    ls.extend(glob.glob('%s/*.JPEG' % directory))
    ls.extend(glob.glob('%s/*.JPG' % directory))
    return ls


def get_photo_timestamp(filename: str, default_time_offset: str = None) -> datetime:
    """
    ¨¨Get the timestamp from the EXIF data stored in the photo under filename
    :param filename:
    :type filename: str
    :param default_time_offset: set the photo time zone delta (format '+2:00') in case the picture is not annotated (no GPS signal)
    :type default_time_offset: str
    :rtype: datetime
    """
    exif_dict = get_photo_exif(filename)
    time = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal].decode("utf-8")
    if piexif.ExifIFD.OffsetTimeOriginal not in exif_dict['Exif']:
        if default_time_offset is None:
            time_offset = '+0000'
        else:
            time_offset = default_time_offset
    else:
        time_offset = exif_dict['Exif'][piexif.ExifIFD.OffsetTimeOriginal].decode("utf-8")

    return datetime.strptime(time + ' ' + time_offset, '%Y:%m:%d %H:%M:%S %z')


def calibrate_photo(photos: 'list[str]', track_coords: CoordinatesCollection,
                    default_time_offset: str) -> CoordinatesCollection:
    photo_coords = []
    for p in tqdm(photos, desc="Calibrating photos"):
        timestamp = get_photo_timestamp(p, default_time_offset)
        coords = track_coords.interpolate_position(timestamp)
        set_photo_exif(filename=p, ifd='GPS', data=coords.exif_gps())
        # print('Saved: %s\t%s' % (p, coords))
        coords.label = os.path.splitext(os.path.basename(p))[0]
        photo_coords.append(coords)
    return CoordinatesCollection(photo_coords)


def set_photo_exif(filename: str, ifd: str, data: dict):
    exif_dict = get_photo_exif(filename)
    exif_dict[ifd] = data
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, filename)


def get_photo_exif(filename: str):
    return piexif.load(filename)