# backend/app/__init__.py
from flask import Flask
from .route import main_blueprint

def create_app():
    app = Flask(__name__)
    
    # 블루프린트 등록
    app.register_blueprint(main_blueprint)
    
    return app

