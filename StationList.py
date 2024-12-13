from Station import Station

def get_all_stations():
    station_list = {}
    with open("data/stations.csv", 'r') as stations_file:
        for line in stations_file:
            line = line.strip()
            fields = line.split(",")
            #adj_stations = []

            # Station_Code,Station_Name,Line_Color,Line_Name,lat,lng,adjacent_stations
            #
            if len(fields) != 7:
                raise Exception(" Wrong station data file. Expecting 7 columns")
            
                # *** skip the first line with header
            if fields[0] != "Station_Code":
                station_code = fields[0]
                station_name = fields[1]
                line_color = fields[2]
                line_name = fields[3]
                lat = fields[4]
                lng = fields[5]
                adj_stations = fields[len(fields) - 1].split("#")
                station_list[station_code] = Station(station_code, station_name, line_color, line_name, lat, lng, adj_stations)
    return station_list

g_station_list = get_all_stations()