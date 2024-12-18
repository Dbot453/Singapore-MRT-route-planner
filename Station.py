class Station:
    def __init__(self, station_Code,station_name,line_color,line_name,lat,lng):
        self.__station_code = station_Code
        self.__station_name = station_name
        self.__line_color = line_color
        self.__line_name = line_name
        self.__lat = lat
        self.__lng = lng
        self.__adjacent_stations = []
        self.__connections = {}

    def __init__(self, station_Code,station_name,line_color,line_name,lat,lng, adjacent_stations):
        self.__station_code = station_Code
        self.__station_name = station_name
        self.__line_color = line_color
        self.__line_name = line_name
        self.__lat = lat
        self.__lng = lng
        self.__adjacent_stations = adjacent_stations
        self.__connections = {}

    def set_adjacent_stations(self, adjacent_stations ):
        self.__adjacent_stations = adjacent_stations 

    def get_adjacent_stations(self):
        return self.__adjacent_stations
    
    def set_connections(self, connections ):
        self.__connections = connections 

    def get_connections(self):
        return self.__connections
    
    def get_station_code(self):
        return self.__station_code
    
    def get_station_name(self):
        return self.__station_name
    
    def get_line_color(self):
        return self.__line_color

    def get_line_name(self):
        return self.__line_name
    
    def get_lat(self):
        return self.__lat

    def get_lng(self):
        return self.__lng