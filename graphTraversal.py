from graph import Graph
from utilities import maths
from custom_queue import PriorityQueue as PQ
import numpy as np
import math as m

def GetShortestPathStatic(start: str, end: str, algorithm: SyntaxError):
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
        self.__closed = []

        # *** only need to call graph() once to get an instance
        my_graph = Graph()
        self.__adjacency_list = my_graph.get_adjacency_list()
        self.__stations = my_graph.get_station_info()

    def haversine(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """
        Haversine formula used to calculate the distance between two points takes latitude and longitude of two points as arguments returns the absolute value of the distance as float
        """
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
                    if distances[current] + self.__adjacency_list[current][neighbour] < distances[neighbour]:
                        distances[neighbour] = distances[current] + self.__adjacency_list[current][neighbour]
                        previous[neighbour] = current
                        queue.append(neighbour)

        current = self.__end
        path = []

        while current != self.__start:
            path.append(current)
            current = previous[current]
        path.append(self.__start)
        path.reverse()

        #station_names = [self.__stations[station][0] for station in path]

        #*** compare to the above line if they are the same
        station_names = [self.__stations[station].get_station_name() for station in path]

        return f"{distances[self.__end]:.2f}", path, station_names

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
            priority_queue.enqueue((0, self.__start))

        while not priority_queue.is_empty():
            current = priority_queue.dequeue()[1]
            visited[current] = True

            for neighbour in self.__adjacency_list[current]:
                if not visited[neighbour]:
                    if distances[current] + self.__adjacency_list[current][neighbour] < distances[neighbour]:
                        distances[neighbour] = distances[current] + self.__adjacency_list[current][neighbour]
                        previous[neighbour] = current
                        priority_queue.enqueue((distances[neighbour], neighbour))

        current = self.__end
        path = []

        while current != self.__start:
            path.append(current)
            current = previous[current]
        path.append(self.__start)
        path.reverse()

        #station_names = [self.__stations[station][0] for station in path]

        #*** compare to the above line if they are the same
        station_names = [self.__stations[station].get_station_name() for station in path]

        return f"{distances[self.__end]:.2f}", path, station_names
    
    def a_star(self) -> str:
        #A* algorithm to find the shortest path between two stations takes start and end as arguments returns a tuple of start, end, distance, path, station_names
        priority_queue = PQ()
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
            priority_queue.enqueue((0, self.__start))

        # *** this is wrong, otherway around
        #end_long = float(self.__stations[self.__end][3])
        #end_lat = float(self.__stations[self.__end][4])
        #
        #end_long = float(self.__stations[self.__end][4])
        #end_lat = float(self.__stations[self.__end][3])

        end_long = float(self.__stations[self.__end].get_lng())
        end_lat = float(self.__stations[self.__end].get_lat())

        while not priority_queue.is_empty():
            current = priority_queue.dequeue()[1]
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
                    heuristic = self.haversine(float(self.__stations[neighbour].get_lat()), float(self.__stations[neighbour].get_lng()), end_lat, end_long)

                    priority_queue.enqueue((distances[neighbour] + heuristic, neighbour))

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

        station_names = [self.__stations[station].get_station_name() for station in path]

        return f"{distances[self.__end]:.2f}", path, station_names
    
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
        
        #result = []
        for distance, path in A:
            station_names = [self.__stations[station].get_station_name() for station in path]
            # only need the first best path and exit
            return (distance, path, station_names)
            

            
        #return result
