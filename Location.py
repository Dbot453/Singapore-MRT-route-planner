from heuristics import DistanceHeuristic

class Location:
    def __init__(self, lat: float, lng: float):
        self._lat = lat
        self._lng = lng
        self.heuristic = DistanceHeuristic()

    @property
    def lat(self) -> float:
        return self._lat

    @property
    def lng(self) -> float:
        return self._lng

    def distance_to(self, other: 'Location') -> float:
        return self.heuristic.euclidean(self.lat, self.lng, other.lat, other.lng)