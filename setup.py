from setuptools import setup

setup(
    entry_points={
        'console_scripts': [
            'coordinates-label-photos=coordinates_label_photos.scripts.label_photos:main',
            'plot-gpx-tracks=coordinates_label_photos.scripts.plot_gpx_tracks:main',
        ],
    }
)
