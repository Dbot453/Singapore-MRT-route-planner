from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

from graphTraversal import GetShortestPathStatic  
from StationList import  g_station_list


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

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/lines')
def show_lines():
    return render_template('lines.svg')

@views.route('/actual-map')
def show_map():
    return render_template('map-test.html', user=current_user)

#@views.route('/map')
#def calculate_route():
#    return render_template('map.html', user=current_user)


@views.route('/map', methods=['GET', 'POST'])
def calculate_route():
    d_distance = 0
    d_path_codes = []
    d_path_names = []
    start = ''
    dest = ''

    new_d_path_codes = []
    
    if request.method == 'POST':
        start = request.form.get('start')
        dest = request.form.get('dest')
        algorithm = request.form.get('algorithm_selection')
        
        # htmo does not talk None
        if start is None:
            start = ''

        if dest is None:
            dest = ''

        if start != dest and len(start) > 1 and len(dest) >1 :
            d_distance, d_path_codes, d_path_names =  GetShortestPathStatic(start, dest, algorithm)

            new_d_path_codes = []
            for i in range(len(d_path_codes)):
                new_d_path_codes.append(d_path_codes[i] + " - " + d_path_names[i])
            
            print(len(d_path_codes), len(d_path_names))
            d_path_names = [g_station_list[c].get_station_name() for c in d_path_codes]


    create_highlighted_map(d_path_names, "website/static/Singapore_MRT_Network_no_tspan.svg", "website/static/Singapore_MRT_Network_new.svg")

    all_station_codes = [c  for  c in  g_station_list.keys()]
    all_station_codes.sort()

    return render_template('map.html', user=current_user,
                            distance=d_distance,
                            path_codes=new_d_path_codes,
                            path_names=d_path_names,
                            selectedStart = start,
                            selectedDest = dest,
                            all_station_codes = all_station_codes)