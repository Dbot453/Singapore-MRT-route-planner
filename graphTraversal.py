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

    def convert_to_time(self, distance_meters: float) -> float:
        cruise_speed = 27.8     # m/s
        acceleration = 1.0      # m/s^2
        accel_decel_distance = (cruise_speed ** 2) / acceleration

        #When the distance is greater than the acceleration distance
        if distance_meters >= accel_decel_distance:
            acceleration_time = cruise_speed / acceleration
            accel_distance = 0.5 * acceleration * (acceleration_time ** 2)
            cruise_distance = distance_meters - 2 * accel_distance
            cruise_time = cruise_distance / cruise_speed
            total_time = 2 * acceleration_time + cruise_time
            
        #When the distance is less than the acceleration distance
        else:
            acceleration_time = m.sqrt(distance_meters / acceleration)
            total_time = 2 * acceleration_time

        return total_time

    def reconstruct_path(self, predecessors: dict) -> Tuple[float, float, list[str], list[str]]:
        path = []
        current_station = self.end_station

        if current_station not in predecessors or predecessors[current_station] is None:
            return float('inf'), 0.0, [], []

        while current_station != self.start_station:
            if current_station not in predecessors:
                return float('inf'), 0.0, [], []
            path.append(current_station)
            current_station = predecessors[current_station]
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
                neighbor = path[i + 1]
                if neighbor not in self.adjacency_list[code]:
                    continue

                travel_info = self.adjacency_list[code][neighbor]
                travel_cost = travel_info["cost"]
                travel_method = travel_info["method"]

                if travel_method == "train":
                    total_distance += travel_cost
                    total_time += self.convert_to_time(travel_cost)
                    if code not in self.interchange_stations:
                        total_time += 28
                    else:
                        total_time += 35
                        
                elif travel_method == "transfer":
                    total_time += travel_cost

        return total_distance, total_time, path, station_names

    def bfs(self) -> Tuple[float, float, list, list]:
        queue = Q()
        visited_stations = {node: False for node in self.adjacency_list}
        distance_map = {node: m.inf for node in self.adjacency_list}
        predecessors = {node: None for node in self.adjacency_list}

        current_station = self.start_station
        queue.enqueue(current_station)
        visited_stations[current_station] = True
        distance_map[current_station] = 0

        while not queue.is_empty():
            current_station = queue.dequeue()
            if current_station == self.end_station:
                break
            visited_stations[current_station] = True

            for neighbor in self.adjacency_list[current_station]:
                if not visited_stations[neighbor]:
                    if (distance_map[current_station] +
                            self.adjacency_list[current_station][neighbor]["cost"]
                            < distance_map[neighbor]):
                        distance_map[neighbor] = (distance_map[current_station] +
                                                  self.adjacency_list[current_station][neighbor]["cost"])
                        predecessors[neighbor] = current_station
                        queue.enqueue(neighbor)
                        
        return self.reconstruct_path(predecessors)

    def dijkstra(self) -> Tuple[float, float, list, list]:
        priority_queue = PQ()
        visited_stations = {node: False for node in self.adjacency_list}
        distance_map = {node: m.inf for node in self.adjacency_list}
        previous_stations = {node: None for node in self.adjacency_list}

        visited_stations[self.start_station] = True
        distance_map[self.start_station] = 0
        previous_stations[self.start_station] = None

        priority_queue.enqueue((0, self.start_station))

        while not priority_queue.is_empty():
            current_station = priority_queue.dequeue()[1]
            if current_station == self.end_station:
                break
            visited_stations[current_station] = True

            for neighbor, travel_info in self.adjacency_list[current_station].items():
                travel_cost = travel_info["cost"]
                if travel_info["method"] == "train":
                    travel_cost = self.convert_to_time(travel_cost)

                new_distance = distance_map[current_station] + travel_cost
                if new_distance < distance_map[neighbor]:
                    distance_map[neighbor] = new_distance
                    previous_stations[neighbor] = current_station
                    priority_queue.enqueue((new_distance, neighbor))

        return self.reconstruct_path(previous_stations)

    def a_star(self) -> Tuple[float, float, list[str], list[str]]:
        closed_list = []
        priority_queue = PQ()
        visited_stations = {node: False for node in self.adjacency_list}
        time_map = {node: m.inf for node in self.adjacency_list}
        previous_stations = {node: None for node in self.adjacency_list}

        visited_stations[self.start_station] = True
        time_map[self.start_station] = 0
        previous_stations[self.start_station] = None

        if self.start_station == self.end_station:
            return (0.0, 0.0, [], [])

        priority_queue.enqueue((0, self.start_station))
        end_lng = float(self.stations_info[self.end_station].get_lng())
        end_lat = float(self.stations_info[self.end_station].get_lat())

        while not priority_queue.is_empty():
            current_station = priority_queue.dequeue()[1]
            if current_station == self.end_station:
                break

            visited_stations[current_station] = True
            for neighbor, travel_info in self.adjacency_list[current_station].items():
                if neighbor in closed_list:
                    continue

                travel_cost = travel_info["cost"]
                if travel_info["method"] == "train":
                    travel_cost = self.convert_to_time(travel_cost)

                tentative_time = time_map[current_station] + travel_info["cost"]
                if tentative_time < time_map[neighbor]:
                    time_map[neighbor] = tentative_time
                    previous_stations[neighbor] = current_station
                    distance_estimate = self.heuristic.euclidian(
                        float(self.stations_info[neighbor].get_lat()),
                        float(self.stations_info[neighbor].get_lng()),
                        end_lat,
                        end_lng,
                    )
                    heuristic = self.convert_to_time(distance_estimate)
                    priority_queue.enqueue((time_map[neighbor] + heuristic, neighbor))

        if self.end_station not in previous_stations or current_station != self.end_station:
            return (0.0, 0.0, [], [])
        
        return self.reconstruct_path(previous_stations)

    def k_shortest_path(self, k) -> List[Tuple[float, float, List[str], List[str]]]:
        first_path = self.a_star()
        if not first_path[2]:
            return []

        shortest_paths = [first_path]
        possible_paths = LL()

        for _ in range(1, k):
            previous_path = shortest_paths[-1]
            _, _, route, _ = previous_path

            for i in range(len(route) - 1):
                removed_edges = []
                for j in range(len(shortest_paths)):
                    if j < len(shortest_paths) and shortest_paths[j][2][:i] == route[:i]:
                        u = shortest_paths[j][2][i]
                        v = shortest_paths[j][2][i + 1]
                        
                        if v in self.adjacency_list[u]:
                            removed_edges.append((u, v, self.adjacency_list[u][v]))
                            del self.adjacency_list[u][v]

                new_path = self.a_star()
                spur_route = new_path[2]

                for (u, v, edge_info) in removed_edges:
                    self.adjacency_list[u][v] = edge_info

                if spur_route:
                    new_route = route[:i] + spur_route
                    distance, _, _, names = new_path
                    time = 0.0
                    
                    for i in range(len(new_route) - 1):
                        u, v = new_route[i], new_route[i + 1]
                        
                        if v not in self.adjacency_list[u]:
                            continue
                        
                        travel_info = self.adjacency_list[u][v]
                        travel_cost = travel_info["cost"]
                        
                        if travel_info["method"] == "train":
                            time += self.convert_to_time(travel_cost)
                            if u not in self.interchange_stations:
                                time += 28
                            else:
                                time += 35
                                
                        elif travel_info["method"] == "transfer":
                            time += travel_cost
                        
                    possible_paths.append((distance, time, new_route, names))

            if not possible_paths:
                break
            
        possible_paths.merge_sort()
        for _ in range(0, k - 1):
            shortest_paths.append(possible_paths.dequeue())

        return shortest_paths

