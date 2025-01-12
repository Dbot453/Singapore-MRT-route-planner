##########################
# GROUP A Skill : OOP    #
##########################
class Station:
    def __init__(self, station_Code: str, station_name: str, line_colour: str, line_name: str, lat: float, lng: float, adjacent_stations: list[str]):
        self.__station_code= station_Code
        self.__station_name= station_name
        self.__line_colour = line_colour
        self.__line_name= line_name
        self.__lat= lat
        self.__lng= lng
        self.__adjacent_stations= adjacent_stations
        self.__connections= {}
        
    def __str__(self) -> str:
        return f"
            {self.__station_code}, {self.__station_name}, {self.__line_colour}, 
            {self.__line_name}, {self.__lat}, {self.__lng}, 
            {self.__adjacent_stations}, {self.__connections}
        "

    def set_adjacent_stations(self, adjacent_stations):
        self.__adjacent_stations = adjacent_stations 

    
    def set_connections(self, connections):
        self.__connections = connections 
           
    def get_adjacent_stations(self) -> list[str]:
        return self.__adjacent_stations

    def get_connections(self) -> dict[str, str]:
        return self.__connections
    
    def get_connection(self, station_code: str) -> str:
        return self.__connections[station_code]
    
    def get_station_code(self) -> str:
        return self.__station_code
    
    def get_station_name(self) -> str:
        return self.__station_name
    
    def get_line_color(self) -> str:
        return self.__line_colour

    def get_line_name(self) -> str:
        return self.__line_name
    
    def get_lat(self) -> float:
        return self.__lat

    def get_lng(self) -> float:
        return self.__lng