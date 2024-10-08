from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')

# Configure MySQL Database URI with the correct password
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Basit%402024@localhost/survey_suite_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)
