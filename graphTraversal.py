from Graph import Station as s
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
        self.open.put((0, start))
        self.path = []
        self.cost = 0
        
    def haversine(lat1, lng1, lat2, lng2):
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
        graph = s.generateAdjacencyList()
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
                        
                        
        stations = s.generateStationData()
        current = end
        path = []
        temp = ""
        while current != start:
            path.append(current)
            current = previous[current]
        path.append(start)   
        path.reverse()
        
        station_names = []
        for j in range(len(path)-1):
            station_names.append(stations[path[j]][0])
        station_names.append(stations[path[len(path)-1]][0])
        
        # for i in range(len(path)-1):
        #     temp = temp + path[i] + " -> "
        # temp = temp + path[len(path)-1]
        
        for i in range(len(station_names)):
            if i == len(station_names)-1:
                temp = temp + station_names[i]
            else:
                temp = temp + station_names[i] + " -> "
        
        return f"{temp} takes {distances[end]:.2f}km"     
       
# print(A_Star.haversine(1.333207,103.742308, 1.300747,103.855873))
info = s.generateData()

x = [*info.keys()]
for i in range(10):
    print(getShortestPath.djikstra(x[randint(0, len(x)-1)], x[randint(0, len(x)-1)]))




