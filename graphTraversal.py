from Station import Station as s
from Graph import Graph as g
from random import randint
from Utilities import maths
from Queue import PriorityQueue as PQ
import numpy as np
import math as m

class getShortestPath:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.open = PQ()
        self.closed = []
        self.path = []
        self.cost = 0
        self.s = s()
        
    def haversine(lat1:float, lng1:float, lat2:float, lng2:float):
        lat1 = m.radians(lat1)
        lat2 = m.radians(lat2)
        lon1 = m.radians(lng1)
        lon2 = m.radians(lng2)
        d_lat = lat2 - lat1
        d_lon = lon2 - lon1
        R = 6371.0

        a = pow(np.sin(d_lat/2),2)
        root_a = m.sqrt(a)
        root_1_a = m.sqrt(1-a)
        c = 2 * m.atan2(root_a, root_1_a)
        latitudeDistance = R * c # R is the Earth's radius, 6,371km
        
        a = pow(np.sin(d_lon/2),2)
        root_a = m.sqrt(a)
        root_1_a = m.sqrt(1-a)
        c = 2 * m.atan2(root_a, root_1_a)
        longitudeDistance = R * c
        
        #manhattan distance
        return maths.mod(latitudeDistance) + maths.mod(longitudeDistance)
    
    def djikstra(start, end): 
        graph = g.generateAdjacencyList()
        q = PQ()
        visited = {}
        distances = {}
        previous = {}
        current = start
        
        
        for v in graph:
            if v != start:
                visited[v] = False
                distances[v] = m.inf
            else:
                visited[start] = True
                distances[start] = 0
                
        # {station : { adj_station : distance}}
        
        for station in graph.keys():
            if station != start:
                previous[station] = None
                distances[station] = m.inf
            q.enqueue((0, start))
        
        while not q.is_empty():
            current = q.dequeue()[1]
            visited[current] = True
            
            for neighbour in graph[current]:
                if not visited[neighbour]:
                    if distances[current] + graph[current][neighbour] < distances[neighbour]:
                        distances[neighbour] = distances[current] + graph[current][neighbour]
                        previous[neighbour] = current
                        q.enqueue((distances[neighbour], neighbour))
                        
                        
        stations = g.generateStationData()
        current = end
        path = []
        temp = ""
        
        while current != start:
            path.append(current)
            current = previous[current]
        path.append(start)   
        path.reverse()
        
        station_info = []
        station_name = []
        for j in range(len(path)):
            station_name.append(stations[path[j]][0])
            station_info.append(stations[path[j]])
        
        names = ""
        lines = ""
        codes = ""
        
        for i in range(len(station_name)):
            if i == len(station_name)-1:
                names = f"{names} {path[i]}/{station_name[i]}"
            else:
                names = f"{names} {path[i]}/{station_name[i]} -> "
                

        return [stations[start][0],stations[end][0],f"{distances[end]:.2f} ",names]
    
    def Astar(start, end): 
        graph = g.generateAdjacencyList()
        stations = g.generateStationData()
        q = PQ()
        visited = {}
        distances = {}
        previous = {}
        current = start
        
        
        for v in graph:
            if v != start:
                visited[v] = False
                distances[v] = m.inf
            else:
                visited[start] = True
                distances[start] = 0
        
        for station in graph.keys():
            if station != start:
                previous[station] = None
                distances[station] = m.inf
            q.enqueue((0, start))
        
        end_long = float(stations[end][3])
        end_lat = float(stations[end][4])
        
        while not q.is_empty():
            current = q.dequeue()[1]
            visited[current] = True
            
            for neighbour in graph[current]:
                if not visited[neighbour]:
                    if distances[current] + graph[current][neighbour] < distances[neighbour]:
                        distances[neighbour] = distances[current] + graph[current][neighbour]
                        previous[neighbour] = current
                        q.enqueue((distances[neighbour] + getShortestPath.haversine(float(stations[neighbour][3]), float(stations[neighbour][4]), end_lat, end_long), neighbour))
                        
                        
        current = end
        path = []
        temp = ""
        
        while current != start:
            path.append(current)
            current = previous[current]
        path.append(start)   
        path.reverse()
        
        station_info = []
        station_name = []
        for j in range(len(path)):
            station_name.append(stations[path[j]][0])
            station_info.append(stations[path[j]])
        
        names = ""
        lines = ""
        codes = ""
        
        for i in range(len(station_name)):
            if i == len(station_name)-1:
                names = f"{names} {path[i]}/{station_name[i]}"
            else:
                names = f"{names} {path[i]}/{station_name[i]} -> "
                

        return [stations[start][0],stations[end][0],f"{distances[end]:.2f} ",names]


print(getShortestPath.djikstra("NS5", "NS20"))
print(getShortestPath.Astar("NS5", "NS20"))