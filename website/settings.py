from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
import sqlite3
from StationList import g_station_codes

# Initialize a Blueprint for settings
settings = Blueprint('settings', __name__)


def get_algorithm_name(algorithm_id):
    """
    Return the algorithm name based on the provided algorithm_id.
    
    Parameters
    ----------
    algorithm_id : str
        The algorithm ID.
                
    Returns
    -------
    str
        The algorithm name.
    """

    # Return the algorithm name based on the provided algorithm_id.

    if algorithm_id == '1':
        return "Breadth First Search"
    elif algorithm_id == '2':
        return "Dijkstra"
    elif algorithm_id == '3':
        return "A Star"
    elif algorithm_id == '4':
        return "K Shortest Path"
    else:
        # Default algorithm name
        return "A Star"


def save_settings_to_db(user_id, preferred_route, algorithm_id, algorithm_name, age):
    """
    Save or update account settings in the database for a given user.
    
    Parameters
    ----------
    user_id : int
        The user ID.
    preferred_route : str
        The preferred route.
    algorithm_id : str
        The algorithm ID.
    algorithm_name : str
        The algorithm name.
    age : int
            
    """

    import sqlite3

    # Connect to the database
    db_connection = sqlite3.connect("instance/database.db")
    cursor = db_connection.cursor()

    # Check if the user already has settings saved
    cursor.execute("SELECT count(*) FROM account_settings WHERE user_id = ?", (user_id,))
    query_count = cursor.fetchall()[0]

    if query_count[0] > 0:
        # Update existing settings
        cursor.execute(
            "UPDATE account_settings SET preferred_route = ?, algorithm_id = ?, algorithm_name = ?, age = ? WHERE user_id = ?",
            (preferred_route, algorithm_id, algorithm_name, age, user_id)
        )
    else:
        # Insert new settings
        cursor.execute(
            "INSERT INTO account_settings (preferred_route, algorithm_id, algorithm_name,age, user_id) VALUES (?, ?, ?, ?, ?)",
            (preferred_route, algorithm_id, algorithm_name,age, user_id)
        )
        
    # Commit changes and close connection
    db_connection.commit()
    db_connection.close()


@settings.route('/settings', methods=['GET', 'POST'])
@login_required
def save_settings():

    """
    Route that allows the user to view and update their settings.
    """
    # Route that allows the user to view and update their settings.

    # Default settings values
    algorithm_id = '3'
    algorithm_name = "A Star"
    preferred_route = "fastest"
    age = 0

    # Retrieve the current age value from the database if it exists
    conn = sqlite3.connect("instance/database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM account_settings WHERE user_id = ?", (current_user.id,))
    result = cursor.fetchone()
    if result:
        age = result[0]
    conn.close()

    if request.method == 'POST':
        # Get form data for preferred route and algorithm selection
        preferred_route = request.form.get('preferred_route')
        algorithm_id = request.form.get('algorithm_selection')
        age = request.form.get('age') or age
        
        
        # Determine the algorithm name based on selection
        algorithm_name = get_algorithm_name(algorithm_id)

        # For A Star (algorithm_id '3'), retrieve the k value from the form
        if algorithm_id == '3':
            k = request.form.get('k-value-container')
        
        # Save updated settings to the database
        save_settings_to_db(
            user_id=current_user.id,
            preferred_route=preferred_route,
            algorithm_id=algorithm_id,
            algorithm_name=algorithm_name,
            age=age,
        )

    # Render the settings page with current settings values
    return render_template(
        'settings.html',
        user=current_user,
        algorithm_id=algorithm_id,
        algorithm_name=algorithm_name,
        preferred_route=preferred_route,
        age=age,
    )