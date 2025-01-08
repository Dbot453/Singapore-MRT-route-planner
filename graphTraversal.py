###############################################################
# yen's is not doing time as of yet work out a way to implement
###############################################################

from Graph import Graph
from Station import Station
from typing import List, Tuple, Dict
from custom_implementations.utilities import maths
from custom_implementations.custom_queue import PriorityQueue as PQ
from custom_implementations.custom_queue import Queue as Q
from custom_implementations.custom_stack import Stack as S
import numpy as np
import math as m

def GetShortestPathStatic(start: str, end: str, algorithm: str):
    """
    GetShortestPathStatic function is used as a static method to get the shortest path between two stations
    """
    instance = ShortestPath(start, end)

    #<option value='1'>Breadth First Search</option>
    #<option value='2'>Dijkstra</option>
    #<option value='3'>K Shortest Path</option>
    #<option value='4'>A Star</option>

    if algorithm == '1' : #'Breadth First Search':
        return instance.bfs()
    elif algorithm == '2': # 'Dijkstra':
        return instance.dijkstra()
    elif algorithm == '3': #'K Shortest Path':
        return instance.k_shortest_path()
    else: 
        return instance.a_star()
    
class ShortestPath:
    def __init__(self, start: str, end: str):
        self.__start = start
        self.__end = end
        # radius of the Earth in km
        self.RADIUS = 6371.0
        graph = Graph()
        self.__adjacency_list = graph.get_adjacency_list()
        self.__stations = graph.get_station_info()
        self.__interchange_stations = graph.get_interchange_stations()
    
    def convert_to_time(self, distance: float) -> float:
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
        R = 6371.0
        # Convert latitude and longitude from degrees to radians
        lat1_rad, lat2_rad, lng1_rad, lng2_rad = map(m.radians, [lat1, lat2, lng1, lng2])

        # Haversine formula
        d_lat = lat2_rad - lat1_rad
        d_lon = lng2_rad - lng1_rad

        a = m.sin(d_lat / 2) ** 2 + m.cos(lat1_rad) * m.cos(lat2_rad) * m.sin(d_lon / 2) ** 2
        c = 2 * m.atan2(m.sqrt(a), m.sqrt(1 - a))

        return self.RADIUS * c
    
    def euclidian(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        #Euclidian formula used to calculate the distance between two points takes latitude and longitude of two points as arguments returns the absolute value of the distance as float
        return m.sqrt((lat2 - lat1) ** 2 + (lng2 - lng1) ** 2)
    
    def reconstruct_path(self, previous) -> Tuple[float, float, list[str], list[str]]:
            current = self.__end
            path = []
            stack = S()

            if current not in previous or previous[current] is None:
                return float('inf'), 0.0, [], []

            while current != self.__start:
                if current is None or current not in previous:
                    return float('inf'), 0.0, [], []
                path.append(current)
                current = previous[current]
            path.append(self.__start)
            
            #same as reversing the path using .reverse
            while path != []:
                stack.push(path.pop())
            while not stack.is_empty():
                path.append(stack.pop())
                

            station_names = [self.__stations[station].get_station_name() for station in path]

            distance = 0  # distance in meters
            time = 0.0  # float due to the conversion of time to seconds

            for i in range(len(path)):
                code = path[i]
                if i < len(path) - 1:
                    cost = self.__adjacency_list[code][path[i + 1]]
                    if cost["method"] == "train":
                        distance += cost["cost"]
                        time += self.convert_to_time(cost["cost"])
                        if code not in self.__interchange_stations:
                            time += 28
                        elif code in self.__interchange_stations:
                            time += 35
                    elif cost["method"] == "transfer":
                        time += cost["cost"]

            return (f"{distance/1000:.0f} km", f"{time//60:.0f} minutes and {time%60:.0f} seconds", path, station_names)
           
    #BFS has issues
    def bfs(self) -> Tuple[float, float, list, list]:
        #Breadth First Search algorithm to find the shortest path between two stations takes start and end as arguments returns a tuple of start, end, distance, path, station_names
    
        queue = Q()
        visited = {v: False for v in self.__adjacency_list}
        distances = {v: m.inf for v in self.__adjacency_list}
        previous = {v : None for v in self.__adjacency_list}
        current = self.__start
        queue.enqueue(current)

        visited[current] = True
        distances[current] = 0
        previous[current] = None

        while not queue.is_empty():
            current = queue.dequeue()
            if current == self.__end:
                break
            visited[current] = True

            #for each neighbour of the current station if not visited add to queue
            for neighbour in self.__adjacency_list[current]:
                if not visited[neighbour]:
                    if distances[current] + self.__adjacency_list[current][neighbour]["cost"] < distances[neighbour]:
                        distances[neighbour] = distances[current] + self.__adjacency_list[current][neighbour]["cost"]
                        previous[neighbour] = current
                        queue.enqueue(neighbour)


        return self.reconstruct_path(previous)
    
    def dijkstra(self) -> str:
        #Dijkstra algorithm to find the shortest path between two stations takes start and end as arguments returns a tuple of start, end, distance, path, station_names
        priority_queue = PQ()
        visited = {v: False for v in self.__adjacency_list}
        distances = {v: m.inf for v in self.__adjacency_list}
        previous = {v : None for v in self.__adjacency_list}
        
        visited[self.__start] = True
        distances[self.__start] = 0
        previous[self.__start] = None
        
        current = self.__start
        priority_queue.enqueue((0, self.__start))#distance, station

        while not priority_queue.is_empty():
            current = priority_queue.dequeue()[1]
            if current == self.__end:
                break
            visited[current] = True

            for neighbour,data in self.__adjacency_list[current].items():
                cost = data["cost"]
                #converts distance to time if method of travel is train
                if data["method"] == "train":
                    cost = self.convert_to_time(cost)

                if distances[current] + cost < distances[neighbour]:
                    distances[neighbour] = distances[current] + cost
                    previous[neighbour] = current
                    priority_queue.enqueue((distances[neighbour], neighbour))
        
        return self.reconstruct_path(previous)
    
    def a_star(self) -> Tuple[float, float, list[str], list[str]]:
        # A* algorithm to find the shortest path between two stations
        priority_queue = PQ()
        visited = {v: False for v in self.__adjacency_list}
        times = {v: m.inf for v in self.__adjacency_list}
        previous = {v: None for v in self.__adjacency_list}
        self.__closed = []
        
        visited[self.__start] = True
        times[self.__start] = 0
        previous[self.__start] = None
        
        if self.__start == self.__end:
            return (0.0, 0.0, [], [])

        times[self.__start] = 0
        priority_queue.enqueue((0, self.__start))

        end_long = float(self.__stations[self.__end].get_lng())
        end_lat = float(self.__stations[self.__end].get_lat())
        
        while not priority_queue.is_empty():
            current = priority_queue.dequeue()[1]            
            if current == self.__end:
                break

            visited[current] = True
            for neighbour,data in self.__adjacency_list[current].items():
                if neighbour in self.__closed:
                    continue
                
                cost = data["cost"]
                if data["method"] == "train":
                    cost = self.convert_to_time(cost)    
     
                tentative_g_score = times[current] + data["cost"]   
                             
                if tentative_g_score < times[neighbour]:
                    times[neighbour] = tentative_g_score
                    previous[neighbour] = current
                    d_est = self.euclidian(float(self.__stations[neighbour].get_lat()), float(self.__stations[neighbour].get_lng()),end_lat,end_long)
                    heuristic = self.convert_to_time(d_est)
                    priority_queue.enqueue((times[neighbour] + heuristic, neighbour))
                    
        if self.__end not in previous or current != self.__end:
            return (0.0, 0.0, [], [])
        
        return self.reconstruct_path(previous)
    
    def k_shortest_path(self,k):
        A = []
        B = []
        self.closed = []
        
        data = self.a_star()
        distance1, time1, path1 = data[0], data[1], data[2]
        
        A.append((distance1, path1))
        
        for _ in range(k-1):
            prev_path = A[-1][1]
            
            for j in range(len(prev_path)-1):
                spur_node = prev_path[j]
                root_path = prev_path[:j+1]
                
                removed_edges = {}
                for _, path in A:
                    if len(path) > j and path[:j+1] == root_path:
                        if path[j] in self.__adjacency_list and path[j+1] in self.__adjacency_list[path[j]]:
                            if path[j] not in removed_edges:
                                removed_edges[path[j]] = {}
                            removed_edges[path[j]][path[j+1]] = self.__adjacency_list[path[j]][path[j+1]]
                            del self.__adjacency_list[path[j]][path[j+1]]
                
                removed_nodes = []
                for node in root_path[:-1]:
                    if node not in self.__closed:
                        self.__closed.append(node)
                        removed_nodes.append(node)
                
                self.__start = spur_node
                data = self.a_star()
                spur_distance, time1, spur_path = data[0], data[1], data[2]
                time = 0.0
                
                if spur_path:
                    total_path = root_path[:-1] + spur_path
                    total_distance = 0
                    
                    for i in range(len(path)-1):
                        code = path[i]
                        if i < len(path) - 1:
                            if path[i + 1] not in self.__adjacency_list[code]:
                                continue
                            field = self.__adjacency_list[code][path[i + 1]]
                            if field["method"] == "train":
                                total_distance += field["cost"]
                                time += self.convert_to_time(field["cost"])
                                if code not in self.__interchange_stations:
                                    time += 28
                                elif code in self.__interchange_stations:
                                    time += 35
                            elif field["method"] == "transfer":
                                time += field["cost"]

                    potential_k = (total_distance, total_path)
                    if potential_k not in B:
                        B.append(potential_k)
            
            if not B: break
            B.sort(key=lambda x: x[0]) 
            A.append(B[0])
            B.pop(0)
            self.__start = A[0][1][0]
        
        result = []
        for total_distance, path in A:
            station_names = [self.__stations[station].get_station_name() for station in path]
            result.append((total_distance, time1, path, station_names))
            
        return result     
     
# s1 = ["NS2","CC5","EW20","DT30"]
# s2 = ["NS22","EW20"]
# for item1 in s1:
#     for item2 in s2:
#         print(f"Shortest path from {item1} to {item2}:")
        
#         print(f"Breadth First Search")
#         x = ShortestPath(item1, item2).bfs()
#         distance,time,path,station_names = x[0], x[1], x[2], x[3]
#         print(f"Distance: {distance}")
#         print(f"Time: {time}")
#         print(f"Station Codes: {', '.join(path)}")
#         print(f"Station  Names: {', '.join(station_names)}")
        
#         x = ShortestPath(item1, item2).dijkstra()
#         print(f"Dijkstra's algorithm")
#         distance,time,path,station_names = x[0], x[1], x[2], x[3]
#         print(f"Distance: {distance}")
#         print(f"Time: {time}")
#         print(f"Station Codes: {', '.join(path)}")
#         print(f"Station  Names: {', '.join(station_names)}")
        
#         print(f"A* algorithm")
#         x = ShortestPath(item1, item2).a_star()
#         distance,time,path,station_names = x[0], x[1], x[2], x[3]
#         print(f"Distance: {distance}")
#         print(f"Time: {time}")
#         print(f"Station Codes: {', '.join(path)}")
#         print(f"Station  Names: {', '.join(station_names)}")
        
#         print(f"using Yen's algorithm")
#         paths = ShortestPath(item1, item2).k_shortest_path(2)
#         for j in paths:
#             x = list(j)
#             # print(data)
#             print(f"Distance: {x[0]}")
#             print(f"Time: {x[1]}")
#             codes = ', '.join(x[2])
#             names = ', '.join(x[3])
#             print(f"Station Codes: {codes}")
#             print(f"Station  Names: {names}")

    