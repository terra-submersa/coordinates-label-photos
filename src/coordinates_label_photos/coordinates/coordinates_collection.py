from datetime import datetime

from coordinates_label_photos.coordinates import Coordinates


class CoordinatesCollection:
    points: 'list[Coordinates]'

    def __init__(self, points: 'list[Coordinates]'):
        self.points = points

    def start_time(self):
        return self.points[0].timestamp

    def end_time(self):
        return self.points[-1].timestamp

    def add(self, other):
        self.points.extend(other.points)

    def __len__(self):
        return len(self.points)

    def interpolate_position(self, timestamp: datetime):
        if timestamp < self.start_time() or timestamp >= self.end_time():
            return None
        bracket = self.__find_bracket(timestamp)
        alpha = (timestamp - bracket[0].timestamp).total_seconds() / (
                bracket[1].timestamp - bracket[0].timestamp).total_seconds()
        return Coordinates(
            lat=self.__interpolate(alpha, bracket[0].lat, bracket[1].lat),
            lon=self.__interpolate(alpha, bracket[0].lon, bracket[1].lon),
            elevation=self.__interpolate(alpha, bracket[0].elevation, bracket[1].elevation),
            timestamp=timestamp
        )

    def lat_lon_boundaries(self):
        """
        :return: the boundaries of the coordinates, upper left and lower right
        :rtype: a pair of Coordinates
        """
        min_lat = min([c.lat for c in self.points])
        min_lon = max([c.lon for c in self.points])
        max_lat = max([c.lat for c in self.points])
        max_lon = min([c.lon for c in self.points])
        return Coordinates(lat=max_lat, lon=max_lon), Coordinates(lat=min_lat, lon=min_lon)

    def dimensions(self):
        """
        :return: the dimensions height x width
        :rtype: a pair of float
        """
        boundaries = self.lat_lon_boundaries()
        return Coordinates(boundaries[0].lat, boundaries[0].lon).distance(
            Coordinates(boundaries[1].lat, boundaries[0].lon)), \
        Coordinates(boundaries[0].lat, boundaries[0].lon).distance(
            Coordinates(boundaries[0].lat, boundaries[1].lon))

    def label_all(self, label: str):
        for p in self.points:
            p.label = label

    @staticmethod
    def __interpolate(alpha, v0, v1):
        return v0 + alpha * (v1 - v0)

    def __find_bracket(self, timestamp: datetime):
        i0 = 0
        i1 = len(self.points) - 1
        while i1 - i0 > 1:
            i_mid = int((i0 + i1) / 2)
            t_mid = self.points[i_mid].timestamp
            if t_mid > timestamp:
                i1 = i_mid
            else:
                i0 = i_mid
        return self.points[i0], self.points[i1]

    def __repr__(self):
        return '\n'.join([str(c) for c in self.points])
