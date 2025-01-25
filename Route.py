##########################
# GROUP A Skill : OOP    #
##########################
from Location import Location

class Route():

    def __init__(self, start_station: str, dest_station: str, distance: float, travel_time: float, path_codes: str, path_names: str, user_id: int):

        self.__start_station = start_station
        self.__dest_station = dest_station
        self.__distance = distance
        self.__travel_time = travel_time
        self.__path_codes = path_codes
        self.__path_names = path_names
        self.__user_id = user_id

    def __str__(self) -> str:
        return f"{self.__start_station}, {self.__dest_station}, {self.__distance}, {self.__travel_time}, {self.__path_codes}, {self.__path_names}, {self.__user_id}"
    
    def get_start_station(self) -> str:
        return self.__start_station
    
    def get_dest_station(self) -> str:
        return self.__dest_station
    
    def get_distance(self) -> float:
        return self.__distance
    
    def get_travel_time(self) -> float:
        return self.__travel_time
    
    def get_path_codes(self) -> str:
        return self.__path_codes
    
    def get_path_names(self) -> str:
        return self.__path_names
    
    def get_user_id(self) -> int:
        return self.__user_id
    
