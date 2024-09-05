from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # React와의 CORS 문제 해결
    
    # Configurations and routes registration
    from app.routes import main_blueprint
    app.register_blueprint(main_blueprint)
    
    # 파일 업로드 폴더 설정
    app.config['UPLOAD_FOLDER'] = 'uploads'

    return app