s1 = ["NS2","CC5","EW20","DT30"]
s2 = ["NS22","EW20"]
for item1 in s1:
    for item2 in s2:
        print(f"Shortest path from {item1} to {item2}:")
        
        # print(f"Breadth First Search")
        # x = ShortestPath(item1, item2).bfs()
        # distance,time,path,station_names = x[0], x[1], x[2], x[3]
        # print(f"Distance: {distance}")
        # print(f"Time: {time}")
        # print(f"Station Codes: {', '.join(path)}")
        # print(f"Station  Names: {', '.join(station_names)}")
        
        # x = ShortestPath(item1, item2).dijkstra()
        # print(f"Dijkstra's algorithm")
        # distance,time,path,station_names = x[0], x[1], x[2], x[3]
        # print(f"Distance: {distance}")
        # print(f"Time: {time}")
        # print(f"Station Codes: {', '.join(path)}")
        # print(f"Station  Names: {', '.join(station_names)}")
        
        # print(f"A* algorithm")
        # x = ShortestPath(item1, item2).a_star()
        # distance,time,path,station_names = x[0], x[1], x[2], x[3]
        # print(f"Distance: {distance}")
        # print(f"Time: {time}")
        # print(f"Station Codes: {', '.join(path)}")
        # print(f"Station  Names: {', '.join(station_names)}")
        
        print(f"using Yen's algorithm")
        paths = ShortestPath(item1, item2).k_shortest_path(3)
        for j in paths:
            x = list(j)
            # print(data)
            print(f"Distance: {x[0]}")
            print(f"Time: {x[1]}")
            codes = ', '.join(x[2])
            names = ', '.join(x[3])
            print(f"Station Codes: {codes}")
            print(f"Station  Names: {names}")