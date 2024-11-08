# backend/app.py

from backend import create_app, db  # Import the create_app function and db instance

# Create the Flask application instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
