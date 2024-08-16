import math
line_and_codes = {"NS":"North South Line","EW":"East West Line","NE":"North East Line","CC":"Circle Line","CE":"Circle Line","DT":"Downtown Line","TE":"Thomson East Coast Line","CG":"Changi Airport Branch Line"}
line_and_colour = {"NS":"Red","EW":"Green","NE":"Purple","CC":"Yellow","CE":"Yellow","DT":"Blue","TE":"Brown","CG":"Green"}

class graph:
      
    def djikstra(self, start, end):
        stations = {}
        distances = {}
        
        with open("stations.csv", 'r') as stations_file:
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
                    
        station_codes = stations.keys()
        distance_station_codes = []
        
        with open("distances.csv", 'r') as distances_file:
            for line in distances_file:
                line = line.strip()
                fields = line.split(",")      
                
                distance_station_codes.append(fields[0])
                distance_station_codes.append(fields[1])
                
                if fields[0] != "Station1":
                    station_value = stations[fields[0]]#station 1 in distances.csv
                    set = station_value[6]#copies the set from the station_value
                    set[fields[1]] = fields[3]#adds the distance from station 1 to station 2 to the set
                    station_value[6] = set #copies the set back to the station_value
                    stations[fields[0]] = station_value
                    
                    station_value = stations[fields[1]]#station 2 in distances.csv
                    set = station_value[6]
                    set[fields[0]] = fields[3]
                    station_value[6] = set
                    stations[fields[1]] = station_value
                
                    # station_value = stations[fields[1]]
                    # adj_stations = station_value[5]
                    # temp[fields[0]] = fields[3]
                    # station_value.append(temp)
                    # stations[fields[1]] = station_value
            
        # print(stations)
        for k in stations:
            if len(stations[k][6]) != len(stations[k][5]):
                for i in stations[k][5]:
                    if i not in stations[k][6]:
                        print(f"{k} to {i} is missing in distances.csv")
    
               
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
        # while current != end:
        #     for i in range(0,len(stations[current])):
        #         if visited[i] == False:
        #             if distances[i] > distances[current]+distances[f"{current} {stations[current][2][i]}"]:
        #                 distances[i] = distances[current]+distances[f"{current} {stations[current][2][i]}"]
        #     visited[current] = True
        #     current = distances.index(min(distances))
        
       
    
graph().djikstra("NS2","CC18")