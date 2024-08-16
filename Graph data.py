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
                    
                    stations[fields[0]] = result

        with open("distances.csv", 'r') as distances_file:
            for line in distances_file:
                line = line.strip()
                fields = line.split(",")      
                result = []
                
                if fields[0] != "Station1":
                    temp = f"{fields[0]} {fields[1]}"
                    distances[temp] = fields[3]
            
        print(distances)      
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
       
    
graph().djikstra("Jurong East","Bayfront")