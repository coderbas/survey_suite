from flask import Blueprint, request, jsonify, redirect, url_for, session, render_template, flash
from models import  Role,User, Survey, Question, Option, Response, Answer,db
from __init__ import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash , check_password_hash
import logging
import uuid

# Create a Blueprint for routes
routes = Blueprint('routes', __name__)

def setup_routes(app):
    # Register the Blueprint with the app
    app.register_blueprint(routes)

# Serve the homepage
@routes.route('/')
def home():
    return render_template('index.html')  # Use render_template for serving HTML



@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        roles = Role.query.all()
        return render_template('registration.html', roles=roles)
    
    if request.method == 'POST':
        name = request.form.get('name')
        phone_number = request.form.get('telephone')
        email_address = request.form.get('email')
        password = request.form.get('password')
        role_id = request.form.get('role')

        if not role_id:
            flash('Role is required!', 'danger')  # Flashing error message with 'danger' class
            return redirect(url_for('routes.register'))

        hashed_password = generate_password_hash(password)
        
        new_user = User(name=name, PhoneNumber=phone_number, EmailAddress=email_address, password=hashed_password, RoleID=role_id)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')  # Flashing success message
            return redirect(url_for('routes.login'))
        except IntegrityError:
            db.session.rollback()  # Rollback the session to prevent any partial commit
            flash('This email address is already registered. Please use a different email.', 'danger')
            return redirect(url_for('routes.register'))  # Stay on the registration page



@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(EmailAddress=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.UserID
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Invalid credentials')
            return redirect(url_for('routes.login'))

# Serve the homepage dashboard
@routes.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    # Fetch user info from session or database
    user = User.query.get(session['user_id'])
    return render_template('homepage.html', user=user)

@routes.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
     # Fetch user info from session or database
    user = User.query.get(session['user_id'])
    return render_template('admin.html', user=user)


# Serve other routes like surveys, stats, etc.
@routes.route('/survey', methods=['GET'])
def list_surveys():
    surveys = get_surveys()
    return jsonify(surveys)

@routes.route('/survey_management')
def survey_management():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
     # Fetch user info from session or database
    user = User.query.get(session['user_id'])
    return render_template('survey_management.html', user=user)


@routes.route('/create_surv')
def create_surv():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    
     # Fetch user info from session or database
    user = User.query.get(session['user_id'])
    return render_template('create_survey.html', user=user)
########
# Route to handle survey creation
@routes.route('/create-survey', methods=['POST'])
def create_survey():
    survey_data = request.get_json()
    creator_id = 1  # Use the actual logged-in user's ID here

    # Create a new Survey entry
    new_survey = Survey(
        creator_id=creator_id,
        title=survey_data['title'],
        description=survey_data['description']
    )
    db.session.add(new_survey)
    db.session.commit()

    # Add questions and options to the database
    for question in survey_data['questions']:
        new_question = Question(
            survey_id=new_survey.survey_id,
            question_text=question['text'],
            question_type=question['type']
        )
        db.session.add(new_question)
        db.session.commit()

        # If question has options (for multiple-choice or checkbox)
        if 'options' in question:
            for option_text in question['options']:
                new_option = Option(
                    question_id=new_question.question_id,
                    option_text=option_text
                )
                db.session.add(new_option)
                db.session.commit()

    return jsonify({'survey_id': new_survey.survey_id})


# Route to view the survey
@routes.route('/view-survey/<int:survey_id>')
def view_survey(survey_id):
    survey = Survey.query.get(survey_id)
    if not survey:
        return 'Survey not found', 404

    questions = Question.query.filter_by(survey_id=survey_id).all()

    questions_with_options = []
    for question in questions:
        options = Option.query.filter_by(question_id=question.question_id).all()
        questions_with_options.append({
            'question': question,
            'options': options
        })

    return render_template('view_survey.html', survey=survey, questions_with_options=questions_with_options)
# Route to fill the survey by the user
@routes.route('/fill-survey/<int:survey_id>', methods=['GET'])
def fill_survey(survey_id):
    survey = Survey.query.get(survey_id)
    if not survey:
        return 'Survey not found', 404

    questions = Question.query.filter_by(survey_id=survey_id).all()

    questions_with_options = []
    for question in questions:
        options = Option.query.filter_by(question_id=question.question_id).all()
        questions_with_options.append({
            'question': question,
            'options': options
        })

    return render_template('fill_survey.html', survey=survey, questions_with_options=questions_with_options)

# Route to submit the survey
@routes.route('/submit-survey/<int:survey_id>', methods=['POST'])
def submit_survey(survey_id):
    survey = Survey.query.get(survey_id)
    if not survey:
        return 'Survey not found', 404

    respondent_id = 1  # Simulated respondent, ideally this should be the logged-in user

    new_response = Response(survey_id=survey_id, respondent_id=respondent_id)
    db.session.add(new_response)
    db.session.commit()

    questions = Question.query.filter_by(survey_id=survey_id).all()

    for question in questions:
        question_key = f'question_{question.question_id}'

        if question.question_type == 'singleChoice':
            answer_text = request.form.get(question_key)
            if answer_text:
                new_answer = Answer(
                    response_id=new_response.response_id,
                    question_id=question.question_id,
                    answer_text=answer_text
                )
                db.session.add(new_answer)

        elif question.question_type == 'multipleChoice':
            selected_options = request.form.getlist(question_key)
            for option in selected_options:
                new_answer = Answer(
                    response_id=new_response.response_id,
                    question_id=question.question_id,
                    answer_text=option
                )
                db.session.add(new_answer)

        else:
            answer_text = request.form.get(question_key)
            if answer_text:
                new_answer = Answer(
                    response_id=new_response.response_id,
                    question_id=question.question_id,
                    answer_text=answer_text
                )
                db.session.add(new_answer)

    db.session.commit()

    return "Thank you for submitting the survey!"

@routes.route('/survey_list')
def survey_list():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
     # Fetch user info from session or database
    user = User.query.get(session['user_id'])
    return render_template('survey_list.html', user=user)
    

@routes.route('/user_management')
def user_management():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
     # Fetch user info from session or database
    user = User.query.get(session['user_id'])
    return render_template('user_management_page.html', user=user)

@routes.route('/analytics')
def analytics():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
     # Fetch user info from session or database
    user = User.query.get(session['user_id'])
    return render_template('homepage.html', user=user)

@routes.route('/settings')
def settings():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    
 # Fetch user info from session or database
    user = User.query.get(session['user_id'])
    return render_template('settings.html', user=user)

@routes.route('/help_support')
def help_support():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    
     # Fetch user info from session or database
    user = User.query.get(session['user_id'])
    return render_template('help.html', user=user)


@routes.route('/logout')
def logout():
    # Clear the session data
    session.pop('user_id', None)
    # Redirect to the login page after logout
    return redirect(url_for('routes.login'))
