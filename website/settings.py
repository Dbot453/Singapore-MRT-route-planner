from flask import Flask, render_template, request, redirect, url_for

map_settings = Flask('/settings',__name__)

@map_settings.route('/map/settings', methods=['GET'])
def settings_page():
    return render_template('settings.html')


@map_settings.route('/map/save-settings', methods=['POST'])
def save_settings():
    preferred_route = request.form.get('preferred_route')
    avoid_lines = request.form.get('avoid_lines')
    max_walking_distance = request.form.get('max_walking_distance')

    return redirect(url_for('settings_page'))

