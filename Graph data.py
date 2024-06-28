import math

# add placeholders for stations that are not in the list blue line, red line, yellow line, brown line
# add times to placeholder stations to be 0  - ignore them in later graph traversal 
# add interchange stations so that they have the correct station codes✓
# add file reading of timings for intersections

#blue line
#add a place holder station at dt4
DTL_stations = ["Bukit Panjang","Cashew", "Hillview" ,"PLACEHOLDER FOR Hume", "Beauty World", "King Albert Park", 
               "Sixth Avenue", "Tan Kah Kee", "Botanic Gardens", "Stevens", "Newton", "Little India", "Rochor", 
               "Bugis", "Promenade", "Bayfront", "Downtown", "Telok Ayer", "Chinatown", "Fort Canning", "Bencoolen", 
               "Jalan Besar", "Bendemeer", "Geylang Bahru", "Mattar", "MacPherson", "Ubi", "Kaki Bukit","Bedok North", 
               "Bedok Reservoir", "Tampines West", "Tampines", "Tampines East", "Upper Changi", "Expo"]

DT_times= [2,2,0,0,2,2,2,3,3,3,3,4,2,3,3,3,2,3,4,2,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2]

#purple line
NEL_stations = ["Punggol","Sengkang", "Buangkok", "Hougang", "Kovan", "Serangoon", "Woodleigh", "Potong Pasir", 
               "Boon Keng", "Farrer Park", "Little India", "Dhoby Ghaut", "Clark Quay", "Chinatown", "Outram Park", 
               "Harbour Front"]#len = 16

NEL_times= [4,2,2,2,2,3,3,2,2,2,4,2,2,3,4]#len = 15

# green line
# find a way to add a separate line with Changi Airport Branch Line (CAL)
EWL_stations = ["Tuas Link","Tuas West Road", "Tuas Crescent", "Gul Circle", "Joo Koon", "Pioneer", "Boon Lay", 
               "Lakeside", "Chinese Garden", "Jurong East", "Clementi", "Dover", "Buona Vista", "Commonwealth", 
               "Queenstown", "Redhill", "Tiong Bahru", "Outram Park", "Tanjong Pagar", "Raffles Place", "City Hall", 
               "Bugis", "Lavender", "Kallang", "Aljunied", "Paya Lebar", "Eunos", "Kembangan", "Bedok", "Tanah Merah", 
               "Simei", "Tampines", "Pasir Ris"]

EWL_times= [2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 4, 2, 3, 2, 3, 2, 2, 3, 2, 2, 2, 2, 3, 2, 3, 2]

#red line 
#place holder at ns4✓ and ns6 ✓
#times added ✓
NSL_stations= ["Jurong East","Bukit Batok", "Bukit Gombak", "PLACEHOLDER FOR Brickland" , "Choa Chu Kang", 
              "PLACE HOLDER FOR Sungei Kadut", "Yew Tee", "Kranji", "Marsiling", "Woodlands", "Admiralty", 
              "Sembawang", "Canberra" ,"Yishun", "Khatib", "Yio Chu Kang", "Ang Mo Kio", "Bishan", "Braddell", 
              "Toa Payoh", "Novena", "Newton", "Orchard", "Somerset", "Dhoby Ghaut", "City Hall", "Raffles Place", 
              "Marina Bay", "Marina South Pier"]

NSL_times = [3, 3, 0, 0, 3, 0, 0, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3, 4, 2, 3, 2]

#yellow line
#add a place holder station at cc18 bukit brown ✓ and add times
CCL_stations = ["Dhoby Ghaut","Bras Basah", "Esplanade", "Promenade", "Nicoll Highway", "Stadium", "Mountbatten", 
              "Dakota", "Paya Lebar", "MacPherson", "Tai Seng", "Bartley", "Serangoon", "Lorong Chuan", "Bishan", 
              "Marymount", "Caldecott", "PLACEHOLDER FOR Bukit Brown", "Botanic Gardens", "Farrer Road", "Holland Village", 
              "Buona Vista", "One-north", "Kent Ridge", "Haw Par Villa", "Pasir Pajang", "Labrador Park", "Telok Blangah", 
              "Harbour Front"]

CCL_times= [3, 3, 3, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 2, 2, 4, 0, 0, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2]

#brown line
#add a place holder at te10 and te21
TEL_stations = ["Woodlands North","Woodlands","Woodlands South","Springleaf","Lentor","Mayflower","Bright Hill",
               "Upper Thomson","Caldecott", "PLACEHOLDER FOR Mount Pleasant","Stevens","Napier","Orchard Boulevard",
               "Orchard","Great World","Havelock","Outram Park","Maxwell","Shenton Way","Marina Bay","Gardens by the Bay"]

TEL_times = [3,2,2,2,2,2,2,2,3,0,0,2,2,2,2,2,4,2,3,2,4]

interchange_stations = {
    "Chinatown":["NE3", "DT19"], "Little India": ["NE6", "DT11"], "Bugis" : ["DT13", "EW12"], "Outram Park" : ["NE2", "EW16", "TE16"],
    "Tampines": ["DT31", "EW2"], "Jurong East": ["NS1", "EW24"], "Newton": ["NS20", "DT10"], "Dhoby Ghaut": ["NS23", "NE5", "CC1"], 
    "City Hall": ["NS24", "EW13"], "Raffles Place": ["NS25", "EW14"],"Promenade": ["CC4", "DT14"], "Bayfront":["CE1", "DT15"], 
    "Marina Bay": ["NS26","TE19"], "Paya Lebar": ["CC9", "EW8"], "MacPherson": ["CC10", "DT25"], "Serangoon":["NE11", "CC13"], 
    "Bishan":["NS16", "CC15"], "Caldecott":["CC17","TE9"], "Botanic Gardens":["CC18", "DT8"], "Buona Vista":["CC22", "EW21"], 
    "Harbour Front":["CC29", "NE1"],"Woodlands":["NS8","TE2"],"Stevens":["TE10","DT9"],"Orchard":["TE13","NS21"]
}

