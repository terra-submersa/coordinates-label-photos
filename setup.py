from setuptools import setup

setup(
    entry_points={
        'console_scripts': [
            'coordinates-label-photos=coordinates_label_photos.scripts.label_photos:main',
            'coordinates-clear-photos=coordinates_label_photos.scripts.clear_photo_coords:main',
            'plot-coords-tracks=coordinates_label_photos.scripts.plot_coords_tracks:main',
            'images-to-gpx=coordinates_label_photos.scripts.images_to_gpx:main',
            'select-closest-photos=coordinates_label_photos.scripts.select_closest_photos:main',
        ],
    }
)
