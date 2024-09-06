from flask import Blueprint, request, jsonify
from app.exception.file_exceptions import (
    FileNotFoundError, 
    FileNameError, 
    InvalidFileFormatError, 
    FileReadError, 
    TooManyParticipantsError
)
import csv
import io
import re

upload_blueprint = Blueprint('upload', __name__)

@upload_blueprint.route('upload', methods=['POST'])
def upload_file():
    # 파일 체크
    if 'file' not in request.files:
        raise FileNotFoundError()

    file = request.files['file']
    
    # 파일이 선택되었는지 확인
    if file.filename == '':
        raise FileNameError()

    # 파일 확장자 확인
    if not (file.filename.endswith('.txt') or file.filename.endswith('.csv')):
        raise InvalidFileFormatError()

    # 고유 발화자를 저장할 집합
    participants = set()

    # 발화자 이름을 추출하기 위한 정규 표현식 패턴
    line_pattern = re.compile(r"\d{4}\.\s\d{1,2}\.\s\d{1,2}\.\s오[전후]\s\d{1,2}:\d{2},\s(.*?):")

    # 파일 유형에 따라 내용 읽기
    try:
        if file.filename.endswith('.txt'):
            # .txt 파일 읽고 디코딩
            content = file.read().decode('utf-8')
            lines = content.splitlines()
            for line in lines:
                match = line_pattern.match(line)
                if match:
                    participants.add(match.group(1))
            response_content = {'content': lines}  # 라인을 나누어 반환
        elif file.filename.endswith('.csv'):
            # .csv 파일 읽고 디코딩
            stream = io.StringIO(file.read().decode('utf-8'))
            csv_reader = csv.reader(stream)
            headers = next(csv_reader, None)  # 첫 번째 행을 헤더로 읽기
            content = [row for row in csv_reader]

            # 'User' 열에서 발화자 추출
            user_index = headers.index('User') if headers and 'User' in headers else -1
            if user_index != -1:
                for row in content:
                    participants.add(row[user_index])

            response_content = {'content': content}

    except Exception as e:
        raise FileReadError(f"Error reading file: {str(e)}")

    # 발화자 수가 2명을 초과하는지 체크
    if len(participants) > 2:
        raise TooManyParticipantsError()

    # 응답 반환
    return jsonify({'message': 'File uploaded successfully!', **response_content}), 200