from flask import Blueprint, render_template, request, flash, redirect, url_for
from graphTraversal import GetShortestPathStatic  
from flask_login import current_user   

map = Blueprint('map', __name__)

# @map.route('/show_lines')
# def display_map():
#     return render_template('lines.svg')

@map.route('/map', methods=['GET', 'POST'])
def calculate_route():
    if request.method == 'POST':
        start = request.form.get('start')
        dest = request.form.get('dest')
        algorithm = request.form.get('algorithm_selection')
        
        if start == dest:
            flash(category='error', message='Start and destination cannot be the same')
        
        else:   
            d_distance, d_path_codes, d_path_names =  GetShortestPathStatic(start, dest, algorithm) 
            return render_template('map.html', user=current_user,
                                 distance=d_distance,
                                 path_codes=d_path_codes,
                                 path_names=d_path_names)
    
    return render_template('map.html')