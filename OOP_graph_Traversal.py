import numpy as np
import math as m
from typing import List, Tuple, Dict
import sqlite3

from Graph import Graph
from Route import Route
from Station import Station as S
from Station import Location as L
from heuristics import DistanceHeuristic as DH
from custom_implementations.custom_queue import PriorityQueue as PQ
from custom_implementations.custom_queue import Queue as Q
from custom_implementations.custom_stack import Stack as St
from custom_implementations.linked_list import LinkedList as LL


def GetShortestPathStatic(
    start_station: str, end_station: str, algorithm: str) -> Dict[int, Tuple[float, float, List[str], List[str]]]:
    sp = ShortestPath(start_station, end_station)
    result = {}

    if algorithm == "1":
        data = sp.run_bfs()
        result[1] = data
    elif algorithm == "2":
        data = sp.run_dijkstra()
        result[1] = data
    elif algorithm == "3":
        data = sp.run_a_star()
        result[1] = data
    else:
        data = sp.run_k_shortest_path(2)
        for i, path in enumerate(data):
            result[i + 1] = path

    return result

def SaveRouteToDBStatic(routes: List[Route]):

    import datetime

    db_connection = sqlite3.connect("website/database.db")
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

class RoutePlanner:
    def __init__(
        self, graph: Graph, start: str, end: str, interchange_stations: set, stations_info: dict):
        self.graph = graph
        self.start = start
        self.end = end
        self.interchange_stations = interchange_stations
        self.stations_info = stations_info
        self.adjacency_list = self.graph.get_adjacency_list()
        self.CRUISE_SPEED = 27.8
        self.ACCELERATION = 1.0
        self.REGULAR_STOPPING_TIME = 28
        self.INTERCHANGE_STOPPING_TIME = 35
        self.INVALID = (0.0, 0.0, [], [])

    def _evaluate_time_for_distance(self, distance_meters: float) -> float:
        accel_decel_distance = (self.CRUISE_SPEED ** 2) / self.ACCELERATION
        
        #This formula is used when the distance is greater than the acceleration distance
        if distance_meters >= accel_decel_distance:
            t_accel = self.CRUISE_SPEED / self.ACCELERATION
            accel_dist = 0.5 * self.ACCELERATION * (t_accel ** 2)
            cruise_dist = distance_meters - 2 * accel_dist
            cruise_time = cruise_dist / self.CRUISE_SPEED
            return 2 * t_accel + cruise_time
        
        #This formula is used when the distance is less than the acceleration distance
        else:
            return 2 * m.sqrt(distance_meters / self.ACCELERATION)

    def _calculate_travel_cost(self, code, neighbour, total_distance, total_time):
        # Get the cost of the method of traveln 
        info = self.adjacency_list[code][neighbour]
        cost, method = info["cost"], info["method"]

        if method == "train":
            total_distance += cost
            # Calculate the time taken to travel the distance
            total_time += self._evaluate_time_for_distance(cost)
            if code not in self.interchange_stations:
                total_time += self.REGULAR_STOPPING_TIME
            else:
                total_time += self.INTERCHANGE_STOPPING_TIME
        elif method == "transfer":
            total_distance += total_distance

        return total_distance, total_time

    # Reconstruct the path from the previous dictionary
    def _reconstruct_path(self, previous: dict) -> Tuple[float, float, list, list]:
        path = []
        curr = self.end

        if curr not in previous or previous[curr] is None:
            return self.INVALID

        while curr != self.start:
            if curr not in previous:
                return self.INVALID
            path.append(curr)
            curr = previous[curr]

        path.append(self.start)
        stack = St()

        while path:
            stack.push(path.pop())

        while not stack.is_empty():
            path.append(stack.pop())

        station_names = [self.stations_info[s].get_station_name() for s in path]
        total_distance = 0.0
        total_time = 0.0

        for i, code in enumerate(path):
            if i < len(path) - 1:
                nb = path[i + 1]
                if nb in self.adjacency_list[code]:
                    total_distance, total_time = self._calculate_travel_cost(
                        code, nb, total_distance, total_time
                    )

        return total_distance, total_time, path, station_names


class BFS_Algorithm(RoutePlanner):
    # Run the BFS algorithm
    def run(self) -> Tuple[float, float, List[str], List[str]]:
        if self.start == self.end:
            return self.INVALID

        q = Q()
        visited = {node: False for node in self.adjacency_list}
        dist = {node: m.inf for node in self.adjacency_list}
        prev = {node: None for node in self.adjacency_list}

        dist[self.start] = 0
        visited[self.start] = True
        q.enqueue(self.start)

        while not q.is_empty():
            current = q.dequeue()
            if current == self.end:
                break
            visited[current] = True

            for nb in self.adjacency_list[current]:
                if not visited[nb]:
                    cost = self.adjacency_list[current][nb]["cost"]
                    if dist[current] + cost < dist[nb]:
                        dist[nb] = dist[current] + cost
                        prev[nb] = current
                        q.enqueue(nb)

        return self._reconstruct_path(prev)


class Dijkstra_Algorithm(RoutePlanner):
    def run(self) -> Tuple[float, float, List[str], List[str]]:
        if self.start == self.end:
            return self.INVALID

        pq = PQ()
        visited = {node: False for node in self.adjacency_list}
        dist = {node: m.inf for node in self.adjacency_list}
        prev = {node: None for node in self.adjacency_list}

        dist[self.start] = 0
        pq.enqueue((0, self.start))

        while not pq.is_empty():
            current = pq.dequeue()[1]
            if current == self.end:
                break
            visited[current] = True

            for nb, info in self.adjacency_list[current].items():
                cost = info["cost"]
                if info["method"] == "train":
                    cost = self._evaluate_time_for_distance(cost)
                nd = dist[current] + cost

                if nd < dist[nb]:
                    dist[nb] = nd
                    prev[nb] = current
                    pq.enqueue((nd, nb))

        return self._reconstruct_path(prev)


