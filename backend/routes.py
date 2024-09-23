# backend/routes.py
from flask import Blueprint, request, jsonify, redirect, url_for, session
from models import create_user, get_surveys, get_survey_statistics, get_user_count, get_average_time, authenticate_user, hash_password, check_password
from werkzeug.security import generate_password_hash
import bcrypt


# Create a Blueprint for routes
routes = Blueprint('routes', __name__)

def setup_routes(app):
    # Register the Blueprint with the app
    app.register_blueprint(routes)

# Route to register a new user
@routes.route('/register', methods=['POST'])
def register():
    data = request.form
    name = data.get('name')
    phone_number = data.get('telephone')
    email_address = data.get('email')
    password = data.get('password')
    role_id = 1  # Default role id for regular users, this can be changed

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create the user in the database
    try:
        create_user(name, phone_number, email_address, hashed_password, role_id)
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route to log in a user
@routes.route('/login', methods=['POST'])
def login():
    data = request.form
    email = data.get('username')
    password = data.get('password')

    # Fetch user from the database
    user = authenticate_user(email)

    if user and check_password(password, user[3]):  # Assuming user[3] is the password in DB
        # Set session or token here to keep user logged in
        session['user_id'] = user[0]  # Assuming user[0] is the user ID
        return redirect(url_for('routes.dashboard'))
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# Route for the user dashboard (after login)
@routes.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    # Example: Retrieve user-specific data to show on the dashboard
    return redirect(url_for('static', filename='admin.html'))

# Route for logout
@routes.route('/logout')
def logout():
    session.pop('user_id', None)  # Clear the session
    return redirect(url_for('routes.login'))


# Define route handlers
@routes.route('/survey', methods=['GET'])
def list_surveys():
    surveys = get_surveys()
    return jsonify(surveys)

@routes.route('/user', methods=['POST'])
def add_user():
    data = request.json
    create_user(data['name'], data['phone_number'], data['email_address'], data['role_id'])
    return jsonify({"message": "User created successfully"}), 201

# New route to fetch admin dashboard statistics
@routes.route('/admin/dashboard', methods=['GET'])
def get_dashboard_data():
    try:
        # Get survey statistics for each survey (e.g., response count, average time, etc.)
        surveys_stats = get_survey_statistics()

        # Get the count of users (admins, participants, etc.)
        user_count = get_user_count()

        # Example: Get average time taken to complete a survey
        avg_time_crime_prevention = get_average_time(survey_name="Crime Prevention Survey")

        # Construct dashboard data response
        dashboard_data = {
            "survey_stats": surveys_stats,
            "user_count": user_count,
            "avg_time_crime_prevention": avg_time_crime_prevention
        }

        return jsonify(dashboard_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route('/api/survey_stats', methods=['GET'])
def survey_statistics():
    stats = get_survey_statistics()
    return jsonify(stats)

#



