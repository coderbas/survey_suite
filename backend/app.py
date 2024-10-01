from flask import Flask
from flask_mysqldb import MySQL
from routes import setup_routes

# Configure Flask app
app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Basit@2024'  # Replace with your MySQL root password
app.config['MYSQL_DB'] = 'survey_suite_db'

# Set up secret key for session
app.secret_key = 'Basit@2024'

# Initialize MySQL
mysql = MySQL(app)
db = mysql

# Setup routes
setup_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
