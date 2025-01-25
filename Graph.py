from Station import Station
from StationList import g_station_list
import sqlite3

class Graph:
    def __init__(self):
        self.__station_list = g_station_list.copy()
        self.adjacency_list = {}
        self.station_info = {}
        self.interchange_stations = []
        self.__read_db = True
        Graph.generate_station_data(self) 

    def generate_station_data(self):
        self._add_stations()
        self._add_transfer_cost()
        self._add_connection_cost()
        self._populate_adjacency_list()

    def _add_stations(self):
        if self.__read_db:
            db_connection = sqlite3.connect("website/database.db")
            cursor = db_connection.cursor()
            # # Get neighbour data
            neighbour_sql_query = "SELECT station_code, neighbour FROM adjacent_stations"
            cursor.execute(neighbour_sql_query)
            neighbour_output = cursor.fetchall()
            neighbours = {}
            for row in neighbour_output:
                station_code = row[0]
                neighbour = row[1]
                if station_code not in neighbours:
                    neighbours[station_code] = [neighbour]
                else:
                    neighbours[station_code].append(neighbour)
                    
                # Add reverse connection
                if neighbour not in neighbours:
                    neighbours[neighbour] = [station_code]
                else:
                    neighbours[neighbour].append(station_code)

            # Get station data
            station_sql_query = "SELECT station_code, station_name, line_colour,line_name, latitude, longitude  FROM station"
            cursor.execute(station_sql_query)
            output = cursor.fetchall()
            for row in output:
                station_code = row[0]
                station_name = row[1]
                line_color = row[2]
                line_name = row[3]
                lat = row[4]
                lng = row[5]
                adj_stations = neighbours[station_code]
                self.__station_list[station_code] = Station(station_code, 
                                                            station_name, 
                                                            line_color, 
                                                            line_name, 
                                                            lat, lng, 
                                                            adj_stations)
                db_connection.close()

        else:
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
                    self.__station_list[station_code] = Station(station_code, 
                                                                station_name, 
                                                                line_color, 
                                                                line_name, 
                                                                lat, lng, 
                                                                adj_stations)

    def _add_connection_cost(self):
        if self.__read_db:
            db_connection = sqlite3.connect("website/database.db")
            cursor = db_connection.cursor()
            # Get distance data
            sql_query = "SELECT station1, station2, distance FROM distance"
            cursor.execute(sql_query)
            output = cursor.fetchall()
            for row in output:
                station1 = row[0]
                station2 = row[1]
                distance = row[2]
                self._update_connections(station1, station2, distance, "train")
                self._update_connections(station2, station1, distance, "train")
            db_connection.close()

        else:
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
        if self.__read_db:
            db_connection = sqlite3.connect("website/database.db")
            cursor = db_connection.cursor()
            # Get transfer time data
            sql_query = "SELECT start_code, end_code, transfer_time_seconds FROM transfer_time"
            cursor.execute(sql_query)
            output = cursor.fetchall()
            for row in output:
                station1 = row[0]
                station2 = row[1]
                transfer_time = row[2]
                self._update_connections(station1, station2, transfer_time, "transfer")
                self._update_connections(station2, station1, transfer_time, "transfer")
            db_connection.close()

        else:
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
    