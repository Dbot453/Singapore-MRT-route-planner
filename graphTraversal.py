import numpy as np
import math as m
from typing import List, Tuple, Dict

from Graph import Graph
from Station import Station as S
from Station import Location as L
from heuristics import DistanceHeuristic as DH
from custom_implementations.custom_queue import PriorityQueue as PQ
from custom_implementations.custom_queue import Queue as Q
from custom_implementations.custom_stack import Stack as S
from custom_implementations.linked_list import LinkedList as LL
from Route import Route
import sqlite3

def GetShortestPathStatic(start_station: str, end_station: str, algorithm: str) -> Tuple[str, str, List[str], List[str]]:
    shortest_path_calculator = ShortestPath(start_station, end_station)
    result = {}
    
    if algorithm == '1':
        data = shortest_path_calculator.bfs()
        result[1] = data
    elif algorithm == '2':
        data = shortest_path_calculator.dijkstra()
        result[1] = data
    elif algorithm == '3':
        data = shortest_path_calculator.a_star()
        result[1] = data
    else:
        data = shortest_path_calculator.k_shortest_path(2)
        for j,k in enumerate(data):
            result[j+1] = k
        
    return result
    #TODO: make it so that k_shortest paths usese a different function to get the shortest path

def SaveRouteToDBStatic(routes: List[Route]):

    import datetime

    db_connection = sqlite3.connect("instance/database.db")
    cursor = db_connection.cursor()

    # save route  data
    for r in routes:
        start = r.get_start_station()
        dest = r.get_dest_station()
        distance = r.get_distance()
        travel_time = r.get_travel_time()
        path_codes = r.get_path_codes()
        path_names = r.get_path_names()
        user_id = r.get_user_id()

        sql_query = "INSERT INTO route (start, dest, distance, travel_time, path_codes, path_names, user_id, save_datetime) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(sql_query, ( start, dest, distance, travel_time, path_codes, path_names, user_id, datetime.datetime.now()))

    db_connection.commit()
    db_connection.close()


class ShortestPath:
    def __init__(self, start_station: str, end_station: str):
        self.start_station = start_station
        self.end_station = end_station
        self.heuristic = DH()
        self.graph = Graph()
        self.adjacency_list = self.graph.get_adjacency_list()
        self.stations_info = self.graph.get_station_info()
        self.interchange_stations = self.graph.get_interchange_stations()
        
        self.INVALID = 0.0, 0.0, [], []
        self.CRUISE_SPEED = 27.8     # m/s
        self.ACCELERATION = 1.0      # m/s^2
        self.REGULAR_STOPPING_TIME = 28
        self.INTERCHANGE_STOPPING_TIME = 35

    def _evaluate_time_for_distance(self, distance_meters: float) -> float:
        accel_decel_distance = (self.CRUISE_SPEED ** 2) / self.ACCELERATION

        if distance_meters >= accel_decel_distance:
            #This formula is used when the distance is greater than the acceleration distance
            acceleration_time = self.CRUISE_SPEED / self.ACCELERATION
            accel_distance = 0.5 * self.ACCELERATION * (acceleration_time ** 2)
            cruise_distance = distance_meters - 2 * accel_distance
            cruise_time = cruise_distance / self.CRUISE_SPEED
            total_time = 2 * acceleration_time + cruise_time
            
        else:
            #This formula is used when the distance is less than the acceleration distance
            acceleration_time = m.sqrt(distance_meters / self.ACCELERATION)
            total_time = 2 * acceleration_time

        return total_time
    
    def _calculate_travel_cost(self,code,neighour,total_distance,total_time) -> Tuple[float, float]:
        
        travel_info = self.adjacency_list[code][neighour]
        travel_cost = travel_info["cost"]
        travel_method = travel_info["method"]

        if travel_method == "train":
            total_distance += travel_cost
            total_time += self._evaluate_time_for_distance(travel_cost)
            if code not in self.interchange_stations:
                total_time += self.REGULAR_STOPPING_TIME
            else:
                total_time += self.INTERCHANGE_STOPPING_TIME
                
        elif travel_method == "transfer":
            total_distance += total_distance
            
        return total_distance, total_time

    def reconstruct_path(self, previous: dict) -> Tuple[float, float, list[str], list[str]]:
        path = []
        current_station = self.end_station

        if current_station not in previous or previous[current_station] is None:
            return self.INVALID

        while current_station != self.start_station:
            if current_station not in previous:
                return self.INVALID
            
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
                
                total_distance, total_time = self._calculate_travel_cost(code,
                                                                        neighbour,
                                                                        total_distance,
                                                                        total_time)

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
        
        if self.start_station == self.end_station:
            return self.INVALID

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
                        distance_map[neighbour] = (distance_map[current_station] + self.adjacency_list[current_station][neighbour]["cost"])
                        previous[neighbour] = current_station
                        queue.enqueue(neighbour)
                        
        return self.reconstruct_path(previous)

    def dijkstra(self) -> Tuple[float, float, list, list]:
        
        if self.start_station == self.end_station:
            return self.INVALID
        
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
            return self.INVALID
        
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
        end_station_info = self.stations_info[self.end_station]
        end_lng = float(end_station_info.get_lng())
        end_lat = float(end_station_info.get_lat())

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
            return self.INVALID
        
        return self.reconstruct_path(previous_stations)

    def k_shortest_path(self, k) -> List[Tuple[float, float, List[str], List[str]]]:
        # K shortest path algorithm is an algorithm that finds the k shortest paths between two nodes in a graph
        
        # If the start and end stations are the same return an empty path
        if self.start_station == self.end_station:
            return [(self.INVALID)]
        
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
                        
                        distance, time = self._calculate_travel_cost(u, v, distance, time)
                        
                    possible_paths.append((distance, time, new_route, names))

            # If no more possible paths, break
            if not possible_paths:
                break
            
        # Sort the possible paths and add the shortest ones to the shortest paths list
        possible_paths.merge_sort()
        for _ in range(0, k - 1):
            shortest_paths.append(possible_paths.dequeue())

        return shortest_paths


station1 = ["NS1","EW24","CC5"]
station2 = ["DT1","NS5","CC5"]

for s1 in station1:
    for s2 in station2:
        print(f"Shortest path from {s1} to {s2}")
        x = ShortestPath(s1,s2).a_star()
        print(x)

if __name__ == "__main__":
    station1 = ["NS1", "EW24", "CC5"]
    station2 = ["DT1", "NS5", "CC5"]

    for s1 in station1:
        for s2 in station2:
            print(f"Shortest path from {s1} to {s2}")
            print("BFS:")
            x = ShortestPath(s1, s2).bfs()
            print(x)
            print("Dijkstra:")
            x = ShortestPath(s1, s2).a_star()
            print(x)
            print("A*:")
            x = ShortestPath(s1, s2).dijkstra()
            print(x)


            print("K Shortest Paths:")
            routes = [];
            x = ShortestPath(s1, s2).k_shortest_path(5)
            for i, path in enumerate(x):
                print(f"Path {i + 1}: {path}")
                distance_calc, time_calc, codes_calc, names_calc = path
                path_codes = ','.join(codes_calc)
                path_names = ','.join(names_calc)
                new_route = Route( 
                    start_station=s1,
                    dest_station=s2,
                    distance=distance_calc,
                    travel_time=time_calc,
                    path_codes=path_codes,
                    path_names=path_names,
                    user_id=0   # testing user id
                )

                routes.append(new_route)
            
            SaveRouteToDBStatic( routes)
        