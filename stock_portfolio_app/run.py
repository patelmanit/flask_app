from flask import Flask, make_response, Response, request, jsonify
from flask_cors import CORS
from config import Config
from models import db
from routing import init_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize CORS with your Flask app
    CORS(app, 
         resources={r"/*": {
             "origins": '*',
             "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
             "allow_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True
         }})
    
    db.init_app(app)
    init_routes(app)
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)