import bcrypt
from __init__ import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    EmailAddress = db.Column(db.String(100), unique=True, nullable=False)
    PhoneNumber = db.Column(db.String(15), nullable=True)
    password = db.Column(db.String(255), nullable=False)  # Password hash
    RoleID = db.Column(db.Integer, db.ForeignKey('role.RoleID'), nullable=False)

    role = db.relationship('Role', backref='users')

class Role(db.Model):
    __tablename__ = 'role'
    RoleID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    RoleName = db.Column(db.String(50), nullable=False)

class Survey(db.Model):
    __tablename__ = 'survey'
    survey_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Question(db.Model):
    __tablename__ = 'question'
    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.survey_id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), nullable=False)

class Option(db.Model):
    __tablename__ = 'questionoption'
    option_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False)
    option_text = db.Column(db.Text, nullable=False)

class Response(db.Model):
    __tablename__ = 'response'
    response_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.survey_id'), nullable=False)
    respondent_id = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

class Answer(db.Model):
    __tablename__ = 'answer'
    answer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    response_id = db.Column(db.Integer, db.ForeignKey('response.response_id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False)
    answer_text = db.Column(db.Text, nullable=False)

# Create tables if they don’t exist
def init_db(app):
    with app.app_context():
        db.create_all()
# Create User
def create_user(name, phone_number, email_address, password, role_id):
    hashed_password = generate_password_hash(password)
    new_user = User(name=name, phone_number=phone_number, email_address=email_address, password=hashed_password, role_id=role_id)
    db.session.add(new_user)
    db.session.commit()

# Authenticate User
def authenticate_user(email, password):
    user = User.query.filter_by(email_address=email).first()  # Corrected attribute
    if user and check_password_hash(user.password, password):
        return user  # Authentication successful
    return None  # Authentication failed


# Update User
def update_user(user_id, name, phone_number, email_address, role_id):
    user = User.query.get(user_id)
    if user:
        user.name = name
        user.phone_number = phone_number
        user.email_address = email_address
        user.role_id = role_id
        db.session.commit()

# Delete User
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))



# Create Role
def create_role(role_name):
    new_role = Role(role_name=role_name)
    db.session.add(new_role)
    db.session.commit()

# Get Roles
def get_roles():
    return Role.query.all()

# Create Survey
def create_survey(title, description, created_by):
    new_survey = Survey(title=title, description=description, created_by=created_by)
    db.session.add(new_survey)
    db.session.commit()
    return new_survey

# Create Question
def create_question(survey_id, question_type, question_text, options=None):
    new_question = Question(survey_id=survey_id, question_text=question_text, question_type=question_type)
    db.session.add(new_question)
    db.session.commit()

    # Add options if they exist
    if options:
        for option_text in options:
            new_option = Option(question_id=new_question.question_id, option_text=option_text)
            db.session.add(new_option)
        db.session.commit()
# Create Response
def create_response(survey_id, respondent_id):
    new_response = Response(survey_id=survey_id, respondent_id=respondent_id)
    db.session.add(new_response)
    db.session.commit()
    return new_response

# Create Answer
def create_answer(response_id, question_id, answer_text):
    new_answer = Answer(response_id=response_id, question_id=question_id, answer_text=answer_text)
    db.session.add(new_answer)
    db.session.commit()

def get_survey_statistics():
    stats = db.session.query(
        Survey.title,
        db.func.count(Response.response_id).label('ResponseCount')
    ).outerjoin(Response, Survey.survey_id == Response.survey_id).group_by(Survey.title).all()
    return stats
