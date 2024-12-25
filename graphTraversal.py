from graph import Graph
from utilities import maths
from typing import List, Tuple, Dict
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
        self.__interchange_stations = Graph().get_interchange_stations()
    
    def convert_to_time(self, distance: float) -> str:
        max_speed = 27.8  # m/s
        acceleration = 1.0  # m/s^2

        distance_accel_deccel = (max_speed ** 2) / acceleration  # Distance needed to reach max speed and slow down

        if distance >= distance_accel_deccel:
            accel = max_speed / acceleration
            acceleration_distance_covered = 0.5 * acceleration * accel ** 2
            cruise_distance = distance - 2 * acceleration_distance_covered
            cruise_time = cruise_distance / max_speed
            total_travel_time = 2 * accel + cruise_time
        else:
            accel = m.sqrt(distance / acceleration)
            total_travel_time = 2 * accel

        return total_travel_time

    def haversine(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        #Haversine formula used to calculate the distance between two points takes latitude and longitude of two points as arguments returns the absolute value of the distance as float
        
        lat1,lat2,lng1,lng2 = map(m.radians, [lat1,lat2,lng1,lng2])
        d_lat = lat2 - lat1
        d_lon = lng2 - lng1
        # radius of the Earth in km
        R = 6371.0
        # Convert latitude and longitude from degrees to radians
        lat1_rad, lat2_rad, lng1_rad, lng2_rad = map(m.radians, [lat1, lat2, lng1, lng2])

        # Haversine formula
        d_lat = lat2_rad - lat1_rad
        d_lon = lng2_rad - lng1_rad

        a = m.sin(d_lat / 2) ** 2 + m.cos(lat1_rad) * m.cos(lat2_rad) * m.sin(d_lon / 2) ** 2
        c = 2 * m.atan2(m.sqrt(a), m.sqrt(1 - a))

        return R * c
    
    def euclidian(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        #Euclidian formula used to calculate the distance between two points takes latitude and longitude of two points as arguments returns the absolute value of the distance as float
        return m.sqrt((lat2 - lat1) ** 2 + (lng2 - lng1) ** 2)
    
    def reconstruct_path(self, previous):
            current = self.__end
            path = []

            if current not in previous or previous[current] is None:
                return float('inf'), 0.0, [], []

            while current != self.__start:
                if current is None or current not in previous:
                    return float('inf'), 0.0, [], []
                path.append(current)
                current = previous[current]
            path.append(self.__start)
            path.reverse()

            station_names = [self.__stations[station][0] for station in path]

            distance = 0  # distance in meters
            time = 0.0  # float due to the conversion of time to seconds

            for i in range(len(path)):
                code = path[i]
                if i < len(path) - 1:
                    field = self.__adjacency_list[code][path[i + 1]]
                    if field["method"] == "train":
                        distance += field["cost"]
                        time += self.convert_to_time(field["cost"])
                        if code not in self.__interchange_stations:
                            time += 28
                        elif code in self.__interchange_stations:
                            time += 35
                    elif field["method"] == "transfer":
                        time += field["cost"]

            return f"{distance/1000:.0f} km", f"{time//60:.0f} minutes and {time%60:.0f} seconds", path, station_names
        
    
    def bfs(self) -> str:
        #Breadth First Search algorithm to find the shortest path between two stations takes start and end as arguments returns a tuple of start, end, distance, path, station_names
        queue = []
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

        queue.append(self.__start)

        while queue:
            current = queue.pop(0)
            visited[current] = True

            for neighbour in self.__adjacency_list[current]:
                if not visited[neighbour]:
                    if distances[current] + self.__adjacency_list[current][neighbour]["cost"] < distances[neighbour]:
                        distances[neighbour] = distances[current] + self.__adjacency_list[current][neighbour]["cost"]
                        previous[neighbour] = current
                        queue.append(neighbour)

        current = self.__end
        path = []

        while current != self.__start:
            path.append(current)
            current = previous[current]
        path.append(self.__start)
        path.reverse()

        station_names = [self.__stations[station][0] for station in path]

        return f"{distances[self.end]:.2f}", path, station_names

    def dijkstra(self) -> str:
        #Dijkstra algorithm to find the shortest path between two stations takes start and end as arguments returns a tuple of start, end, distance, path, station_names
        priority_queue = PQ()
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
            priority_queue.enqueue((0, self.__start))#distance, station

        while not priority_queue.is_empty():
            current = priority_queue.dequeue()[1]
            visited[current] = True

            for neighbour in self.__adjacency_list[current]:
                if not visited[neighbour]:
                    if distances[current] + self.__adjacency_list[current][neighbour]["cost"] < distances[neighbour]:
                        distances[neighbour] = distances[current] + self.__adjacency_list[current][neighbour]["cost"]
                        previous[neighbour] = current
                        priority_queue.enqueue((distances[neighbour], neighbour))

        
        return self.reconstruct_path(previous)
    
    def a_star(self) -> Tuple[float, float, list[str], list[str]]:
        # A* algorithm to find the shortest path between two stations
        priority_queue = PQ()
        visited = {v: False for v in self.__adjacency_list}
        distances = {v: m.inf for v in self.__adjacency_list}
        previous = {v: None for v in self.__adjacency_list}

        distances[self.__start] = 0
        priority_queue.enqueue((0, self.__start))

        end_long = float(self.__stations[self.__end][3])
        end_lat = float(self.__stations[self.__end][4])

        while not priority_queue.is_empty():
            current = priority_queue.dequeue()[1]
            
            if current == self.__end:
                break
            visited[current] = True

            for neighbour, data in self.__adjacency_list[current].items():
                if neighbour in self.__closed:
                    continue
                tentative_g_score = distances[current] + data["cost"]
                
                if tentative_g_score < distances[neighbour]:
                    distances[neighbour] = tentative_g_score
                    previous[neighbour] = current
                    heuristic = self.euclidian(
                        float(self.__stations[neighbour][3]),
                        float(self.__stations[neighbour][4]),
                        end_lat,
                        end_long
                    )
                    priority_queue.enqueue((distances[neighbour] + heuristic, neighbour))

        if self.__end not in previous or current != self.__end:
            return float('inf'), 0.0, [], []
        
        return self.reconstruct_path(previous)
    
    def k_shortest_path(self):
        k = 2
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
                            total_distance += self.__adjacency_list[total_path[p]][total_path[p+1]]["cost"]
                    
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
     
# s1 = ["NS2","CC5","EW20","DT30"]
# s2 = ["NS22","EW20"]
# for item1 in s1:
#     for item2 in s2:
#         print(f"Shortest path from {item1} to {item2}:")
#         distance, time, codes, names = get_shortest_path(item1, item2).a_star()
#         print(f"Distance: {distance} km")
#         print(f"Time: {time}")
#         codes = ','.join(codes)
#         names = ','.join(names)
#         print(f"Station Codes: {codes}")
#         print(f"Station  Names: {names}")
#         print(f"Shortest path from {item1} to {item2}:")
        # distance, time, codes, names = get_shortest_path(item1, item2).dijkstra()
        # print(f"Distance: {distance} km")
        # print(f"Time: {time}")
        # codes = ','.join(codes)
        # names = ','.join(names)
        # print(f"Station Codes: {codes}")
        # print(f"Station  Names: {names}")
        # print(f"Shortest path from {item1} to {item2}:")
    