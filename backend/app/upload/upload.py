# backend/app/upload/upload.py
from flask import Blueprint, request, jsonify
from app.exception.file_exceptions import *

# 블루프린트 생성
upload_blueprint = Blueprint('upload', __name__)

# 파일 업로드 라우트 정의
@upload_blueprint.route('/upload', methods=['POST'])
def upload_file():
    # file 체크
    if 'file' not in request.files:
        raise FileNotFoundError()

    file = request.files['file']

    # Check if a file was selected
    if file.filename == '':
        raise FileNameError()

    # 확장자 체크
    if not file.filename.endswith('.txt'):
        raise InvalidFileFormatError()

    # utf-8 인코딩
    try:
        content = file.read().decode('utf-8')
    except Exception as e:
        raise FileReadError(f"Error reading file: {str(e)}")

    # 테스트용
    print("Uploaded file content:")
    print(content)
    
    # Return the content in the response
    return jsonify({'message': 'File uploaded successfully!', 'content': content}), 200