class A_Star_Algorithm(RoutePlanner):
    def __init__(
        self, graph, start, end, interchange_stations, stations_info, heuristic):
        super().__init__(graph, start, end, interchange_stations, stations_info)
        self.heuristic = heuristic

    def run(self) -> Tuple[float, float, List[str], List[str]]:
        if self.start == self.end:
            return self.INVALID

        closed_set = set()
        pq = PQ()
        visited = {node: False for node in self.adjacency_list}
        t_map = {node: m.inf for node in self.adjacency_list}
        prev = {node: None for node in self.adjacency_list}

        t_map[self.start] = 0
        pq.enqueue((0, self.start))

        end_info = self.stations_info[self.end]
        end_lng = float(end_info.get_lng())
        end_lat = float(end_info.get_lat())

        while not pq.is_empty():
            current = pq.dequeue()[1]
            if current == self.end:
                break
            visited[current] = True
            closed_set.add(current)

            for nb, info in self.adjacency_list[current].items():
                if nb in closed_set:
                    continue
                cost = info["cost"]
                if info["method"] == "train":
                    cost = self._evaluate_time_for_distance(cost)

                tmp = t_map[current] + info["cost"]
                if tmp < t_map[nb]:
                    t_map[nb] = tmp
                    prev[nb] = current
                    d_est = self.heuristic.manhattan(
                        float(self.stations_info[nb].get_lat()),
                        float(self.stations_info[nb].get_lng()),
                        end_lat,
                        end_lng,
                    )
                    est = self._evaluate_time_for_distance(d_est)
                    pq.enqueue((t_map[nb] + est, nb))

        if self.end not in prev:
            return self.INVALID

        return self._reconstruct_path(prev)


class KShortestPathsAlgorithm(RoutePlanner):
    def __init__(
        self,
        graph,
        start,
        end,
        interchange_stations,
        stations_info,
        heuristic,
        k,
    ):
        super().__init__(graph, start, end, interchange_stations, stations_info)
        self.a_star_algo = A_Star_Algorithm(
            graph, start, end, interchange_stations, stations_info, heuristic
        )
        self.k = k

    def run(self) -> List[Tuple[float, float, List[str], List[str]]]:
        if self.start == self.end:
            return [self.INVALID]

        first_path = self.a_star_algo.run()
        if not first_path[2]:
            return []

        shortest = [first_path]
        possible = LL()

        for _ in range(1, self.k):
            route = shortest[-1][2]
            for i in range(len(route) - 1):
                removed_edges = []

                for j in range(len(shortest)):
                    if j < len(shortest) and shortest[j][2][:i] == route[:i]:
                        u = shortest[j][2][i]
                        v = shortest[j][2][i + 1]
                        if v in self.adjacency_list[u]:
                            removed_edges.append((u, v, self.adjacency_list[u][v]))
                            del self.adjacency_list[u][v]

                new_path = self.a_star_algo.run()
                spur_route = new_path[2]

                for (u, v, e_info) in removed_edges:
                    self.adjacency_list[u][v] = e_info

                if spur_route:
                    nr = route[:i] + spur_route
                    dist, time = 0.0, 0.0
                    for idx in range(len(nr) - 1):
                        u, v = nr[idx], nr[idx + 1]
                        if v in self.adjacency_list[u]:
                            dist, time = self._calculate_travel_cost(u, v, dist, time)
                    possible.append((dist, time, nr, new_path[3]))

            if not possible:
                break

        possible.merge_sort()

        for _ in range(self.k - 1):
            if possible.is_empty():
                break
            shortest.append(possible.dequeue())

        return shortest


class ShortestPath:
    def __init__(self, start_station: str, end_station: str):
        self.start = start_station
        self.end = end_station
        self.graph = Graph()
        self.interchange_stations = self.graph.get_interchange_stations()
        self.stations_info = self.graph.get_station_info()
        self.heuristic = DH()

    def run_bfs(self):
        return BFS_Algorithm(
            self.graph, self.start, self.end, self.interchange_stations, self.stations_info
        ).run()

    def run_dijkstra(self):
        return Dijkstra_Algorithm(
            self.graph, self.start, self.end, self.interchange_stations, self.stations_info
        ).run()

    def run_a_star(self):
        return A_Star_Algorithm(
            self.graph, self.start, self.end, self.interchange_stations, self.stations_info, self.heuristic
        ).run()

    def run_k_shortest_path(self, k):
        return KShortestPathsAlgorithm(
            self.graph,
            self.start,
            self.end,
            self.interchange_stations,
            self.stations_info,
            self.heuristic,
            k,
        ).run()


if __name__ == "__main__":
    station1 = ["NS1", "EW24", "CC5"]
    station2 = ["DT1", "NS5", "CC5"]

    for s1 in station1:
        for s2 in station2:
            print(f"Shortest path from {s1} to {s2}")
            print("BFS:")
            x = ShortestPath(s1, s2).run_bfs()
            print(x)
            print("Dijkstra:")
            x = ShortestPath(s1, s2).run_dijkstra()
            print(x)
            print("A*:")
            x = ShortestPath(s1, s2).run_a_star()
            print(x)
            print("K Shortest Paths:")
            x = ShortestPath(s1, s2).run_k_shortest_path(5)
            for i, path in enumerate(x):
                print(f"Path {i + 1}: {path}")
