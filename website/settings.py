from flask import Flask, render_template, request, redirect, url_for

settings = Flask('settings',__name__)

@settings.route('/settings', methods=['GET'])
def render_settings():
    return render_template('settings.html')


@settings.route('/save-route-settings', methods=['POST'])
def save_settings():
    preferredroute = request.form.get('preferred-route')
    algorithm = request.form.get('algorithm')
    return redirect(url_for('settings_page'))


@settings.route('/save-account-settings', methods=['POST'])   
def save_account_settings():
    
    return redirect(url_for('settings_page'))

  # In your Flask app (app.py or similar)

#   @app.route('/settings', methods=['GET', 'POST'])
#   def settings():
#     if request.method == 'POST':
#       session['preferred_route'] = request.form.get('preferred_route')
#       session['algorithm_selection'] = request.form.get('algorithm_selection')
#       # Handle password changes here as needed
#       return redirect(url_for('settings'))
#     return render_template('settings.html',
#                  preferred_route=session.get('preferred_route'),
#                  algorithm_selection=session.get('algorithm_selection'))