from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
import json

#from graphTraversal import GraphTraversal  
from StationList import g_station_list


views = Blueprint('views', __name__)

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
