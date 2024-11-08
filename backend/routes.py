from flask import Blueprint, request, jsonify, redirect, url_for, session, render_template, flash
from backend.models import Role, Users, Survey, SurveyRating, Question, Option, Response, Answer, db
from backend import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
import logging
import uuid

# Create a Blueprint for routesS
routes = Blueprint('routes', __name__)

def setup_routes(app):
    # Register the Blueprint with the app
    app.register_blueprint(routes)


@routes.route('/set-language/<lang>')
def set_language(lang):
    # Store the selected language in session
    session['lang'] = lang
    return redirect(url_for('routes.home_page'))  # Redirect to the updated home_page


# Use this function to serve both English and Arabic home pages
@routes.route('/home', endpoint='home_page')
def home_page():
    lang = session.get('lang', 'en')  # Default to English if no language is selected
    if lang == 'ar':
        return render_template('ar/home.html')  # Serve Arabic version
    return render_template('home.html')  # Serve English version


# Serve the homepage (rename the function here to avoid conflict)
@routes.route('/')
def home_default():
    return render_template('index.html')  # Use render_template for serving HTML



@routes.route('/register', methods=['GET', 'POST'])
def register():
    lang = session.get('lang', 'en')  # Default to English
    
    if request.method == 'GET':
        # Serve the appropriate registration template based on language
        if lang == 'ar':
            return render_template('ar/registration.html')
        return render_template('registration.html')

    if request.method == 'POST':
        # Collect form data
        finance_no = request.form.get('finance_no')
        name_ar = request.form.get('name_ar')
        name_en = request.form.get('name_en')
        mobile_no = request.form.get('mobile_no')
        email_id = request.form.get('email_id')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        section = request.form.get('section')

        # Ensure passwords match
        if password != confirm_password:
            flash('كلمة المرور غير متطابقة!' if lang == 'ar' else 'Passwords do not match!', 'danger')
            return render_template('registration.html')  # Stay on the same page

        # Check if the email already exists
        existing_user = Users.query.filter_by(email_id=email_id).first()
        if existing_user:
            flash('هذا البريد الإلكتروني مسجل بالفعل.' if lang == 'ar' else 'This email is already registered.', 'danger')
            return render_template('registration.html')

        # Hash the password and create a new user
        hashed_password = generate_password_hash(password)
        new_user = Users(
            finance_no=finance_no,
            name_ar=name_ar,
            name_en=name_en,
            mobile_no=mobile_no,
            email_id=email_id,
            hashed_password=hashed_password,
            section=section
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('تم التسجيل بنجاح. يرجى تسجيل الدخول.' if lang == 'ar' else 'Registration successful. Please log in.', 'success')
            return redirect(url_for('routes.login'))
        except IntegrityError:
            db.session.rollback()
            flash('حدث خطأ أثناء التسجيل.' if lang == 'ar' else 'An error occurred during registration.', 'danger')
            return render_template('registration.html')




@routes.route('/login', methods=['GET', 'POST'])
def login():
    lang = session.get('lang', 'en')  # Default to English

    if request.method == 'GET':
        # Render either Arabic or English login template
        if lang == 'ar':
            return render_template('ar/login.html')
        return render_template('login.html')

    if request.method == 'POST':
        email_id = request.form.get('email_id')
        password = request.form.get('password')

        # Query the user by email
        user = Users.query.filter_by(email_id=email_id).first()
        print(f"User: {user}")

        print(f"Entered Password: {password}")
        print(f"Stored Hashed Password: {user.hashed_password if user else 'No user found'}")

        # Validate user credentials
        if user and check_password_hash(user.hashed_password, password):
            session['user_id'] = user.id  # Use the correct user ID field
            flash(f'مرحبًا، {user.name_ar}!' if lang == 'ar' else f'Welcome, {user.name_en}!', 'success')
            return redirect(url_for('routes.dashboard'))
        else:
            flash('بيانات الاعتماد غير صحيحة' if lang == 'ar' else 'Invalid credentials', 'danger')
            return render_template('login.html')  # Stay on the same page



@routes.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    lang = session.get('lang', 'en')
    user = Users.query.get(session['user_id'])

    # Render the homepage based on the selected language
    if lang == 'ar':
        return render_template('ar/homepage.html', user=user)
    return render_template('homepage.html', user=user)
@routes.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))
    
    user = Users.query.get(session['user_id'])
    return render_template('profile.html', user=user)

