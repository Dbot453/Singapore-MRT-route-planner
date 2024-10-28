from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return "<h1>Test</h1>"

@views.route("/auth")
def auth():
    return "<h1>Auth</h1>"


