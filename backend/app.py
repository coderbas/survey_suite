from flask import Flask, session
from flask_mysqldb import MySQL
from routes import setup_routes

app = Flask(__name__)

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Basit@2024'  # Replace with your MySQL root password
app.config['MYSQL_DB'] = 'survey_suite_db'

# Set up secret key for session
app.secret_key = 'Basit@2024'  # Make sure this is a strong secret key

mysql = MySQL(app)

setup_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
