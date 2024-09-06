# backend/app/route.py
from flask import Blueprint
from .upload.upload import upload_blueprint  # upload.py의 Blueprint 가져오기
from .generic_data.generic_data import generic_data_blueprint

# 블루프린트 생성
main_blueprint = Blueprint('main', __name__)

# 파일 업로드 기능 라우트 등록
main_blueprint.register_blueprint(upload_blueprint, url_prefix='/api')


main_blueprint.register_blueprint(generic_data_blueprint, url_prefix='/api')