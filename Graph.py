########################################################################################################################
#TODO: work out a way to change the transfer time to distance for A* to work due to g(h) going to be manhattan distance
#TODO: work out a way to change the distance between stations to time for djikstra
########################################################################################################################

class Graph:
    def __init__(self):
        self.stations = {}
        self.adjacency_list = {}
        self.station_info = {}
        Graph.generate_station_data(self)

    def generate_station_data(self):
        self._add_stations()
        self._add_connection_distances()
        self._add_transfer_distances()
        self._validate_station_data()
        self._populate_adjacency_list()
        self._populate_station_info()

    def _add_stations(self):
        with open("data/stations.csv", 'r') as stations_file:
            for line in stations_file:
                line = line.strip()
                fields = line.split(",")
                adj_stations = []

                if fields[0] != "Station_Code":
                    result = []
                    result.append(fields[1])
                    for i in range(2, len(fields) - 1):
                        result.append(fields[i])
                    adj_stations = fields[len(fields) - 1].split("#")
                    result.append(adj_stations)
                    result.append({})
                    self.stations[fields[0]] = result

    def _add_connection_distances(self):
        with open("data/distances.csv", 'r') as distances_file:
            for line in distances_file:
                line = line.strip()
                fields = line.split(",")

                if fields[0] != "Station1":
                    station1 = fields[0]
                    station2 = fields[1]
                    distance = float(fields[3])

                    self._update_connections(station1, station2, distance)
                    self._update_connections(station2, station1, distance)
                    
    def _add_transfer_distances(self):
        with open("data/transfer timings.csv", 'r') as transfers_file:
            for line in transfers_file:
                line = line.strip()
                fields = line.split(",")

                if fields[0] != "Station Name":
                    station1 = fields[2]
                    station2 = fields[4]
                    distance = float(fields[5]) * 1.5 #TODO: work out how to change time to distance currently it is walking distance

                    self._update_connections(station1, station2, distance)
                    self._update_connections(station2, station1, distance)

    def _update_connections(self, station1, station2, distance):
        info = self.stations[station1]
        connections = info[6]
        connections[station2] = distance
        info[6] = connections
        self.stations[station1] = info

    def _validate_station_data(self):
        errors = []
        for k in self.stations:
            temp = self.stations[k]
            if len(temp[6].keys()) != len(temp[5]):
                for i in temp[5]:
                    if i not in temp[6].keys():
                        errors.append(f"{k} to {i} is missing in stations")

        if errors:
            for error in errors:
                raise Exception(error)

    def _populate_adjacency_list(self):
        for k in self.stations:
            temp = self.stations[k]
            self.adjacency_list[k] = temp[6]

    def _populate_station_info(self):
        for k in self.stations:
            temp = self.stations[k]
            self.station_info[k] = temp[0:5]

    def get_adjacency_list(self):
        return self.adjacency_list

    def get_station_info(self):
        return self.station_info