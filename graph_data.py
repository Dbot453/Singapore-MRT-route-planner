import math
from queue import PriorityQueue

class emptyqueueerror(Exception):
    pass

class pq:
    def __init__(self):
        self.__queue = []
        self.__head = 0
        self.__tail = 0
        
    def empty(self):
        return self.__head == self.__tail
    
    def isfull(self):
        return False
    
    def enqueue(self, value):
        for i in range(self.__head, self.__tail):
            if value > self.__queue[i]:
                self.__queue[i:] = [value] + self.__queue[i:]
                self.__tail += 1
        
    def dequeue(self):
        if not self.empty():
            value = self.__queue[self.__head]
            self.__head += 1
            return value
        else:
            return emptyqueueerror("Queue is empty")

class station:
    def __init__(self, code, name, line, adjacent, distance):
        self.__name = ""
        self.__line = ""
        self.__code = "" 
        self.__adjacent_distance = {}
        self.__adjacent_time = {}    
        
    def generate_stations():    
        with open("stations.csv", 'r') as stations_file:
            stations = {}
            distances = {}
            for line in stations_file:
                line = line.strip()
                fields = line.split(",")
                adj_stations = []
                
                if fields[0] != "Station_Code":
                    result = []
                    result.append(fields[1])
                    # result.append(fields[0].split(" "))
                    for i in range(2, len(fields)-1):
                        result.append(fields[i])
                    adj_stations = fields[len(fields)-1].split("#")
                    result.append(adj_stations)
                    result.append({})
                    stations[fields[0]] = result
                    
        with open("distances.csv", 'r') as distances_file:
            for line in distances_file:
                line = line.strip()
                fields = line.split(",")      
                
                #Station1,Station2,Line,Distance (km)
                if fields[0] != "Station1":
                    info = stations[fields[0]]#station 1 in distances.csv
                    connections = info[6]#copies the set from the station_value
                    connections[fields[1]] = float(fields[3])#adds the distance from station 1 to station 2 to the set
                    info[6] = connections #copies the set back to the station_value
                    stations[fields[0]] = info
                    
                    info = stations[fields[1]]#station 2 in distances.csv
                    connections = info[6]
                    connections[fields[0]] = float(fields[3])
                    info[6] = connections
                    stations[fields[1]] = info
                                
        # add transfer distances   
        with open("transfer timings.csv", 'r') as transfers:
            for line in transfers:
                line = line.strip()
                fields = line.split(",")
                #Station Name,Start Line,Start Code,End Line,End Code,Transfer time in seconds
                if fields[0] != "Station Name":
                    s1 = fields[2]
                    s2 = fields[4]
                    
                    connections = {}
                    info = stations[s1]
                    connections = info[6]
                    connections[s2] = float(fields[5])#in seconds
                    info[6] = connections 
                    stations[s1] = info
                    
                    info = stations[s2]
                    connections = info[6]
                    connections[s1] = float(fields[5])
                    info[6] = connections
                    stations[s2] = info
        
        for k in stations:
            temp = stations[k]
            if len(temp[6].keys()) != len(temp[5]):
                for i in temp[5]:
                    if i not in temp[6].keys():
                        print(f"{k} to {i} is missing in stations")
        
        # for k in stations:
        #     print(f"{k} has info {stations[k]} ") 
            
        return stations                     
    
class graph:
    def djikstra(self, start, end):
        stations = station.generate_stations()
        visited = { node: False for node in stations}
        visited[start] = True
        distances = {node: math.inf for node in stations  }
        distances[start] = 0  # Set the source value to 0

        current = start
        while current != end:
            for neighbour in stations[current][6]:
                if visited[neighbour] == False:
                    new_distance = distances[current] + stations[current][6][neighbour]
                    if new_distance < distances[neighbour]:
                        distances[neighbour] = new_distance
            visited[current] = True

         
station.generate_stations()

# prq = PriorityQueue(20)
# print(prq.empty())
# prq.put(5)
# prq.put(3)
# prq.put(3)
# prq.put(1)
# print(prq.empty())
# print(prq.get())
# print(prq.get())
# print(prq.get())
# print(prq.get())

# print(prq.empty())

priority_queue = pq()
priority_queue.empty()
priority_queue.enqueue(5)
priority_queue.enqueue(3)
priority_queue.enqueue(3)
priority_queue.enqueue(1)
priority_queue.empty()
print(priority_queue.dequeue())
print(priority_queue.dequeue())
print(priority_queue.dequeue())
print(priority_queue.dequeue())

print(priority_queue.isempty())
