# backend/app/route.py
from flask import Blueprint
from .upload.upload import upload_file

# 블루프린트 생성
main_blueprint = Blueprint('main', __name__)

# 파일 업로드 라우트 등록
main_blueprint.route('/upload', methods=['POST'])(upload_file)