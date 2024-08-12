import math

class graph:
    def djikstra(self, start, end):
        with open("stations.csv", 'r') as file:
                    stations = {}
                    for line in file:
                        line = line.strip()
                        fields = line.split(",")
                        adj_stations = []
                        
                        if fields[0] != "Station_Code":
                            result = []
                            result.append(fields[1])
                            result.append(fields[0].split(" "))
                            for i in range(2, len(fields)-1):
                                result.append(fields[i])
                            adj_stations = fields[len(fields)-1].split("#")
                            result.append(adj_stations)
                            
                            stations[fields[1]] = result
                            
        visited = []
        distances = []                                        
        for keys in stations:
            if keys == start:
                visited.append(True)
                distances.append(0)
            else:
                visited.append(False)
                distances.append(math.inf)
        
        current = start
        for i in range(len(stations[current][6])):
            print(stations[current][6][i])
        # while current != end:
            # for i in range(len(stations[current][3])):
            #     if visited[stations[current][3][i]] == False:
            #         if distances[stations[current][3][i]] > distances[current] + 1:
            #             distances[stations[current][3][i]] = distances[current] + 1
            # min = math.inf
            # for i in range(len(distances)):
            #     if visited[i] == False and distances[i] < min:
            #         min = distances[i]
            #         current = i
            # visited[current] = True
          
                
        
        
        
    
graph().djikstra("Jurong East","Bayfront")