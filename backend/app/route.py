# backend/app/route.py
from flask import Blueprint
from .upload.upload import upload_blueprint  # upload.py의 Blueprint 가져오기
from .calculate.calculate import calculate_blueprint  # calculate.py의 Blueprint 가져오기

# 블루프린트 생성
main_blueprint = Blueprint('main', __name__)

# 파일 업로드 기능 라우트 등록
main_blueprint.register_blueprint(upload_blueprint, url_prefix='/api')

# 계산 기능 라우트 등록
main_blueprint.register_blueprint(calculate_blueprint, url_prefix='/api')