# Admin Dashboard Route with Top Surveys
@routes.route('/admin-dashboard')
def admin_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    lang = session.get('lang', 'en')
    user = Users.query.get(session['user_id'])

    # Query top 3 surveys by response count
    top_surveys = db.session.query(Survey, func.count(Response.response_id).label('response_count')) \
        .outerjoin(Response) \
        .group_by(Survey.survey_id) \
        .order_by(func.count(Response.response_id).desc()) \
        .limit(3) \
        .all()

    if lang == 'ar':
        return render_template('ar/admin.html', user=user, surveys=top_surveys)
    return render_template('admin.html', user=user, surveys=top_surveys)


# Full Survey List Route
@routes.route('/surveys')
def surveys():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    lang = session.get('lang', 'en')
    user = Users.query.get(session['user_id'])

    # Query all surveys with response counts
    survey_list = db.session.query(Survey, func.count(Response.response_id).label('response_count')) \
        .outerjoin(Response) \
        .group_by(Survey.survey_id) \
        .all()

    if lang == 'ar':
        return render_template('ar/survey_list.html', user=user, surveys=survey_list)
    return render_template('survey_list.html', user=user, surveys=survey_list)


@routes.route('/analytics_reporting')
def analytics_reporting():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    lang = session.get('lang', 'en')
    user = Users.query.get(session['user_id'])

    # Fetch all surveys with response counts
    survey_list = db.session.query(Survey, func.count(Response.response_id).label('response_count')) \
        .outerjoin(Response) \
        .group_by(Survey.survey_id) \
        .all()

    if lang == 'ar':
        return render_template('ar/analytics_reporting.html', user=user, surveys=survey_list)
    return render_template('analytics_reporting.html', user=user, surveys=survey_list)

# Route for searching surveys
@routes.route('/search-survey', methods=['GET'])
def search_survey():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    user = Users.query.get(session['user_id'])
    lang = session.get('lang', 'en')
    query = request.args.get('query')  # Get the search query

    if query:
        search_results = db.session.query(Survey, func.count(Response.response_id).label('response_count')) \
            .outerjoin(Response) \
            .filter(Survey.title.ilike(f'%{query}%')) \
            .group_by(Survey.survey_id) \
            .all()
    else:
        # Default to top 3 surveys if no query
        search_results = db.session.query(Survey, func.count(Response.response_id).label('response_count')) \
            .outerjoin(Response) \
            .group_by(Survey.survey_id) \
            .order_by(func.count(Response.response_id).desc()) \
            .limit(3) \
            .all()

    if lang == 'ar':
        return render_template('ar/analytics_reporting.html', surveys=search_results, query=query, user=user)
    return render_template('analytics_reporting.html', surveys=search_results, query=query, user=user)

# Route for survey analytics
@routes.route('/survey-analytics/<int:survey_id>')
def survey_analytics(survey_id):
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    user = Users.query.get(session['user_id'])
    survey = Survey.query.get(survey_id)
    if not survey:
        return 'Survey not found', 404

    # Fetch questions and answers for this survey
    questions = Question.query.filter_by(survey_id=survey_id).all()
    question_data = [{
        'question_text': question.question_text,
        'question_type': question.question_type,
        'answers': [answer.answer_text for answer in Answer.query.filter_by(question_id=question.question_id).all()]
    } for question in questions]

    lang = session.get('lang', 'en')
    if lang == 'ar':
        return render_template('ar/analytics.html', survey=survey, question_data=question_data, user=user)
    return render_template('analytics.html', survey=survey, question_data=question_data, user=user)

from datetime import datetime
from flask import jsonify
from collections import Counter
from openai import OpenAI
import os

