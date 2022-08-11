from pyproj import CRS, Transformer, crs, Geod, Proj
from pyproj.aoi import AreaOfInterest
from pyproj.database import query_utm_crs_info

from coordinates_label_photos.coordinates.coordinates_collection import CoordinatesCollection


def crs_epsg_code(coords: CoordinatesCollection) -> str:
    (nw, se) = coords.lat_lon_boundaries()
    utm_crs_list = query_utm_crs_info(
        datum_name="WGS 84",
        area_of_interest=AreaOfInterest(
            west_lon_degree=nw.lon,
            south_lat_degree=se.lat,
            east_lon_degree=se.lon,
            north_lat_degree=nw.lat,
        ),
    )
    return utm_crs_list[0].code


def crs_wgs84_utm_tile(coords: CoordinatesCollection):
    """

    :param coords:
    :type coords:
    :return:
    :rtype:
    """
    name = CRS.from_epsg(crs_epsg_code(coords)).name
    return name.replace('WGS 84 / UTM zone ', 'WGS84 UTM ')


def crs_transformer_deg_utm(epsg_code: str) -> Transformer:
    """
    From a given coords collection, gives the transformation function long/lat -> x/y
    :param epsg_code: the area EPSG code
    :type epsg_code: str
    :return: a pyproj transformer object
    :rtype: pyproj.Transformer
    """
    crs_latlon = CRS.from_epsg('4326') # WGS84
    crs = CRS.from_epsg(epsg_code)
    return Transformer.from_crs(crs_latlon.geodetic_crs, crs, always_xy=True)
