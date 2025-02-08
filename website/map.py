#TODO: make it so that k_shortest paths uses  a different function to get the shortest path

import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
import sqlite3

from graphTraversal import GraphTraversal
from StationList import  g_station_codes, g_station_list
from Station import Station
from Route import Route

map = Blueprint('map', __name__)

def create_highlighted_map(shortest_route, original_svg_file, new_svg_file):
    stations_in_route = list(shortest_route)

    # Remove existing file if present
    if os.path.isfile(new_svg_file):
        os.remove(new_svg_file)

    with open(original_svg_file, "r") as old_file, open(new_svg_file, "w") as new_file:
        for line in old_file:
            if "<text" in line:
                for station in stations_in_route:
                    if f">{station}<" in line:
                        if "51,51,51" in line:
                            line = line.replace("rgb(51,51,51)", "rgb(0,0,251)")
                        if "26,26,26" in line:
                            line = line.replace("rgb(26,26,26)", "rgb(0,0,251)")
                        break
            new_file.write(line)
    print("Highlighting complete")

@map.route('/map', methods=['GET', 'POST'])
@login_required
def calculate_route():
    path_codes = []
    path_names = []
    path_coords = []
    start_station = ''
    destination_station = ''

    # Retrieve past routes if logged in
    user_past_routes = []
    user_past_routes_string = []
    # default  to 3 - A Star
    algorithm_id = '3'
    algorithm_name = "A Star"
    preferred_route = 'fastest'
    if current_user.is_authenticated:
        conn = sqlite3.connect('instance/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id, start, dest, distance, travel_time, path_codes, path_names, SAVE_datetime FROM route WHERE user_id = ? order by SAVE_datetime desc  ", (current_user.id,))
        query_result = cursor.fetchall()

        for r in query_result:
            # start_station: str, dest_station: str, distance: float, travel_time: float, path_codes: str, path_names: str, user_id: int):
            new_route=Route(r[2], r[3], r[4], r[5], r[6], r[7], current_user.id)
            user_past_routes.append(new_route)
            route_tuple = (r[2], r[3], r[4], r[5])
            user_past_routes_string.append(route_tuple)

        cursor.execute("SELECT preferred_route, algorithm_id, algorithm_name FROM account_settings WHERE user_id = ? ", (current_user.id,))
        account_settings = cursor.fetchall()
        if len(account_settings) > 0:
            settings_result = account_settings[0]
            preferred_route = settings_result[0]
            algorithm_id = settings_result[1]
            algorithm_name = settings_result[2]

        conn.close()

    # Handle form submission
    if request.method == 'POST':
        start_station = request.form.get('start') or ''
        destination_station = request.form.get('dest') or ''
             
        # Handle settings
        post_action = request.form.get("action")
        if post_action == 'Settings': 
            #return redirect(url_for('views.settings'))
            return render_template(
                    'settings.html',
                    user=current_user,
                    algorithm_selection = algorithm_id,
                    algorithm_name = algorithm_name,
                    preferred_route = preferred_route) 
        
        if post_action == 'Calculate':
            #Ensure both start and destination are selected
            if not start_station or not destination_station:
                flash('Please select both start and destination', category='error')
                return render_template(
                    'map.html',
                    user=current_user,
                    all_station_codes=g_station_codes,
                    past_routes=user_past_routes_string) 

            # Ensure start and destination are different
            if start_station == destination_station:
                flash('Start and destination cannot be the same', category='error')
                return render_template(
                    'map.html',
                    user=current_user,
                    all_station_codes=g_station_codes,
                    past_routes=user_past_routes_string,
                    algorithm_selection = algorithm_name,
                    prefferred_route = preferred_route) 
            

            myTraversal = GraphTraversal()
            
            result = myTraversal.GetShortestPathStatic(start_station.split(' - ')[0], destination_station.split(' - ' )[0], algorithm_id)

            # k shortest path, it is a dictionary, use the first one temporarily
            if len(result) > 1:
                print("More than one result") 
                
            one_result = result[1]
                
            distance_calc, time_calc, codes_calc, names_calc =  one_result[0], one_result[1], one_result[2], one_result[3]

            #distance_calc, time_calc, codes_calc, names_calc = myTraversal.GetShortestPathStatic(start_station, destination_station, algorithm)
            
            for code in codes_calc:
                #path_coords.append((Station.get_lat(code), Station.get_lng(code)))
                path_coords.append((g_station_list[code].get_lat(), g_station_list[code].get_lng()))
                
            path_codes = ','.join(codes_calc)
            path_names = ','.join(names_calc)
            conn = sqlite3.connect('instance/database.db')
            ##start_station: str, dest_station: str, distance: float, travel_time: float, path_codes: str, path_names: str, user_id: int):
            new_route = Route(start_station, destination_station, distance_calc, time_calc, path_codes, path_names, current_user.id)

            create_highlighted_map(path_names.split(','), "website/static/Singapore_MRT_Network_no_tspan.svg", "website/static/Singapore_MRT_Network_new.svg")
            
            # save route to database
            # question: how to deal with k shortest paths? i.e. more than one route. Shoud use a list for save all routes
            myTraversal.save_route_to_db([new_route])

            code_name_tuple_list = zip(path_codes.split (','), path_names.split(','))
            code_name_list = [ " - ".join(x) for x in code_name_tuple_list ]
            return render_template(
                'map.html',
                user=current_user,
                distance=distance_calc,
                time=time_calc,
                path_names=path_names.split(','),
                path_codes=code_name_list[::-1],
                past_routes=user_past_routes_string,
                all_station_codes=g_station_codes,
                selectStart=start_station,
                selectDest=destination_station,
                algorithm_selection = algorithm_name,
                preferred_route = preferred_route
                )
    
    # default action     
    return render_template(
        'map.html',
        user=current_user,
        all_station_codes=g_station_codes,
        past_routes=user_past_routes_string,
        algorithm_selection = algorithm_name,
        preferred_route = preferred_route) 

@map.route('/delete-route/<int:route_id>')
@login_required
def delete_route(route_id):
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM route WHERE id = ?", (route_id,))
    route = cursor.fetchone()
    if route and route[0] == current_user.id:
        cursor.execute("DELETE FROM route WHERE id = ?", (route_id,))
        conn.commit()
        flash('Route deleted successfully', category='success')
    conn.close()
    return redirect(url_for('map.calculate_route'))
