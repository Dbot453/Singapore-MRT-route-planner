from flask import Blueprint, render_template, request, flash
from graphTraversal import GetShortestPath  

map = Blueprint('map', __name__)

@map.route('/map')
def map():
    return render_template('lines.svg')

@map.route('/map', methods=['GET', 'POST'])
def calculate_route():
    if request.method == 'POST':
        start = request.form.get('start')
        dest = request.form.get('dest')
        path = GetShortestPath(start, dest)
        d_distance, d_path_codes, d_path_names = path.astar()
        flash(category='success', message=f'The shortest path from {start} to {dest} is {d_distance} km')
        return render_template('lines.svg', start=start, dest=dest, path=path)

    return render_template('lines.svg')









