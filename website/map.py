import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required

from .models import Route
from . import db
from graphTraversal import GetShortestPathStatic
from StationList import g_station_list
from custom_implementations.linked_list import LinkedList as LL

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
def calculate_route():
    distance = 0
    path_codes = []
    path_names = []
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
        user_past_routes = Route.query.filter_by(user_id=current_user.id).order_by(Route.id.desc()).limit(5).all()

    if request.method == 'POST':
        start_station = request.form.get('start') or ''
        destination_station = request.form.get('dest') or ''
        algorithm = request.form.get('algorithm_selection')

        if 'settings' in request.form:
            return redirect(url_for('settings_page'))

        if 'show_old_routes' in request.form:
            return render_template(
                'map.html',
                user=current_user,
                past_routes=user_past_routes,
                all_station_codes=station_codes,
                show_old_routes=True
            )

        if not start_station or not destination_station:
            flash('Please select both start and destination', category='error')
            return redirect(url_for('map.display_map'))

        if start_station == destination_station:
            flash('Start and destination cannot be the same', category='error')
            return redirect(url_for('map.display_map'))

        existing_route = Route.query.filter_by(start=start_station, dest=destination_station).first()
        if existing_route:
            return render_template(
                'map.html',
                user=current_user,
                distance=existing_route.distance,
                time=existing_route.time,
                path_names=existing_route.path_names,
                path_codes=existing_route.path_codes,
                past_routes=user_past_routes,
                all_station_codes=station_codes,
                selectStart=start_station,
                selectDest=destination_station
            )
        else:
            distance_calc, time_calc, codes_calc, names_calc = GetShortestPathStatic(start_station, destination_station)
            path_codes = ','.join(codes_calc)
            path_names = ','.join(names_calc)
            new_route = Route(
                start=start_station,
                dest=destination_station,
                distance=distance_calc,
                time=time_calc,
                path_codes=path_codes,
                path_names=path_names,
                user_id=current_user.id
            )
            db.session.add(new_route)
            db.session.commit()
            return render_template(
                'map.html',
                user=current_user,
                distance=distance_calc,
                time=time_calc,
                path_names=path_names,
                path_codes=path_codes,
                past_routes=user_past_routes,
                all_station_codes=station_codes,
                selectStart=start_station,
                selectDest=destination_station
            )

    return render_template(
        'map.html',
        user=current_user,
        past_routes=user_past_routes,
        all_station_codes=station_codes
    )

@map.route('/delete-route/<int:route_id>')
@login_required
def delete_route(route_id):
    route_to_delete = Route.query.get(route_id)
    if route_to_delete and route_to_delete.user_id == current_user.id:
        db.session.delete(route_to_delete)
        db.session.commit()
        flash('Route deleted successfully', category='success')
    return redirect(url_for('map.calculate_route'))
