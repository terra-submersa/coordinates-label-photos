import glob

from coordinates_label_photos.photos import get_photo_timestamp

if __name__ == '__main__':
    ls = glob.glob('measures/images/*.JPG')
    print(ls)
    for f in ls:
        print('%s\t%s' % (f, get_photo_timestamp(f, timezone_offset='+03:00')))
