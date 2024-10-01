from flask import Blueprint, request, jsonify, redirect, url_for, session, render_template, flash
from models import create_user, get_surveys, get_survey_statistics, authenticate_user, hash_password, check_password
from werkzeug.security import generate_password_hash
import logging

# Create a Blueprint for routes
routes = Blueprint('routes', __name__)

def setup_routes(app):
    # Register the Blueprint with the app
    app.register_blueprint(routes)

# Serve the homepage
@routes.route('/')
def home():
    return render_template('index.html')  # Use render_template for serving HTML

# Serve the registration page
@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('registration.html')
    

    if request.method == 'POST':
        data = request.form
        name = data.get('name')
        phone_number = data.get('telephone')
        email_address = data.get('email')
        password = data.get('password')
        role_id = 1  # Default role id for regular users

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create the user in the database
        try:
            create_user(name, phone_number, email_address, hashed_password, role_id)
            return jsonify({"message": "User registered successfully!"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

# Serve the login page
@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
            # Handle the login form submission
            data = request.form
            email = data.get('username')  # Fetch the email (assuming username is the email)
            password = data.get('password')  # Fetch the password

            # Fetch user from the database
            user = authenticate_user(email, password)

            if user:
                # Set session or token here to keep user logged in
                session['user_id'] = user[0]  # Assuming user[0] is the user ID
                return redirect(url_for('routes.dashboard'))
            else:
                flash('Invalid credentials, please try again.', 'danger')
                return render_template('login.html')
                

# Serve the homepage dashboard
@routes.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    return render_template('homepage.html')

@routes.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    return render_template('admin.html')


# Serve other routes like surveys, stats, etc.
@routes.route('/survey', methods=['GET'])
def list_surveys():
    surveys = get_surveys()
    return jsonify(surveys)

@routes.route('/survey_management')
def survey_management():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    
    return render_template('survey_management.html')

@routes.route('/survey_list')
def survey_list():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    
    return render_template('survey_list.html')

@routes.route('/user_management')
def user_management():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    
    return render_template('user_management_page.html')

@routes.route('/analytics')
def analytics():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    
    return render_template('analytics.html')

@routes.route('/settings')
def settings():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    
    return render_template('settings.html')

@routes.route('/help_support')
def help_support():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    
    return render_template('help_support.html')


@routes.route('/logout')
def logout():
    # Clear the session data
    session.pop('user_id', None)
    # Redirect to the login page after logout
    return redirect(url_for('routes.login'))
