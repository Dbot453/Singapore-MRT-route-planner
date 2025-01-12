from Station import Station
from StationList import g_station_list

class Graph:
    def __init__(self):
        self.__station_list = g_station_list.copy()
        self.adjacency_list = {}
        self.station_info = {}
        self.interchange_stations = []
        Graph.generate_station_data(self)

    def generate_station_data(self):
        self._add_transfer_cost()
        self._add_connection_cost()
        self._populate_adjacency_list()

    def _add_stations(self):
        with open("data/stations.csv", 'r') as stations_file:
            for line in stations_file:
                line = line.strip()
                fields = line.split(",")
                adj_stations = []
                station_code = fields[0]
                station_name = fields[1]
                line_color = fields[2]
                line_name = fields[3]
                lat = fields[4]
                lng = fields[5]
                adj_stations = fields[len(fields) - 1].split("#")
                self.__station_list[station_code] = Station(station_code, station_name, line_color, line_name, lat, lng, adj_stations)

    def _add_connection_cost(self):
        with open("data/distances.csv", 'r') as distances_file:
            for line in distances_file:
                line = line.strip()
                fields = line.split(",")
                
                if len(fields) != 4:
                    raise Exception(" Wrong connection data file. Expecting 4 columns")

                if fields[0] != "Station1":
                    station1 = fields[0]
                    station2 = fields[1]
                    distance = float(fields[3])*1000
                    
                    self._update_connections(station1, station2, distance, "train")
                    self._update_connections(station2, station1, distance, "train")
                    
    def _add_transfer_cost(self):
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
        start_station = self.__station_list[station1]
        start_connection = start_station.get_connections()
        start_connection[station2] = {"cost": distance, "method": travel_method}
        start_station.set_connections(start_connection)

    def _populate_adjacency_list(self):
        for k in self.__station_list:
            temp = self.__station_list[k]
            self.adjacency_list[k] = temp.get_connections()

    def get_adjacency_list(self):
        return self.adjacency_list

    def get_station_info(self):
        return self.__station_list
    
    def get_interchange_stations(self):
        return self.interchange_stations
    