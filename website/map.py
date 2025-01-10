from flask import Blueprint, render_template, request, flash, redirect, url_for
from graphTraversal import GetShortestPathStatic  
from flask_login import current_user, login_required
from .models import Route
from . import db
from StationList import  g_station_list
from custom_implementations.linked_list import CustomList

map = Blueprint('map', __name__)

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

    # Get all station codes for the dropdowns
    all_station_codes = CustomList()
    for c in g_station_list.keys():
        all_station_codes.append(c)
    all_station_codes.merge_sort()

    # Get user's past routes if logged in
    past_routes = []
    if current_user.is_authenticated:
        past_routes = Route.query.filter_by(user_id=current_user.id).order_by(Route.id.desc()).limit(5).all()

    if request.method == 'POST':
        start = request.form.get('start')
        dest = request.form.get('dest')
        algorithm = request.form.get('algorithm_selection')
        
        if start is None:
            start = ''

        if dest is None:
            dest = ''
        
        
        
        if start == dest:
            flash(category='error', message='Start and destination cannot be the same')
            return redirect(url_for('map.display_map'))
        
        else:   
            route = Route.query.filter_by(start=start, dest=dest).first()
            if route:
                return render_template('map.html', user=current_user,
                                     distance=route.distance,
                                     time = route.time,
                                     path_names=route.path_names,
                                     path_codes=route.path_codes,
                                     past_routes=past_routes,
                                     all_station_codes=all_station_codes,
                                     selectStart=start,
                                     selectDest=dest)
            else:
                x = GetShortestPathStatic(start, dest)
                d_distance, d_time, d_path_codes, d_path_names =  x[0], x[1], x[2], x[3]
                d_path_codes = ','.join(d_path_codes)
                d_path_names = ','.join(d_path_names)
                new_route = Route(start=start, dest=dest, distance=d_distance, time=d_time, path_codes=d_path_codes, path_names=d_path_names, user_id=current_user.id)
                db.session.add(new_route)
                db.session.commit()
                return render_template('map.html', user=current_user,
                                    distance=d_distance,
                                    time=d_time,
                                    path_names=d_path_names,
                                    path_codes=d_path_codes,
                                    past_routes=past_routes,
                                    all_station_codes=all_station_codes,
                                    selectStart=start,
                                    selectDest=dest)
    
    return render_template('map.html', user=current_user,
                         past_routes=past_routes,
                         all_station_codes=all_station_codes)

@map.route('/delete-route/<int:route_id>')
@login_required
def delete_route(route_id):
    route = Route.query.get(route_id)
    if route and route.user_id == current_user.id:
        db.session.delete(route)
        db.session.commit()
        flash('Route deleted successfully', category='success')
    return redirect(url_for('map.calculate_route'))