#add interchange times from source

line_code = {"DT":"DTL", "NE":"NEL", "EW":"EWL", "NS":"NSL", "CC":"CCL", "TE":"TEL","CE":"CCL"}

class map:
    
    def __init__():
        pass

    def __repr__():
        print(map.create_nodes())

    def create_graph():
        # station_code = map.station_codes()
        # return stations
        pass
    
    def create_nodes():
        nodes = []

        # creates station codes 
        for i in range(len(DTL_stations)):
            nodes.append((DTL_stations[i],f"DT{str(i+1)}","DTL"))
        for i in range(len(NEL_stations)):
            nodes.append((NEL_stations[i],f"NE{str(i+1)}","NEL"))
        for i in range(len(EWL_stations)):
            nodes.append((EWL_stations[i],f"EW{str(i+1)}","EWL"))
        for i in range(len(NSL_stations)):
            nodes.append((NSL_stations[i],f"NS{str(i+1)}","NSL"))
        for i in range(len(CCL_stations)):
            nodes.append((CCL_stations[i],f"CC{str(i+1)}","CCL"))
        for i in range(len(TEL_stations)):
            nodes.append((TEL_stations[i],f"TE{str(i+1)}","TEL"))
        
        return nodes

    def create_edges(nodes):
        mrt_graph = {}
        with open("distances.csv","r") as file:
            for i in range(len(nodes)):
                station_name = nodes[i][0]
                station_code = nodes[i][1]
                line = nodes[i][2] 
                station_number = station_code[2:]
                adjacent_stations = []
                
                print(station_number)

                if line == "DTL":
                    if int(station_number) == 1:
                        adjacent_stations = [[DTL_stations[int(station_number)],DT_times[int(station_number)],0,"train"]]
                    elif int(station_number) == len(DTL_stations):
                        adjacent_stations = [[DTL_stations[int(station_number)-1],DT_times[int(station_number)-1],0,"train"]]
                    else:
                        adjacent_stations = [[DTL_stations[int(station_number)-1],DT_times[int(station_number)-1],0,"train"],[DTL_stations[int(station_number)],DT_times[int(station_number)],0,"train"]]
                elif line == "NEL":
                    if int(station_number) == 1:
                        adjacent_stations = [[NEL_stations[int(station_number)],NEL_times[int(station_number)],0,"train"]]
                    elif int(station_number) == len(NEL_stations):
                        adjacent_stations = [[NEL_stations[int(station_number)-1],NEL_times[int(station_number)-1],0,"train"]]
                    else:
                        adjacent_stations = [[NEL_stations[int(station_number)-1],NEL_times[int(station_number)-1],0,"train"],[NEL_stations[int(station_number)],NEL_times[int(station_number)],0,"train"]]
                elif line == "EWL":
                    if int(station_number) == 1:
                        adjacent_stations = [[EWL_stations[int(station_number)],EWL_times[int(station_number)],0,"train"]]
                    elif int(station_number) == len(EWL_stations):
                        adjacent_stations = [[EWL_stations[int(station_number)-1],EWL_times[int(station_number)-1],0,"train"]]
                    else:
                        adjacent_stations = [[EWL_stations[int(station_number)-1],EWL_times[int(station_number)-1],0,"train"],[EWL_stations[int(station_number)],EWL_times[int(station_number)],0,"train"]]
                elif line == "NSL":
                    if int(station_number) == 1:
                        adjacent_stations = [[NSL_stations[int(station_number)],NSL_times[int(station_number)],0,"train"]]
                    elif int(station_number) == len(NSL_stations):
                        adjacent_stations = [[NSL_stations[int(station_number)-1],NSL_times[int(station_number)-1],0,"train"]]
                    else:
                        adjacent_stations = [[NSL_stations[int(station_number)-1],NSL_times[int(station_number)-1],0,"train"],[NSL_stations[int(station_number)],NSL_times[int(station_number)],0,"train"]]
                elif line == "CCL":
                    if int(station_number) == 1:
                        adjacent_stations = [[CCL_stations[int(station_number)],CCL_times[int(station_number)],0,"train"]]
                    elif int(station_number) == len(CCL_stations):
                        adjacent_stations = [[CCL_stations[int(station_number)-1],CCL_times[int(station_number)-1],0,"train"]]
                    else:
                        adjacent_stations = [[CCL_stations[int(station_number)-1],CCL_times[int(station_number)-1],0,"train"],[CCL_stations[int(station_number)],CCL_times[int(station_number)],0,"train"]]
                elif line == "TEL":
                    if int(station_number) == 1:
                        adjacent_stations = [[TEL_stations[int(station_number)],TEL_times[int(station_number)],0,"train"]]
                    elif int(station_number) == len(TEL_stations):
                        adjacent_stations = [[TEL_stations[int(station_number)-1],TEL_times[int(station_number)-1],0,"train"]]
                    else:
                        adjacent_stations = [[TEL_stations[int(station_number)-1],TEL_times[int(station_number)-1],0,"train"],[TEL_stations[int(station_number)],TEL_times[int(station_number)],0,"train"]]
                        
        print(mrt_graph)
        return mrt_graph
    



map.create_edges(map.create_nodes())