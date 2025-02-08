from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
import sqlite3
from StationList import  g_station_codes

settings = Blueprint('settings',__name__)

def get_algorithm_name(algorithm_id):
    if algorithm_id == '1':
        return "Breadth First Search"
    elif algorithm_id == '2':
        return "Dijkstra"
    elif algorithm_id == '3':
        return "A Star"
    elif algorithm_id == '4':
        return "K Shortest Path"
    else: # default
        return "A Star"

def save_settings_to_db(user_id, preferred_route, algorithm_id, algorithm_name, k):
    import sqlite3
    import datetime

    db_connection = sqlite3.connect("instance/database.db")
    cursor = db_connection.cursor()

    cursor.execute("SELECT count(*) FROM account_settings WHERE user_id = ?  ", (user_id,))
    query_count = cursor.fetchall()[0]
    if query_count[0] > 0:
        cursor.execute("update account_settings set preferred_route = ? , algorithm_id = ? , algorithm_name = ?, k = ? where user_id = ? ", 
                       (preferred_route, algorithm_id, algorithm_name,k, user_id))
    else:
        cursor.execute("INSERT INTO account_settings (preferred_route, algorithm_id, algorithm_name, k, user_id) VALUES (?, ?, ?, ?)",  
                       (preferred_route, algorithm_id, algorithm_name, k, user_id))
        
    db_connection.commit()
    db_connection.close()


@settings.route('/settings', methods=['GET', 'POST'])
@login_required
def save_settings():
    # default 
    algorithm_id = 3
    algorithm_name = "A Star"
    preferred_route = "fastest"
    
    k = None
    conn = sqlite3.connect("instance/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT k FROM account_settings WHERE user_id = ?", (current_user.id,))
    result = cursor.fetchone()
    if result:
        k = result[0]
    conn.close()

    if request.method == 'POST':
        preferred_route = request.form.get('preferred_route')
        algorithm_id = request.form.get('algorithm_selection')
        # Handle password changes here as needed
        algorithm_name =  get_algorithm_name(algorithm_id)
        if algorithm_id == '3':
            k = request.form.get('k-value-container')
        save_settings_to_db(user_id=current_user.id, preferred_route=preferred_route, algorithm_id=algorithm_id, algorithm_name = algorithm_name, k = k)

    return render_template(
        'settings.html',
        user=current_user,
        algorithm_id = algorithm_id,
        algorithm_name = algorithm_name,
        preferred_route = preferred_route,
        k = k)