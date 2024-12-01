from flask import Blueprint, render_template, request, flash, redirect, url_for
from graphTraversal import GetShortestPathStatic  
from flask_login import current_user
from StationList import  g_station_list

map = Blueprint('map', __name__)

# @map.route('/show_lines')
# def display_map():
#     return render_template('lines.svg')

def create_highlighted_map(shortestRoute, original_svg_file, new_svg_file):
    import os

    my_shortestRoute = list(shortestRoute)
    # remove previous file 
    if os.path.isfile(new_svg_file):
        os.remove(new_svg_file)

    new_f = open(new_svg_file, "w")
    old_f = open(original_svg_file, "r")
    is_start = False 
    for x in old_f:
        if x. find("<text") > 0:
            is_in_route = False
            for s in my_shortestRoute:
                ##print(s, x)
                if x.find('>' + s + '<') > 0:
                    if x.find('51,51,51') > 0: 
                        x = x.replace("rgb(51,51,51)", "rgb(0,0,251)")

                    if x.find('26,26,26') > 0: 
                        x = x.replace("rgb(26,26,26)", "rgb(0,0,251)")                        
                    
                    break
            
        new_f.write(x)

    old_f.close()
    new_f.close()
    
    print("Done")


@map.route('/map', methods=['GET', 'POST'])
def calculate_route():
    d_distance = 0
    d_path_codes = []
    d_path_names = []
    start = ''
    dest = ''

    if request.method == 'POST':
        start = request.form.get('start')
        dest = request.form.get('dest')
        algorithm = request.form.get('algorithm_selection')
        
        # htmo does not talk None
        if start is None:
            start = ''

        if dest is None:
            dest = ''

        if start != dest and len(start) > 1 and len(dest) >1 :
            d_distance, d_path_codes, d_path_names =  GetShortestPathStatic(start, dest, algorithm)

    create_highlighted_map(d_path_names, "website/static/Singapore_MRT_Network_no_tspan.svg", "website/static/Singapore_MRT_Network_new.svg")

    all_station_codes = [c  for  c in  g_station_list.keys()]
    all_station_codes.sort()

    return render_template('map.html', user=current_user,
                            distance=d_distance,
                            path_codes=d_path_codes,
                            path_names=d_path_names,
                            selectedStart = start,
                            selectedDest = dest,
                            all_station_codes = all_station_codes)
