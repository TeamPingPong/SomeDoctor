# backend/app/upload/upload.py
from flask import Blueprint,request, jsonify
from app.exception.file_exceptions import *

upload_blueprint = Blueprint('upload',__name__)

@upload_blueprint.route('upload',methods=['POST'])
def upload_file():
    # file체킹
    if 'file' not in request.files:
        raise FileNotFoundError()

    file = request.files['file']
    
    # Check if a file was selected
    if file.filename == '':
        raise FileNameError()

    # 확장자 체킹
    if not file.filename.endswith('.txt'):
        raise InvalidFileFormatError()

    # utf-8인코딩
    try:
        content = file.read().decode('utf-8')
    except Exception as e:
        raise FileReadError(f"Error reading file: {str(e)}")

    # 테스트용
    print("Uploaded file content:")
    print(content)
    
    # Return the content in the response
    return jsonify({'message': 'File uploaded successfully!', 'content': content}), 200