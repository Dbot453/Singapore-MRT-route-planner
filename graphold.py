########################################################################################################################
#TODO: work out a way to change the transfer time to distance for A* to work due to g(h) going to be manhattan distance
#TODO: work out a way to change the distance between stations to time for djikstra
#######################################################################################################################

class Graph:

    def generateAdjacencyList(self):
        stations = Graph.generateStationData()
        adjacencyList = {}
        for k in stations:
            temp = stations[k]
            adjacencyList[k] = temp[6]
        return adjacencyList
    
    def generateStationInfo(self):
        stations = Graph.generateStationData()
        info = {}
        for k in stations:
            temp = stations[k]
            info[k] = temp[0:5]
        return info
    
    def generateStationData():  
        #adding stations   
        with open("stations.csv", 'r') as stationsFile:
            stations = {}
            distances = {}
            for line in stationsFile:
                line = line.strip()
                fields = line.split(",")
                adj_stations = []
                
                if fields[0] != "Station_Code":
                    result = []
                    result.append(fields[1])
                    for field_index in range(2, len(fields)-1):
                        result.append(fields[field_index])
                    adj_stations = fields[len(fields)-1].split("#")
                    result.append(adj_stations)
                    result.append({})
                    stations[fields[0]] = result

        #adding the distances
        with open("distances.csv", 'r') as distancesFile:
            for line in distancesFile:
                line = line.strip()
                fields = line.split(",")      
                
                #Station1,Station2,Line,Distance (km)
                if fields[0] != "Station1":
                    station1 = fields[0]
                    station2 = fields[1]
                    distance = float(fields[3])
                    
                    info = stations[station1]#get the station info
                    connections = info[6]#get the connections
                    connections[station2] = distance#add the distance to the connections
                    info[6] = connections #update the connections
                    stations[station1] = info #update the station info
                    
                    info = stations[station2]
                    connections = info[6]
                    connections[station1] = distance
                    info[6] = connections
                    stations[station2] = info
                                
        # add transfer distances   
        with open("transfer timings.csv", 'r') as transfersFile:
            for line in transfersFile:
                line = line.strip()
                fields = line.split(",")
                
                #Station Name,Start Line,Start Code,End Line,End Code,Transfer time in seconds
                if fields[0] != "Station Name":
                    station1 = fields[2]
                    station2 = fields[4]
                    
                    connections = {}
                    info = stations[station1]
                    connections = info[6]
                    connections[station2] = float(fields[5])*1.5 #TODO: work out how to change time to distance currently it is walking distance
                    info[6] = connections 
                    stations[station1] = info
                    
                    info = stations[station2]
                    connections = info[6]
                    connections[station1] = float(fields[5])*1.5
                    info[6] = connections
                    stations[station2] = info
        
        errors = []
        for k in stations:
            temp = stations[k]
            if len(temp[6].keys()) != len(temp[5]):
                for i in temp[5]:
                    if i not in temp[6].keys():
                        errors.append(f"{k} to {i} is missing in stations")

        if len(errors) > 0:
            for i in errors:
                raise Exception(i)
        
        return stations 