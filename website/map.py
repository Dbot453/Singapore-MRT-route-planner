from flask import Blueprint, render_template, request, flash, redirect, url_for
from graphTraversal import GetShortestPathStatic  
from flask_login import current_user
from .models import Route
from . import db

map = Blueprint('map', __name__)

# @map.route('/show_lines')
# def display_map():
#     return render_template('lines.svg')

@map.route('/map', methods=['GET', 'POST'])
def calculate_route():
    if request.method == 'POST':
        start = request.form.get('start')
        dest = request.form.get('dest')
        
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
                                     path_codes=route.path_codes)
            else:
                d_distance, d_time, d_path_codes, d_path_names =  GetShortestPathStatic(start,dest) 
                d_path_codes = ','.join(d_path_codes)
                d_path_names = ','.join(d_path_names)
                new_route = Route(start=start, dest=dest, distance=d_distance, time=d_time, path_codes=d_path_codes, path_names=d_path_names, user_id=current_user.id)
                db.session.add(new_route)
                db.session.commit()
                return render_template('map.html', user=current_user,
                                    distance=d_distance,
                                    time = d_time,
                                    path_names=d_path_names,
                                    path_codes=d_path_codes)
    
    return render_template('map.html')