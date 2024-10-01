# backend/models.py
import bcrypt
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
from flask import current_app

db = MySQL()

# User operations
def create_user(name, phone_number, email_address, password, role_id):
    try:
        cur = db.connection.cursor()
        cur.execute("INSERT INTO user (Name, PhoneNumber, EmailAddress, Password, RoleID) VALUES (%s, %s, %s, %s, %s)",
                    (name, phone_number, email_address, password, role_id))
        db.connection.commit()
        cur.close()
    except Exception as e:
        current_app.logger.error(f"Error creating user: {str(e)}")
        raise e

# Authenticate user with email and password
def authenticate_user(email, password):
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM user WHERE EmailAddress = %s", (email,))
    user = cur.fetchone()  # Get the user from the database
    cur.close()

    # Check if the user exists and password matches
    if user and check_password_hash(user[5], password):  # Assuming user[5] is the password column
        return user  # Return user details if authentication is successful
    return None  # Return None if authentication fails


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_users():
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM user")
    users = cur.fetchall()
    cur.close()
    return users

def update_user(user_id, name, phone_number, email_address, role_id):
    cur = db.connection.cursor()
    cur.execute("UPDATE user SET Name = %s, PhoneNumber = %s, EmailAddress = %s, RoleID = %s WHERE UserID = %s",
                (name, phone_number, email_address, role_id, user_id))
    db.connection.commit()
    cur.close()

def delete_user(user_id):
    cur = db.connection.cursor()
    cur.execute("DELETE FROM user WHERE UserID = %s", (user_id,))
    db.connection.commit()
    cur.close()

# Role operations
def create_role(role_name):
    cur = db.connection.cursor()
    cur.execute("INSERT INTO Role (RoleName) VALUES (%s)", (role_name,))
    db.connection.commit()
    cur.close()

def get_roles():
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM role")
    roles = cur.fetchall()
    cur.close()
    return roles

# Survey operations
def create_survey(title, description, status, created_by):
    cur = db.connection.cursor()
    created_date = datetime.now()
    cur.execute("INSERT INTO survey (Title, Description, CreatedDate, Status, CreatedBy) VALUES (%s, %s, %s, %s, %s)",
                (title, description, created_date, status, created_by))
    db.connection.commit()
    cur.close()



def update_survey(survey_id, title, description, status):
    cur = db.connection.cursor()
    cur.execute("UPDATE survey SET Title = %s, Description = %s, Status = %s WHERE SurveyID = %s",
                (title, description, status, survey_id))
    db.connection.commit()
    cur.close()

def delete_survey(survey_id):
    cur = db.connection.cursor()
    cur.execute("DELETE FROM survey WHERE SurveyID = %s", (survey_id,))
    db.connection.commit()
    cur.close()

# Question operations
def create_question(survey_id, question_type, question_text, options):
    cur = db.connection.cursor()
    cur.execute("INSERT INTO question (SurveyID, QuestionType, QuestionText, Options) VALUES (%s, %s, %s, %s)",
                (survey_id, question_type, question_text, options))
    db.connection.commit()
    cur.close()

def get_questions(survey_id):
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM question WHERE SurveyID = %s", (survey_id,))
    questions = cur.fetchall()
    cur.close()
    return questions

def update_question(question_id, question_type, question_text, options):
    cur = db.connection.cursor()
    cur.execute("UPDATE question SET QuestionType = %s, QuestionText = %s, Options = %s WHERE QuestionID = %s",
                (question_type, question_text, options, question_id))
    db.connection.commit()
    cur.close()

def delete_question(question_id):
    cur = db.connection.cursor()
    cur.execute("DELETE FROM question WHERE QuestionID = %s", (question_id,))
    db.connection.commit()
    cur.close()

# Response operations
def create_response(survey_id, user_id, answer):
    cur = db.connection.cursor()
    submission_date = datetime.now()
    cur.execute("INSERT INTO response (SurveyID, UserID, Answer, SubmissionDate) VALUES (%s, %s, %s, %s)",
                (survey_id, user_id, answer, submission_date))
    db.connection.commit()
    cur.close()

def get_responses(survey_id):
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM response WHERE SurveyID = %s", (survey_id,))
    responses = cur.fetchall()
    cur.close()
    return responses

# Template operations
def create_template(title, description, content, created_by):
    cur = db.connection.cursor()
    cur.execute("INSERT INTO template (Title, Description, Content, CreatedBy) VALUES (%s, %s, %s, %s)",
                (title, description, content, created_by))
    db.connection.commit()
    cur.close()

def get_templates():
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM template")
    templates = cur.fetchall()
    cur.close()
    return templates

# Report operations
def create_report(survey_id, content):
    cur = db.connection.cursor()
    generated_date = datetime.now()
    cur.execute("INSERT INTO report (SurveyID, GeneratedDate, Content) VALUES (%s, %s, %s)",
                (survey_id, generated_date, content))
    db.connection.commit()
    cur.close()

def get_reports():
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM report")
    reports = cur.fetchall()
    cur.close()
    return reports

# API operations
def create_api(endpoint, description, method):
    cur = db.connection.cursor()
    cur.execute("INSERT INTO api (Endpoint, Description, Method) VALUES (%s, %s, %s)",
                (endpoint, description, method))
    db.connection.commit()
    cur.close()

def get_apis():
    cur = db.connection.cursor()
    cur.execute("SELECT * FROM api")
    apis = cur.fetchall()
    cur.close()
    return apis

    

def get_surveys():
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT Title, Description, Status, CreatedDate FROM survey")
        surveys = cur.fetchall()
        cur.close()
        return surveys
    except Exception as e:
        current_app.logger.error(f"Error fetching surveys: {str(e)}")
        raise e

def get_survey_statistics():
    try:
        cur = db.connection.cursor()
        cur.execute("""
            SELECT s.Title, COUNT(r.ResponseID) as ResponseCount
            FROM survey s
            LEFT JOIN response r ON s.SurveyID = r.SurveyID
            GROUP BY s.Title
        """)
        stats = cur.fetchall()
        cur.close()
        return stats
    except Exception as e:
        current_app.logger.error(f"Error fetching survey statistics: {str(e)}")
        raise e


def get_user_count():
    cur = db.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM user")
    user_count = cur.fetchone()[0]
    cur.close()
    return user_count

def get_average_time(survey_name):
    cur = db.connection.cursor()
    cur.execute("""
        SELECT AVG(TIMESTAMPDIFF(MINUTE, SubmissionDate, NOW())) AS AvgTime 
        FROM response r
        JOIN survey s ON r.SurveyID = s.SurveyID 
        WHERE s.Title = %s
    """, (survey_name,))
    avg_time = cur.fetchone()[0]
    cur.close()
    return avg_time
