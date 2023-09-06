import glob
import os

import piexif
from datetime import datetime, timedelta

from tqdm import tqdm

from coordinates_label_photos.coordinates.coordinates_collection import CoordinatesCollection


def list_photo_filenames(directory: str) -> 'list[str]':
    ls = glob.glob(directory)
    ls.extend(glob.glob('%s/*.jpeg' % directory))
    ls.extend(glob.glob('%s/*.jpg' % directory))
    ls.extend(glob.glob('%s/*.JPEG' % directory))
    ls.extend(glob.glob('%s/*.JPG' % directory))
    return ls


def get_photo_timestamp(
        filename: str,
        timezone_offset: str = None,
        timestamp_correction:float = None
    ) -> datetime:
    """
    ¨¨Get the timestamp from the EXIF data stored in the photo under filename.
    Add the millisecond timestamp if you have installed the GoPro Lab plugin https://gopro.github.io/labs/control/precisiontime/.
    :param filename:
    :type filename: str
    :param timezone_offset: set the photo time zone delta (format '+2:00') in case the picture is not annotated (no GPS signal)
    :type timezone_offset: str
    :param timestamp_correction: an eventual number of seconds to substracte to the recorder time stamp.
    :type timestamp_correction: float
    :rtype: datetime
    """
    exif_dict = get_photo_exif(filename)
    time = exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal].decode("utf-8")
    if piexif.ExifIFD.OffsetTimeOriginal not in exif_dict['Exif']:
        if timezone_offset is None:
            time_offset = '+0000'
        else:
            time_offset = timezone_offset
    else:
        time_offset = exif_dict['Exif'][piexif.ExifIFD.OffsetTimeOriginal].decode("utf-8")

    dt =  datetime.strptime(time + ' ' + time_offset, '%Y:%m:%d %H:%M:%S %z')
    if ('Exif' in exif_dict) and piexif.ExifIFD.SubSecTime in exif_dict['Exif']:
        sub_sec_time=float(exif_dict['Exif'][piexif.ExifIFD.SubSecTime].decode("utf-8"))
        dt = dt + timedelta(seconds=sub_sec_time/1000)

    if timestamp_correction is not None:
        dt = dt + timedelta(seconds=timestamp_correction)
    return dt


def calibrate_photo(
        photos: 'list[str]',
        track_coords: CoordinatesCollection,
        photo_timezone_offset: str = None,
        photo_timestamp_correction: float = None,
        camera_fixed_elevation: float = None,
        horizontal_accuracy: float = None,
        vertical_accuracy: float = None,
        edit_photo: bool = True
) -> CoordinatesCollection:
    photo_coords = []
    for p in tqdm(photos, desc="Calibrating photos"):
        timestamp = get_photo_timestamp(p, photo_timezone_offset, photo_timestamp_correction)
        # print('Photo %s taken at %s' % (p, timestamp))
        coords = track_coords.interpolate_position(timestamp)

        if camera_fixed_elevation is not None:
            coords.elevation = camera_fixed_elevation
        if horizontal_accuracy is not None:
            coords.horiz_accuracy = horizontal_accuracy
        if vertical_accuracy is not None:
            coords.vert_accuracy = vertical_accuracy

        if edit_photo:
            set_photo_exif(filename=p, ifd='GPS', data=coords.exif_gps())
        # print('Saved: %s\t%s' % (p, coords))
        coords.label = os.path.basename(p)
        photo_coords.append(coords)
    return CoordinatesCollection(photo_coords)


def set_photo_exif(filename: str, ifd: str, data: dict):
    exif_dict = get_photo_exif(filename)
    exif_dict[ifd] = data
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, filename)


def clear_photo_exif(filename: str, ifd: str):
    """
    Removes a whole IFD branch from the exif and saves the file back
    :param filename: the image location
    :type filename: str
    :param ifd: the key of the sub IFD map
    :type ifd: str
    """
    exif_dict = get_photo_exif(filename)
    del exif_dict[ifd]
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, filename)


def get_photo_exif(filename: str):
    return piexif.load(filename)
