from __init__ import app, db
from routes import setup_routes

from routes import routes  # assuming 'routes' is your Blueprint object

# Set up routes
setup_routes(app)
app.config['SECRET_KEY'] = 'Basit@2024'


if __name__ == '__main__':
    app.run(debug=True)
