import numpy as np
import math as m
from typing import List, Tuple, Dict

from Graph import Graph
from Station import Station
from heuristics import DistanceHeuristic as DH
from custom_implementations.custom_queue import PriorityQueue as PQ
from custom_implementations.custom_queue import Queue as Q
from custom_implementations.custom_stack import Stack as S
from custom_implementations.linked_list import LinkedList as LL

def GetShortestPathStatic(start_station: str, end_station: str, algorithm: str) -> Tuple[str, str, List[str], List[str]]:
    shortest_path_calculator = ShortestPath(start_station, end_station)
    if algorithm == '1':
        data = shortest_path_calculator.bfs()
    elif algorithm == '2':
        data = shortest_path_calculator.dijkstra()
    elif algorithm == '3':
        data = shortest_path_calculator.a_star()
    else:
        data = shortest_path_calculator.k_shortest_path(2)
        
    return (
        f"{data[0]:.2f} km",
        f"{data[1]//60:.2f} minutes {data[1]%60}s",
        data[2],
        data[3],
    )

class ShortestPath:
    def __init__(self, start_station: str, end_station: str):
        self.start_station = start_station
        self.end_station = end_station
        self.earth_radius = 6371.0
        self.heuristic = DH()
        self.graph = Graph()
        self.adjacency_list = self.graph.get_adjacency_list()
        self.stations_info = self.graph.get_station_info()
        self.interchange_stations = self.graph.get_interchange_stations()

    def _evaluate_time_for_distance(self, distance_meters: float) -> float:
        cruise_speed = 27.8     # m/s
        acceleration = 1.0      # m/s^2
        accel_decel_distance = (cruise_speed ** 2) / acceleration

        if distance_meters >= accel_decel_distance:
            #This formula is used when the distance is greater than the acceleration distance
            acceleration_time = cruise_speed / acceleration
            accel_distance = 0.5 * acceleration * (acceleration_time ** 2)
            cruise_distance = distance_meters - 2 * accel_distance
            cruise_time = cruise_distance / cruise_speed
            total_time = 2 * acceleration_time + cruise_time
            
        else:
            #This formula is used when the distance is less than the acceleration distance
            acceleration_time = m.sqrt(distance_meters / acceleration)
            total_time = 2 * acceleration_time

        return total_time
    
    def _travel_cost(self,code,neighour,total_distance,total_time) -> Tuple[float, float]:
        travel_info = self.adjacency_list[code][neighour]
        travel_cost = travel_info["cost"]
        travel_method = travel_info["method"]

        if travel_method == "train":
            total_distance += travel_cost
            total_time += self._evaluate_time_for_distance(travel_cost)
            if code not in self.interchange_stations:
                total_time += 28
            else:
                total_time += 35
                
        elif travel_method == "transfer":
            total_distance += total_distance
            
        return total_distance, total_time

    def reconstruct_path(self, previous: dict) -> Tuple[float, float, list[str], list[str]]:
        path = []
        current_station = self.end_station

        if current_station not in previous or previous[current_station] is None:
            return float('inf'), 0.0, [], []

        while current_station != self.start_station:
            if current_station not in previous:
                return float('inf'), 0.0, [], []
            path.append(current_station)
            current_station = previous[current_station]
        path.append(self.start_station)

        path_stack = S()
        while path:
            path_stack.push(path.pop())
        while not path_stack.is_empty():
            path.append(path_stack.pop())

        station_names = [self.stations_info[s].get_station_name() for s in path]
        total_distance = 0.0
        total_time = 0.0

        for i, code in enumerate(path):
            if i < len(path) - 1:
                neighbour = path[i + 1]
                if neighbour not in self.adjacency_list[code]:
                    continue
                
                total_distance, total_time = self._travel_cost(code,
                                                               neighbour,
                                                               total_distance,
                                                               total_time)
                
                # travel_info = self.adjacency_list[code][neighbour]
                # travel_cost = travel_info["cost"]
                # travel_method = travel_info["method"]

                # if travel_method == "train":
                #     total_distance += travel_cost
                #     total_time += self._evaluate_time_for_distance(travel_cost)
                #     if code not in self.interchange_stations:
                #         total_time += 28
                #     else:
                #         total_time += 35
                        
                # elif travel_method == "transfer":
                #     total_time += travel_cost

        return total_distance, total_time, path, station_names

    def bfs(self) -> Tuple[float, float, list, list]:
        queue = Q()
        visited_stations = {node: False for node in self.adjacency_list}
        distance_map = {node: m.inf for node in self.adjacency_list}
        previous = {node: None for node in self.adjacency_list}

        current_station = self.start_station
        queue.enqueue(current_station)
        visited_stations[current_station] = True
        distance_map[current_station] = 0

        while not queue.is_empty():
            current_station = queue.dequeue()
            if current_station == self.end_station:
                break
            visited_stations[current_station] = True

            for neighbour in self.adjacency_list[current_station]:
                if not visited_stations[neighbour]:
                    if (distance_map[current_station] +
                            self.adjacency_list[current_station][neighbour]["cost"]
                            < distance_map[neighbour]):
                        distance_map[neighbour] = (distance_map[current_station] +
                                                  self.adjacency_list[current_station][neighbour]["cost"])
                        previous[neighbour] = current_station
                        queue.enqueue(neighbour)
                        
        return self.reconstruct_path(previous)

    def dijkstra(self) -> Tuple[float, float, list, list]:
        
        if self.start_station == self.end_station:
            return 0.0, 0.0, [], []
        
        # Initialize data structures
        priority_queue = PQ()
        visited_stations = {node: False for node in self.adjacency_list}
        distance_map = {node: m.inf for node in self.adjacency_list}
        previous_stations = {node: None for node in self.adjacency_list}

        visited_stations[self.start_station] = True
        distance_map[self.start_station] = 0
        previous_stations[self.start_station] = None

        priority_queue.enqueue((0, self.start_station))

        #while the priority queue is not empty
        while not priority_queue.is_empty():
            current_station = priority_queue.dequeue()[1]
            #check if the current station is the destination
            if current_station == self.end_station:
                break
            #mark the current station as visited
            visited_stations[current_station] = True

            #iterate through the neighbours of the current station
            for neighbour, travel_info in self.adjacency_list[current_station].items():
                #convert the travel cost to time if the method is train
                travel_cost = travel_info["cost"]
                if travel_info["method"] == "train":
                    travel_cost = self._evaluate_time_for_distance(travel_cost)

                #update the distance map if a shorter path is found
                new_distance = distance_map[current_station] + travel_cost
                if new_distance < distance_map[neighbour]:
                    distance_map[neighbour] = new_distance
                    previous_stations[neighbour] = current_station
                    priority_queue.enqueue((new_distance, neighbour))

        return self.reconstruct_path(previous_stations)

    def a_star(self) -> Tuple[float, float, list[str], list[str]]:
        
        # f(n) = g(n) + h(n) where g(n) is the time taken to reach the current station and h(n) is the heuristic in this case the euclidian distance in time
        
        # If the start and end stations are the same
        if self.start_station == self.end_station:
            return (0.0, 0.0, [], [])
        
        # Initialize data structures
        closed_list = []
        priority_queue = PQ()
        visited_stations = {node: False for node in self.adjacency_list}
        time_map = {node: m.inf for node in self.adjacency_list}
        previous_stations = {node: None for node in self.adjacency_list}

        visited_stations[self.start_station] = True
        time_map[self.start_station] = 0
        previous_stations[self.start_station] = None

        # Enqueue the start station
        priority_queue.enqueue((0, self.start_station))
        
        # Get the coordinates of the end station
        end_lng = float(self.stations_info[self.end_station].get_lng())
        end_lat = float(self.stations_info[self.end_station].get_lat())

        # While the priority queue is not empty
        while not priority_queue.is_empty():
            #dequeue the station with the shortest time
            current_station = priority_queue.dequeue()[1]
            if current_station == self.end_station:
                break
            
            #mark the current station as visited
            visited_stations[current_station] = True
            
            for neighbour, travel_info in self.adjacency_list[current_station].items():
                #check if the neighbour has been visited
                if neighbour in closed_list:
                    continue
                #convert the travel cost to time if the method is train
                travel_cost = travel_info["cost"]
                if travel_info["method"] == "train":
                    travel_cost = self._evaluate_time_for_distance(travel_cost)

                #g(n) is the time taken to reach the current station
                tentative_time = time_map[current_station] + travel_info["cost"]
                
                #update the time map if a shorter path is found
                if tentative_time < time_map[neighbour]:
                    time_map[neighbour] = tentative_time
                    previous_stations[neighbour] = current_station
                    distance_estimate = self.heuristic.euclidian(
                        float(self.stations_info[neighbour].get_lat()),
                        float(self.stations_info[neighbour].get_lng()),
                        end_lat,
                        end_lng,
                    )
                    #convert the distance estimate to time
                    heuristic = self._evaluate_time_for_distance(distance_estimate)
                    priority_queue.enqueue((time_map[neighbour] + heuristic, neighbour))
        
        #if the end station is not in the previous stations list, return an empty path
        if self.end_station not in previous_stations or current_station != self.end_station:
            return (0.0, 0.0, [], [])
        
        return self.reconstruct_path(previous_stations)

    def k_shortest_path(self, k) -> List[Tuple[float, float, List[str], List[str]]]:
        # K shortest path algorithm is an algorithm that finds the k shortest paths between two nodes in a graph
        
        # If the start and end stations are the same return an empty path
        if self.start_station == self.end_station:
            return [(0.0, 0.0, [], [])]
        
        # First path using A* algorithm
        first_path = self.a_star()
        if not first_path[2]:
            return []

        # Initialize the shortest paths list with the first path
        shortest_paths = [first_path]
        possible_paths = LL()

        # Loop to find the next k-1 shortest paths
        for _ in range(1, k):
            previous_path = shortest_paths[-1]
            _, _, route, _ = previous_path

            # Iterate through each node in the route except the last one
            for i in range(len(route) - 1):
                removed_edges = []
                # Remove edges that are part of the previous shortest paths
                for j in range(len(shortest_paths)):
                    if j < len(shortest_paths) and shortest_paths[j][2][:i] == route[:i]:
                        u = shortest_paths[j][2][i]
                        v = shortest_paths[j][2][i + 1]
                        
                        if v in self.adjacency_list[u]:
                            removed_edges.append((u, v, self.adjacency_list[u][v]))
                            del self.adjacency_list[u][v]

                # Find the new path after removing edges
                new_path = self.a_star()
                spur_route = new_path[2]

                # Restore the removed edges
                for (u, v, edge_info) in removed_edges:
                    self.adjacency_list[u][v] = edge_info

                # If a new spur route is found, calculate the total route and its cost
                if spur_route:
                    new_route = route[:i] + spur_route
                    distance, _, _, names = new_path
                    time = 0.0
                    
                    # Calculate the total time for the new route
                    for i in range(len(new_route) - 1):
                        u, v = new_route[i], new_route[i + 1]
                        
                        if v not in self.adjacency_list[u]:
                            continue
                        
                        distance, time = self._travel_cost(u, v, distance, time)
                        
                    possible_paths.append((distance, time, new_route, names))

            # If no more possible paths, break
            if not possible_paths:
                break
            
        # Sort the possible paths and add the shortest ones to the shortest paths list
        possible_paths.merge_sort()
        for _ in range(0, k - 1):
            shortest_paths.append(possible_paths.dequeue())

        return shortest_paths

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
#         paths = ShortestPath(item1, item2).k_shortest_path(3)
#         for j in paths:
#             x = list(j)
#             # print(data)
#             print(f"Distance: {x[0]}")
#             print(f"Time: {x[1]}")
#             codes = ', '.join(x[2])
#             names = ', '.join(x[3])
#             print(f"Station Codes: {codes}")
#             print(f"Station  Names: {names}")