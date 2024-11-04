from graph import Graph
from utilities import maths
from custom_queue import PriorityQueue as PQ
import numpy as np
import math as m

def GetShortestPathStatic(start: str, end: str):
    """
    GetShortestPathStatic function is used as a static method to get the shortest path between two stations
    """
    instance = get_shortest_path(start, end)
    return instance.a_star()
    
class get_shortest_path:
    def __init__(self, start: str, end: str):
        self.__start = start
        self.__end = end
        self.__closed = []
        self.__adjacency_list = Graph().get_adjacency_list()
        self.__stations = Graph().get_station_info()

    def haversine(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """
        Haversine formula used to calculate the distance between two points takes latitude and longitude of two points as arguments returns the absolute value of the distance as float
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
        #Dijkstra algorithm to find the shortest path between two stations takes start and end as arguments returns a tuple of start, end, distance, path, station_names
        q = PQ()
        visited = {}
        distances = {}
        previous = {}
        current = self.__start

        for v in self.__adjacency_list:
            if v == self.__start:
                visited[self.__start] = True
                distances[self.__start] = 0
            else:
                visited[v] = False
                distances[v] = m.inf

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
    
    def a_star(self) -> str:
        #A* algorithm to find the shortest path between two stations takes start and end as arguments returns a tuple of start, end, distance, path, station_names
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

        if self.__end not in previous and current != self.__end:
            return float('inf'), [], []

        current = self.__end
        path = []

        if current not in previous or previous[current] is None:
            return float('inf'), [], []

        while current != self.__start:
            if current is None or current not in previous:
                return float('inf'), [], []
            path.append(current)
            current = previous[current]
        path.append(self.__start)
        path.reverse()

        station_names = [self.__stations[station][0] for station in path]

        return distances[self.__end], path, station_names
    
    def k_shortest_path(self):
        k = 4
        A = []
        B = []
        
        first_distance, first_path, first_names = self.a_star()
        A.append((first_distance, first_path))
        
        for i in range(k-1):
            prev_path = A[-1][1]
            
            for j in range(len(prev_path)-1):
                spur_node = prev_path[j]
                root_path = prev_path[:j+1]
                
                edges_removed = {}
                for path_distance, path in A:
                    if len(path) > j and path[:j+1] == root_path:
                        if path[j] in self.__adjacency_list and path[j+1] in self.__adjacency_list[path[j]]:
                            if path[j] not in edges_removed:
                                edges_removed[path[j]] = {}
                            edges_removed[path[j]][path[j+1]] = self.__adjacency_list[path[j]][path[j+1]]
                            del self.__adjacency_list[path[j]][path[j+1]]
                
                nodes_removed = []
                for node in root_path[:-1]:
                    if node not in self.__closed:
                        self.__closed.append(node)
                        nodes_removed.append(node)
                
                self.__start = spur_node
                spur_distance, spur_path, _ = self.a_star()
                
                if spur_path:
                    total_path = root_path[:-1] + spur_path
                    total_distance = 0
                    
                    for p in range(len(total_path)-1):
                        if total_path[p] in self.__adjacency_list and total_path[p+1] in self.__adjacency_list[total_path[p]]:
                            total_distance += self.__adjacency_list[total_path[p]][total_path[p+1]]
                    
                    potential_k = (total_distance, total_path)
                    if potential_k not in B:
                        B.append(potential_k)
            
            if not B: break
            B.sort(key=lambda x: x[0]) 
            A.append(B[0])
            B.pop(0)
            self.__start = A[0][1][0]
        
        result = []
        for distance, path in A:
            station_names = [self.__stations[station][0] for station in path]
            result.append((distance, path, station_names))
            
        return result
