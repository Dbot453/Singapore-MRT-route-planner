##########################
# GROUP A Skill : OOP    #
##########################
from Location import Location

class Station(Location):
    def __init__(self, station_code: str, station_name: str, line_colour: str, line_name: str, lat: float, lng: float, adjacent_stations: list[str]):
        super().__init__(lat, lng)
        self.__station_code = station_code
        self.__station_name = station_name
        self.__line_colour = line_colour
        self.__line_name = line_name
        self.__adjacent_stations = adjacent_stations
        self.__connections = {}
        self.validate_data()

    def __str__(self) -> str:
        return f"{self.__station_code}, {self.__station_name}, {self.__line_colour}, {self.__line_name}, {self.lat}, {self.lng}, {self.__adjacent_stations}, {self.__connections}"

    def validate_data(self):
        if not self.__station_code or not isinstance(self.__station_code, str):
            raise ValueError("Invalid station code")
        if not self.__station_name or not isinstance(self.__station_name, str):
            raise ValueError("Invalid station name")
        # Add more validation as needed

    def get_adjacent_stations(self) -> list[str]:
        return self.__adjacent_stations

    def set_adjacent_stations(self, adjacent_stations: list[str]):
        self.__adjacent_stations = adjacent_stations

    def get_connections(self) -> dict[str, str]:
        return self.__connections

    def set_connections(self, connections: dict[str, str]):
        self.__connections = connections

    def get_station_code(self) -> str:
        return self.__station_code

    def get_station_name(self) -> str:
        return self.__station_name

    def get_line_color(self) -> str:
        return self.__line_colour

    def get_line_name(self) -> str:
        return self.__line_name

    def get_connection(self, station_code: str) -> str:
        return self.__connections.get(station_code)
    
    def get_lng(self) -> float:
        return self.lng
    
    def get_lat(self) -> float:
        return self.lat

    def add_connection(self, station_code: str, connection_info: str):
        if station_code not in self.__connections:
            self.__connections[station_code] = connection_info
        else:
            raise ValueError("Connection already exists")

    def remove_connection(self, station_code: str):
        if station_code in self.__connections:
            del self.__connections[station_code]
        else:
            raise ValueError("Connection does not exist")