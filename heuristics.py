import math as m

class DistanceHeuristic:
    
    def __init__(self):
        self.RADIUS = 6371
         
    def manhattan(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
            
            lat1_rad, lat2_rad, lng1_rad, lng2_rad = map(m.radians, [lat1, lat2, lng1, lng2])
            delta_lat = lat2_rad - lat1_rad
            delta_lng = lng2_rad - lng1_rad
            a = (m.sin(delta_lat / 2) ** 2 + m.cos(lat1_rad) * m.cos(lat2_rad) * m.sin(delta_lng / 2) ** 2)
            c = 2 * m.atan2(m.sqrt(a), m.sqrt(1 - a))
            return self.RADIUS * c

    def euclidian(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        
        lat1, lng1, lat2, lng2 = map(m.radians, [lat1, lng1, lat2, lng2])
        return m.sqrt( self.RADIUS * ( (lat2 - lat1) ** 2 + (lng2 - lng1) ** 2 ))
