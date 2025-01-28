#TODO: make it so that k_shortest paths uses  a different function to get the shortest path

import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
import sqlite3

from graphTraversal import GraphTraversal
from StationList import g_station_list
from custom_implementations.linked_list import LinkedList as LL
from .models import User

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

    # Collect station codes
    station_codes = LL()
    for station_code in g_station_list.keys():
        station_codes.append(station_code)
    station_codes.merge_sort()


    # Retrieve past routes if logged in
    user_past_routes = []
    if current_user.is_authenticated:
        conn = sqlite3.connect('instance/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id, start, end, distance, travel_time, path_codes, path_names, SAVE_datetime FROM route WHERE user_id = ? ORDER BY id DESC LIMIT 5", (current_user.id,))
        user_past_routes = cursor.fetchall()
        conn.close()

    # Handle form submission
    if request.method == 'POST':
        start_station = request.form.get('start') or ''
        destination_station = request.form.get('dest') or ''
        algorithm = request.form.get('algorithm_selection')
        
        # Handle settings
        if 'settings' in request.form:
            return redirect(url_for('settings_page'))

        # Handle show old routes button with a popup
        if 'show_old_routes' in request.form:
            return render_template(
                'map.html',
                user=current_user,
                past_routes=user_past_routes,
                all_station_codes=station_codes,
                show_old_routes=True
            )

        #Ensure both start and destination are selected
        if not start_station or not destination_station:
            flash('Please select both start and destination', category='error')
            return redirect(url_for('map.display_map'))

        # Ensure start and destination are different
        if start_station == destination_station:
            flash('Start and destination cannot be the same', category='error')
            return redirect(url_for('map.display_map'))
        
        #Check if route already exists
        
        conn = sqlite3.connect('instance/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id, start, end, distance, travel_time, path_codes, path_names, SAVE_datetime FROM route WHERE user_id = ? ORDER BY id DESC LIMIT 5", (current_user.id,))
        existing_route = cursor.fetchall()
        conn.close()
        
        if existing_route:
            return render_template(
                #temp change to map-test.html
                'map-test.html',
                user=current_user,
                distance=existing_route.distance,
                time=existing_route.time,
                path_names=existing_route.path_names,
                path_codes=existing_route.path_codes,
                past_routes=user_past_routes,
                selectStart=start_station,
                selectDest=destination_station,
                path_coords=path_coords
            )
            
        else:
            distance_calc, time_calc, codes_calc, names_calc = GraphTraversal(start_station, destination_station, algorithm)
            for code in path_codes:
                path_coords.append(g_station_list.get_lat(code), g_station_list.get_lon(code))
            path_codes = ','.join(codes_calc)
            path_names = ','.join(names_calc)
            conn = sqlite3.connect('instance/database.db')
            new_route = (current_user.id, start_station, destination_station, distance_calc, time_calc, path_codes, path_names)

            # save route to database
            # question: how to deal with k shortest paths? i.e. more than one route. Shoud use a list for save all routes
            GraphTraversal.save_route_to_db([new_route])


            return render_template(
                #temp change to map-test.html
                'map-test.html',
                user=current_user,
                distance=distance_calc,
                time=time_calc,
                path_names=path_names,
                path_codes=path_codes,
                past_routes=user_past_routes,
                all_station_codes=station_codes,
                selectStart=start_station,
                selectDest=destination_station,
                path_coords=path_coords
                )
            
    return render_template(
        #temp change to map-test.html
        'map-test.html',
        user=current_user,
        past_routes=user_past_routes,
        all_station_codes=station_codes,
        path_coords=path_coords
    )
    
@map.route('/map/popup', methods=['GET'])
@login_required
def show_user_routes_popup():
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM route WHERE user_id = ? ORDER BY id DESC", (current_user.id,))
    user_routes = cursor.fetchall()
    conn.close()
    return render_template('popup.html', routes=user_routes)

@map.route('/settings')
@login_required
def settings_page():
    return redirect(url_for('settings.settings_page'))

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
