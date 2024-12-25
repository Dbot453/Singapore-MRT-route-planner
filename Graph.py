########################################################################################################################
#TODO: work out a way to change the transfer time to distance for A* to work due to g(h) going to be manhattan distance
#TODO: work out a way to change the distance between stations to time for djikstra
########################################################################################################################

from Station import Station
from StationList import  g_station_list

class Graph:
    def __init__(self):
        self.stations = {}
        self.adjacency_list = {}
        self.station_info = {}
        self.interchange_stations = []
        Graph.generate_station_data(self)

    def generate_station_data(self):
        self._add_stations()
        self._add_connection_distances()
        self._add_transfer_distances()
        self._validate_station_data()
        self._populate_adjacency_list()
        #self._populate_station_info()
        
    def get_all_stations(self):
        return self.__station_list
    
    def _add_stations(self):
        self.__station_list = g_station_list

        with open("data/stations.csv", 'r') as stations_file:
           for line in stations_file:
               line = line.strip()
               fields = line.split(",")
               #adj_stations = []#
        
               # Station_Code,Station_Name,Line_Color,Line_Name,lat,lng,adjacent_stations
               #
               if len(fields) != 7:
                   raise Exception(" Wrong station data file. Expecting 7 columns")
        #       
                # *** skip the first line with header
               if fields[0] != "Station_Code":
                   #result = []
                   #result.append(fields[1])
                   #for i in range(2, len(fields) - 1):
                   #    result.append(fields[i])
                   #adj_stations = fields[len(fields) - 1].split("#")
                   #result.append(adj_stations)
                   # this dict is for connection
                   #result.append({})
                   #self.__stations[fields[0]] = result
                   #
                   # *** new class based approach
                   station_code = fields[0]
                   station_name = fields[1]
                   line_color = fields[2]
                   line_name = fields[3]
                   lat = fields[4]
                   lng = fields[5]
                   adj_stations = fields[len(fields) - 1].split("#")
                   self.__station_list[station_code] = Station(station_code, station_name, line_color, line_name, lat, lng, adj_stations)


    def _add_connection_distances(self):
        with open("data/distances.csv", 'r') as distances_file:
            for line in distances_file:
                line = line.strip()
                fields = line.split(",")

                # *** Skip the first header line
                # Station1,Station2,Line,Distance (km)
                if len(fields) != 4:
                    raise Exception(" Wrong connection data file. Expecting 4 columns")
                
                if fields[0] != "Station1":
                    station1 = fields[0]
                    station2 = fields[1]
                    
                    max_speed = 27.8  # m/s
                    acceleration = 1.0  # m/s^2
                    distance = float(fields[3])*1000
                    
                    self._update_connections(station1, station2, distance, "train")
                    self._update_connections(station2, station1, distance, "train")
                    
    def _add_transfer_distances(self):
        with open("data/transfer timings.csv", 'r') as transfers_file:
            
            for line in transfers_file:
                line = line.strip()
                fields = line.split(",")

                if fields[0] != "Station Name":
                    station1 = fields[2]
                    station2 = fields[4]
                    self.interchange_stations.append(station1)
                    self.interchange_stations.append(station2)
                    transfer_time = float(fields[5])
                    self._update_connections(station1, station2, transfer_time, "transfer")
                    self._update_connections(station2, station1, transfer_time, "transfer")

    def _update_connections(self, station1, station2, distance, travel_method):
        info = self.stations[station1]
        connections = info[6]
        connections[station2] = {"cost": distance, "method": travel_method}
        info[6] = connections
        self.stations[station1] = info

        # *** set connection for station 1
        start_station = self.__station_list[station1]
        start_connection = start_station.get_connections()
        start_connection[station2] = distance
        start_station.set_connections(start_connection)

    # Not clear what this function do 
    def _validate_station_data(self):
        errors = []
        for station_code in self.__station_list:
            station = self.__station_list[station_code]
            connections = station.get_connections()
            adjacent_stations = station.get_adjacent_stations()
            if len(connections.keys()) != len(adjacent_stations):
                for s in adjacent_stations:
                    if s not in connections:
                        errors.append(f"{station_code} to {s} is missing in stations")

        if errors:
            #    raise Exception with multiple errors
            raise Exception("\n".join(errors))

    def _populate_adjacency_list(self):
        for k in self.__station_list:
            #temp = self.__stations[k]
            #self.__adjacency_list[k] = temp[6]
            # *** new approach
            self.__adjacency_list[k] = self.__station_list[k].get_connections()
        return self.__station_list

    def get_adjacency_list(self):
        return self.__adjacency_list
    
    def get_station_info(self):
        return self.station_info
    
    def get_interchange_stations(self):
        return self.interchange_stations
    
# stations dictionary is station code : [station name, line, line colour, longitude, latitude, [adjacent stations], {adjacent stations : {distance :" an int", method"train / transfer"}}]"}}]
x = Graph()
print(x.stations)
print(x.adjacency_list)
print(x.interchange_stations)
