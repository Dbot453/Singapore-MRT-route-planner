from graph import Graph
from utilities import maths
from custom_queue import PriorityQueue as PQ
import numpy as np
import math as m

def GetShortestPathStatic(start: str, end: str):
    instance = GetShortestPath(start, end)
    return instance.astar()
    
class GetShortestPath:
    def __init__(self, start: str, end: str):
        self.__start = start
        self.__end = end
        self.__closed = []
        self.__adjacency_list = Graph().get_adjacency_list()
        self.__stations = Graph().get_station_info()

    def haversine(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """
        Haversine formula to calculate the distance between two points takes latitude and longitude of two points as arguments returns the absolute value of the distance as float
        """
        lat1 = m.radians(lat1)
        lat2 = m.radians(lat2)
        lng1 = m.radians(lng1)
        lng2 = m.radians(lng2)
        d_lat = lat2 - lat1
        d_lon = lng2 - lng1
        R = 6371.0

        a = pow(np.sin(d_lat / 2), 2)
        root_a = m.sqrt(a)
        root_1_a = m.sqrt(1 - a)
        c = 2 * m.atan2(root_a, root_1_a)
        latitude_distance = R * c

        a = pow(np.sin(d_lon / 2), 2)
        root_a = m.sqrt(a)
        root_1_a = m.sqrt(1 - a)
        c = 2 * m.atan2(root_a, root_1_a)
        longitude_distance = R * c

        return maths.mod(latitude_distance) + maths.mod(longitude_distance)

    def dijkstra(self) -> str:
        """
        Dijkstra algorithm to find the shortest path between two stations takes start and end as arguments returns a tuple of start, end, distance, path, station_names
        """
        q = PQ()
        visited = {}
        distances = {}
        previous = {}
        current = self.__start

        for v in self.__adjacency_list:
            if v != self.__start:
                visited[v] = False
                distances[v] = m.inf
            else:
                visited[self.__start] = True
                distances[self.__start] = 0

        for station in self.__adjacency_list.keys():
            if station != self.__start:
                previous[station] = None
                distances[station] = m.inf
            q.enqueue((0, self.__start))

        while not q.is_empty():
            current = q.dequeue()[1]
            visited[current] = True

            for neighbour in self.__adjacency_list[current]:
                if not visited[neighbour]:
                    if distances[current] + self.__adjacency_list[current][neighbour] < distances[neighbour]:
                        distances[neighbour] = distances[current] + self.__adjacency_list[current][neighbour]
                        previous[neighbour] = current
                        q.enqueue((distances[neighbour], neighbour))

        current = self.__end
        path = []

        while current != self.__start:
            path.append(current)
            current = previous[current]
        path.append(self.__start)
        path.reverse()

        station_names = [self.__stations[station][0] for station in path]

        return distances[self.__end], path, station_names
    
    def astar(self) -> str:
        """
        A* algorithm to find the shortest path between two stations takes start and end as arguments returns a tuple of start, end, distance, path, station_names
        """
        q = PQ()
        visited = {}
        distances = {}
        previous = {}
        current = self.__start

        for v in self.__adjacency_list:
            if v != self.__start:
                visited[v] = False
                distances[v] = m.inf
            else:
                visited[self.__start] = True
                distances[self.__start] = 0

        for station in self.__adjacency_list.keys():
            if station != self.__start:
                previous[station] = None
                distances[station] = m.inf
            q.enqueue((0, self.__start))

        end_long = float(self.__stations[self.__end][3])
        end_lat = float(self.__stations[self.__end][4])

        while not q.is_empty():
            current = q.dequeue()[1]
            if current == self.__end:
                break
            visited[current] = True

            for neighbour in self.__adjacency_list[current]:
                if neighbour in self.__closed:
                    continue
                tentative_g_score = distances[current] + self.__adjacency_list[current][neighbour]
                if tentative_g_score < distances[neighbour]:
                    distances[neighbour] = tentative_g_score
                    previous[neighbour] = current
                    heuristic = self.haversine(float(self.__stations[neighbour][3]), float(self.__stations[neighbour][4]), end_lat, end_long)
                    q.enqueue((distances[neighbour] + heuristic, neighbour))

        current = self.__end
        path = []

        while current != self.__start:
            path.append(current)
            current = previous[current]
        path.append(self.__start)
        path.reverse()

        station_names = [self.__stations[station][0] for station in path]

        return distances[self.__end], path, station_names