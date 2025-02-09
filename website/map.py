import os
import sqlite3
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required

from graphTraversal import GraphTraversal
from StationList import g_station_codes, g_station_list
from Station import Station
from Route import Route
from datetime import datetime, timedelta
from datetime import datetime, time as dtime

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
                            line = line.replace("font-size:10px", "font-size:16px")
                        if "26,26,26" in line:
                            line = line.replace("rgb(26,26,26)", "rgb(0,0,251)")
                            line = line.replace("font-size:10px", "font-size:16px")
                        break
            new_file.write(line)
    print("Highlighting complete")

def calculate_cost(distance: float, age: int, time: str) -> int:
    adult_cost_table = {
        (0, 3.2): (69, 119),
        (3.3, 4.2): (79, 129),
        (4.3, 5.2): (90, 140),
        (5.3, 6.2): (100, 150),
        (6.3, 7.2): (109, 159),
        (7.3, 8.2): (116, 166),
        (8.3, 9.2): (123, 173),
        (9.3, 10.2): (127, 177),
        (10.3, 11.2): (131, 181),
        (11.3, 12.2): (135, 185),
        (12.3, 13.2): (139, 189),
        (13.3, 14.2): (143, 193),
        (14.3, 15.2): (148, 198),
        (15.3, 16.2): (152, 202),
        (16.3, 17.2): (156, 206),
        (17.3, 18.2): (160, 210),
        (18.3, 19.2): (164, 214),
        (19.3, 20.2): (167, 217),
        (20.3, 21.2): (170, 220),
        (21.3, 22.2): (173, 223),
        (22.3, 23.2): (176, 226),
        (23.3, 24.2): (178, 228),
        (24.3, 25.2): (180, 230),
        (25.3, 26.2): (182, 232),
        (26.3, 27.2): (183, 233),
        (27.3, 28.2): (184, 234),
        (28.3, 29.2): (185, 235),
        (29.3, 30.2): (186, 236),
        (30.3, 31.2): (187, 237),
        (31.3, 32.2): (188, 238),
        (32.3, 33.2): (189, 239),
        (33.3, 34.2): (190, 240),
        (34.3, 35.2): (191, 241),
        (35.3, 36.2): (192, 242),
        (36.3, 37.2): (193, 243),
        (37.3, 38.2): (194, 244),
        (38.3, 39.2): (195, 245),
        (39.3, 40.2): (196, 246),
        (40.3, float("inf")): (197, 247)
    }
    student_cost_table = {
        (0, 3.2): (2, 52),
        (3.3, 4.2): (7, 57),
        (4.3, 5.2): (13, 63),
        (5.3, 6.2): (18, 68),
        (6.3, 7.2): (21, 71),
        (7.3, 8.2): (24, 74),
        (8.3, 9.2): (24, 74),
        (9.3, 11.2): (24, 74),
        (11.3, 15.2): (24, 74),
        (15.3, 19.2): (24, 74),
        (19.3, 23.2): (24, 74),
        (23.3, float("inf")): (24, 74)
    }

    if age < 7:
        return 0
    elif 7 <= age <= 25:
        for (min_d, max_d), (early_fare, regular_fare) in student_cost_table.items():
            if min_d <= distance <= max_d:
                departure_time = datetime.strptime(time, "%H:%M").time()
                if departure_time < dtime(7, 45):
                    return early_fare
                else:
                    return regular_fare
        return None
    else:
        for (min_d, max_d), (early_fare, regular_fare) in adult_cost_table.items():
            if min_d <= distance <= max_d:
                departure_time = datetime.strptime(time, "%H:%M").time()
                if departure_time < dtime(7, 45):
                    return early_fare
                else:
                    return regular_fare
        return None

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
    # default to 3 - A Star
    algorithm_id = '3'
    algorithm_name = "A Star"
    preferred_route = 'fastest'

    if current_user.is_authenticated:
        conn = sqlite3.connect('instance/database.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, user_id, start, dest, distance, travel_time, path_codes, path_names, SAVE_datetime "
            "FROM route WHERE user_id = ? order by SAVE_datetime desc",
            (current_user.id,)
        )
        query_result = cursor.fetchall()
        for r in query_result:
            new_route = Route(r[2], r[3], r[4], r[5], r[6], r[7], current_user.id)
            user_past_routes.append(new_route)
            route_tuple = (r[2], r[3], r[4], r[5])
            user_past_routes_string.append(route_tuple)

        cursor.execute(
            "SELECT preferred_route, algorithm_id, algorithm_name "
            "FROM account_settings WHERE user_id = ?",
            (current_user.id,)
        )
        account_settings = cursor.fetchall()
        if account_settings:
            settings_result = account_settings[0]
            preferred_route = settings_result[0]
            algorithm_id = settings_result[1]
            algorithm_name = settings_result[2]

        conn.close()

    # Handle form submission
    if request.method == 'POST':
        start_station = request.form.get('start') or ''
        destination_station = request.form.get('dest') or ''
        set_off_time = request.form.get('departure_time') or ''
        set_off_time = set_off_time.strip()
        kpath = request.form.get('kpathSelection') or ''
        
        try:
            off_time_obj = datetime.strptime(set_off_time, "%H:%M").time()
        except ValueError:
            flash("Invalid time format", category="error")
            return redirect(url_for("map.calculate_route"))

        if datetime.strptime("00:30", "%H:%M").time() <= off_time_obj < datetime.strptime("05:30", "%H:%M").time():
            flash("No trains running at that time", category="error")
            return redirect(url_for("map.calculate_route"))

        # Handle settings action
        post_action = request.form.get("action")
        if post_action == 'Settings':
            return render_template(
                'settings.html',
                user=current_user,
                algorithm_selection=algorithm_id,
                algorithm_name=algorithm_name,
                preferred_route=preferred_route
            )

        if post_action == 'Calculate':
            # Ensure both start and destination are selected
            if not start_station or not destination_station:
                flash('Please select both start and destination', category='error')
                return render_template(
                    'map.html',
                    user=current_user,
                    all_station_codes=g_station_codes,
                    past_routes=user_past_routes_string
                )

            # Ensure start and destination are different
            if start_station == destination_station:
                flash('Start and destination cannot be the same', category='error')
                return render_template(
                    'map.html',
                    user=current_user,
                    all_station_codes=g_station_codes,
                    past_routes=user_past_routes_string,
                    algorithm_selection=algorithm_name,
                    prefferred_route=preferred_route
                )

            myTraversal = GraphTraversal()
            shortest_path_result = myTraversal.GetShortestPathStatic(
                start_station.split(' - ')[0],
                destination_station.split(' - ')[0],
                algorithm_id
            )

            shortest_path_result = shortest_path_result[0]                
                
            distance_calc, time_calc, codes_calc, names_calc = shortest_path_result[0], shortest_path_result[1], shortest_path_result[2], shortest_path_result[3]

            path_codes = ','.join(codes_calc)
            path_names = ','.join(names_calc)
            conn = sqlite3.connect('instance/database.db')

            new_route = Route(start_station, destination_station, distance_calc, time_calc, path_codes, path_names, current_user.id)

            create_highlighted_map(
                path_names.split(','),
                "website/static/Singapore_MRT_Network_no_tspan.svg",
                "website/static/Singapore_MRT_Network_new.svg"
            )

            # Save route to database
            myTraversal.save_route_to_db([new_route])

            code_name_tuple_list = zip(path_codes.split(','), path_names.split(','))
            code_name_list = [" - ".join(x) for x in code_name_tuple_list]
            
            conn = sqlite3.connect('instance/database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT age FROM account_settings WHERE user_id = ?", (current_user.id,))
            result_age = cursor.fetchone()
            conn.close()
            if result_age:
                age = result_age[0]
            else:
                age = 0  # fallback default age
            
            cost = calculate_cost(distance_calc, age, set_off_time)
            
            try:
                # Assuming time_calc is in seconds, convert to minutes
                travel_time_minutes = int(time_calc) // 60
            except Exception:
                travel_time_minutes = None
            try:
                departure = datetime.strptime(set_off_time, "%H:%M")
                arrival_time = (departure + timedelta(minutes=travel_time_minutes)).strftime("%H:%M")
            except Exception:
                arrival_time = "Invalid Time"
            

            return render_template(
                'map.html',
                user=current_user,
                distance=f"{distance_calc:.0f}",
                time=time_calc,
                arrival_time=arrival_time,
                path_names=path_names.split(','),
                path_codes=code_name_list[::-1],
                past_routes=user_past_routes_string,
                all_station_codes=g_station_codes,
                selectStart=start_station,
                selectDest=destination_station,
                algorithm_selection=algorithm_name,
                preferred_route=preferred_route,
                cost = cost
            )

    # Default action if not POST or no specific action
    return render_template(
        'map.html',
        user=current_user,
        all_station_codes=g_station_codes,
        past_routes=user_past_routes_string,
        algorithm_selection=algorithm_name,
        preferred_route=preferred_route
    )


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
