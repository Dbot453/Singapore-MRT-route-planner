########################################################################################################################
#TODO: work out a way to change the transfer time to distance for A* to work due to g(h) going to be manhattan distance
#TODO: work out a way to change the distance between stations to time for djikstra
#######################################################################################################################

class Station:
    # def __init__(self, code, name, line, longitude, latitiude):
    #     self.name = name
    #     self.code = code
    #     self.line = line
    #     self.long = longitude
    #     self.lat = latitiude
    #     self.adjacentStations = []
        
    # def getName(self):
        
        
    def generateData():  
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
                    for i in range(2, len(fields)-1):
                        result.append(fields[i])
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
                    s1 = fields[0]
                    s2 = fields[1]
                    d = float(fields[3])
                    
                    info = stations[s1]
                    connections = info[6]
                    connections[s2] = d
                    info[6] = connections 
                    stations[s1] = info
                    
                    info = stations[s2]
                    connections = info[6]
                    connections[s1] = d
                    info[6] = connections
                    stations[s2] = info
                                
        # add transfer distances   
        with open("transfer timings.csv", 'r') as transfersFile:
            for line in transfersFile:
                line = line.strip()
                fields = line.split(",")
                
                #Station Name,Start Line,Start Code,End Line,End Code,Transfer time in seconds
                if fields[0] != "Station Name":
                    s1 = fields[2]
                    s2 = fields[4]
                    
                    connections = {}
                    info = stations[s1]
                    connections = info[6]
                    connections[s2] = float(fields[5])*1.3/1000 #TODO: work out how to change time to distnace
                    info[6] = connections 
                    stations[s1] = info
                    
                    info = stations[s2]
                    connections = info[6]
                    connections[s1] = float(fields[5])*1.3/1000
                    info[6] = connections
                    stations[s2] = info
        
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
    
    def generateAdjacencyList():
        stations = Station.generateData()
        adjacencyList = {}
        for k in stations:
            temp = stations[k]
            adjacencyList[k] = temp[6]
        return adjacencyList
    
    def generateStationData():
        stations = Station.generateData()
        info = {}
        for k in stations:
            temp = stations[k]
            info[k] = temp[0:5]
        return info
    