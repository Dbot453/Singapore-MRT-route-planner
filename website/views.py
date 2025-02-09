from flask import Blueprint, render_template
from flask_login import current_user
import os
  
from StationList import g_station_list

views = Blueprint('views', __name__)


def create_highlighted_map(shortest_route, original_svg_file, new_svg_file):
    # Create a new SVG file highlighting the route in the original SVG.
    # Removes previous instance of the new_svg_file if it exists.
    
    route_stations = list(shortest_route)

    # Remove existing file if present.
    if os.path.isfile(new_svg_file):
        os.remove(new_svg_file)

    with open(original_svg_file, "r") as old_f, open(new_svg_file, "w") as new_f:
        for line in old_f:
            # Process only lines containing "<text"
            if "<text" in line:
                for station in route_stations:
                    if f'>{station}<' in line:
                        if "51,51,51" in line:
                            line = line.replace("rgb(51,51,51)", "rgb(0,0,251)")
                        if "26,26,26" in line:
                            line = line.replace("rgb(26,26,26)", "rgb(0,0,251)")
                        break
            new_f.write(line)

    print("Done")


@views.route('/')
def home():
    return render_template('home.html', user=current_user)


@views.route('/lines')
def show_lines():
    return render_template('lines.svg')


@views.route('/actual-map')
def show_map():
    return render_template('map-test.html', user=current_user)


@views.route('/save_settings')
def settings():
    return render_template('settings.html', user=current_user)
