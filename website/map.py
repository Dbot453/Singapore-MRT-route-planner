from flask import Blueprint, render_template

map = Blueprint('map', __name__)

@map.route('/map')
def map():
    return render_template('lines.svg')#






