from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html', user=current_user)

@views.route('/lines')
def show_lines():
    return render_template('lines.svg')

@views.route('/actual-map')
def show_map():
    return render_template('map-test.html', user=current_user)

@views.route('/map')
def calculate_route():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('map.html', user=current_user)
