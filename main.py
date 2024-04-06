from flask import Flask
from config.main import Config 

app = Flask(__name__)

# Load configuration (adjust path if needed)
config = Config()
app.config.from_object(config)

# Import controllers (adjust filenames as needed)
from app import scrape_controller
# from app.user_controller import create_app as user_controller_app  # Example for user routes

# Register blueprints from controllers
app.register_blueprint(scrape_controller.create_app(), url_prefix='/scrape/instagram')
# app.register_blueprint(user_controller_app(), url_prefix='/users')  # Adjust prefix for user routes

if __name__ == '__main__':
    app.run(debug=True)