# Initialize OpenAI client with the environment variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@routes.route('/generate-report/<int:survey_id>', methods=['POST'])
def generate_ai_report(survey_id):
    survey = Survey.query.get(survey_id)
    if not survey:
        return jsonify({'error': 'Survey not found'}), 404

    responses = Response.query.filter_by(survey_id=survey_id).all()
    if not responses:
        return jsonify({'error': 'No responses available for this survey'}), 404

    report_data = {
        "survey_title": survey.title,
        "survey_description": survey.description,
        "responses": [],
        "aggregated_data": {}
    }

    # Loop through all responses and gather answers
    for response in responses:
        answers = Answer.query.filter_by(response_id=response.response_id).all()
        for answer in answers:
            question = Question.query.get(answer.question_id)
            report_data["responses"].append({
                "question": question.question_text,
                "answer": answer.answer_text
            })

            if question.question_type in ['singleChoice', 'multipleChoice']:
                if question.question_text not in report_data["aggregated_data"]:
                    report_data["aggregated_data"][question.question_text] = Counter()

                report_data["aggregated_data"][question.question_text][answer.answer_text] += 1

    aggregated_summary = []
    for question, counts in report_data["aggregated_data"].items():
        aggregated_summary.append(f"Question: {question}\nCounts: {dict(counts)}")

    prompt = f"""
    You are a survey analysis assistant. Here is the data from a survey titled "{report_data['survey_title']}".
    Description: {report_data['survey_description']}
    
    The survey responses are as follows:
    {', '.join([f"Q: {entry['question']}, A: {entry['answer']}" for entry in report_data['responses']])}

    Aggregated Results:
    {', '.join(aggregated_summary)}
    
    Please provide a formal detailed report with the following sections:
    Survey Title as Header
    1. Executive Summary
    2. Insights
    3. Sentiment Analysis
    4. Compare the data to real life data from previous years
    5. Conclusions
    6. Recommendations
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.5
        )

        report_content = response.choices[0].message.content
        return jsonify({'report': report_content})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@routes.route('/survey_management')
def survey_management():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    lang = session.get('lang', 'en')
    user = Users.query.get(session['user_id'])

    if lang == 'ar':
        return render_template('ar/survey_management.html', user=user)
    return render_template('survey_management.html', user=user)

@routes.route('/create_surv')
def create_surv():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    lang = session.get('lang', 'en')
    user = Users.query.get(session['user_id'])

    if lang == 'ar':
        return render_template('ar/create_survey.html', user=user)
    return render_template('create_survey.html', user=user)

########
from datetime import datetime

# Route to handle survey creation
from datetime import datetime
from flask import redirect, url_for

# Route to handle survey creation
# Route to handle survey creation
@routes.route('/create-survey', methods=['POST'])
def create_survey():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    survey_data = request.get_json()
    print("Received survey data:", survey_data)  # Debugging print statement

    if not all(k in survey_data for k in ('title', 'description', 'start_date', 'end_date', 'questions')):
        return jsonify({'error': 'Missing fields'}), 400  # Validation check

    creator_id = session['user_id']  # Use logged-in user's ID from session

    new_survey = Survey(
        creator_id=creator_id,
        title=survey_data['title'],
        description=survey_data['description'],
        start_date=datetime.strptime(survey_data['start_date'], '%Y-%m-%d'),
        end_date=datetime.strptime(survey_data['end_date'], '%Y-%m-%d')
    )
    db.session.add(new_survey)
    db.session.commit()

    for question in survey_data['questions']:
        new_question = Question(
            survey_id=new_survey.survey_id,
            question_text=question['text'],
            question_type=question['type']
        )
        db.session.add(new_question)
        db.session.commit()

        if 'options' in question:
            for option_text in question['options']:
                new_option = Option(
                    question_id=new_question.question_id,
                    option_text=option_text
                )
                db.session.add(new_option)
                db.session.commit()

    return jsonify({'success': True, 'survey_id': new_survey.survey_id}), 201





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
# Route to submit the survey responses
@routes.route('/submit-survey/<int:survey_id>', methods=['POST'])
def submit_survey(survey_id):
    survey = Survey.query.get(survey_id)
    if not survey:
        return 'Survey not found', 404

    # Simulate a respondent for this case, ideally would be the logged-in user
    respondent_id = 1

    # Create a new Response entry
    new_response = Response(survey_id=survey_id, respondent_id=respondent_id)
    db.session.add(new_response)

    # Fetch the rating from the form
    survey_rating = request.form.get('survey_rating', type=int)  # Ensure it's an integer

    # Save the rating if it's provided
    if survey_rating is not None:
        new_rating = SurveyRating(survey_id=survey_id, respondent_id=respondent_id, rating=survey_rating)
        db.session.add(new_rating)

    db.session.commit()

    # Fetch questions for the survey
    questions = Question.query.filter_by(survey_id=survey_id).all()

    # Save the answers for each question
    for question in questions:
        question_key = f'question_{question.question_id}'

        # Handle different types of questions
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
            selected_options = request.form.getlist(question_key)  # Get list of selected options
            for option in selected_options:
                new_answer = Answer(
                    response_id=new_response.response_id,
                    question_id=question.question_id,
                    answer_text=option  # Save the selected option
                )
                db.session.add(new_answer)

        else:  # For text input questions
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

@routes.route('/survey-participation-data')
def survey_participation_data():
    try:
        # Query surveys with at least one response
        survey_data = (
            db.session.query(Survey.title, db.func.count(Response.response_id))
            .join(Response, Survey.survey_id == Response.survey_id)
            .group_by(Survey.title)
            .having(db.func.count(Response.response_id) > 0)
            .all()
        )

        # Prepare data for the chart
        labels = [survey[0] for survey in survey_data]
        data = [survey[1] for survey in survey_data]

        return jsonify({'labels': labels, 'data': data})

    except Exception as e:
        # Log the error to the console and return a JSON error response
        print(f"Error fetching survey data: {e}")
        return jsonify({'error': 'Failed to fetch survey data'}), 500

@routes.route('/get-participation-data') ##Over time
def get_participation_data():
    # Query database for submission counts grouped by date
    participation_data = (
        db.session.query(
            func.date(Response.submitted_at).label('submission_date'),
            func.count(Response.response_id).label('participation_count')
        )
        .group_by(func.date(Response.submitted_at))
        .order_by(func.date(Response.submitted_at))
        .all()
    )

    # Prepare data for the chart
    labels = [data.submission_date.strftime('%b %d') for data in participation_data]
    counts = [data.participation_count for data in participation_data]

    # Return data as JSON
    return jsonify({"labels": labels, "data": counts})





@routes.route('/happiness_index')
def happiness_index():
    try:
        average_rating = db.session.query(func.avg(SurveyRating.rating)).scalar()
        # Calculate the happiness index as a percentage
        if average_rating is not None:
            happiness_index_value = round((average_rating / 5) * 100, 2)  # Convert to percentage
        else:
            happiness_index_value = 0  # Default to 0 if there are no ratings
        return jsonify({'happiness_index': happiness_index_value}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@routes.route('/sentiment-data', methods=['GET'])
def sentiment_data():
    # Fetch ratings from the database
    ratings = SurveyRating.query.all()

    positive_count = sum(1 for rating in ratings if rating.rating >= 4)
    neutral_count = sum(1 for rating in ratings if rating.rating == 3)
    negative_count = sum(1 for rating in ratings if rating.rating <= 2)

    return jsonify({
        'positive': positive_count,
        'neutral': neutral_count,
        'negative': negative_count
    })





@routes.route('/user_management', methods=['GET'])
def user_management():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    lang = session.get('lang', 'en')
    current_user = Users.query.get(session['user_id'])  # The logged-in user

    # Get the search query from the URL parameters
    search_query = request.args.get('search', '')

    # Filter users based on the search query
    if search_query:
        users = Users.query.filter(
            (Users.name_ar.ilike(f'%{search_query}%')) | 
            (Users.name_en.ilike(f'%{search_query}%')) |
            (Users.email_id.ilike(f'%{search_query}%')) |
            (Users.finance_no.ilike(f'%{search_query}%'))
        ).all()
    else:
        users = Users.query.all()

    if lang == 'ar':
        return render_template('ar/user_management_page.html', user=current_user, users=users, search_query=search_query)
    
    return render_template('user_management_page.html', user=current_user, users=users, search_query=search_query)



# Route to handle user deletion
@routes.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if user_id == 1:
        flash("Admin user cannot be deleted.")
        return redirect(url_for('routes.user_management'))
    user = Users.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('routes.user_management'))




# Route to handle user editing (GET for fetching, POST for updating)
@routes.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if user_id == 1:
        flash("Admin user cannot be edited.")
        return redirect(url_for('routes.user_management'))
    user = Users.query.get(user_id)
    if request.method == 'POST':
        # Update user details
        user.name_en = request.form['name_en']
        user.name_ar = request.form['name_ar']
        user.email_id = request.form['email_id']
        user.mobile_no = request.form['mobile_no']
        user.section = request.form['section']
        
        db.session.commit()
        return redirect(url_for('routes.user_management'))
    
    # Render the user edit form (you'll need a separate HTML form for this)
    return render_template('edit_user.html', user=user)



@routes.route('/settings')
def settings():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    lang = session.get('lang', 'en')
    user = Users.query.get(session['user_id'])

    if lang == 'ar':
        return render_template('ar/settings.html', user=user)
    return render_template('settings.html', user=user)

@routes.route('/help_support')
def help_support():
    if 'user_id' not in session:
        return redirect(url_for('routes.login'))

    lang = session.get('lang', 'en')
    user = Users.query.get(session['user_id'])

    if lang == 'ar':
        return render_template('ar/help.html', user=user)
    return render_template('help.html', user=user)

@routes.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('routes.login'))
