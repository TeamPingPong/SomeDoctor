from flask import Blueprint, request, jsonify
import pandas as pd
import re

# 블루프린트 생성
upload_blueprint = Blueprint('upload', __name__)

@upload_blueprint.route('/upload', methods=['POST'])
def upload_file():
    """
    파일을 업로드하여 카카오톡 대화 내용을 파싱하고 CSV로 변환하는 엔드포인트입니다.
    """
    # 파일이 요청에 포함되어 있는지 확인
    if 'file' not in request.files:
        return jsonify({'error': '파일이 존재하지 않습니다.'}), 400

    file = request.files['file']
    
    # 파일명이 비어 있는지 확인
    if file.filename == '':
        return jsonify({'error': '파일명이 비어 있습니다.'}), 400

    # 확장자 확인 (.txt 파일만 허용)
    if not file.filename.endswith('.txt'):
        return jsonify({'error': '지원되지 않는 파일 형식입니다. .txt 파일만 업로드하세요.'}), 400

    try:
        # 텍스트 파일 읽기
        txt_content = file.read().decode('utf-8')
        # 텍스트 내용을 파싱하여 DataFrame으로 변환
        df = parse_kakao_talk(txt_content)
        
        # 간단한 요약을 출력하여 변환 체크
        summary = {
            'total_messages': len(df),  # 총 메시지 개수
            'sample_messages': df.head(5).to_dict(orient='records')  # 상위 5개의 메시지를 샘플로 반환
        }
        
        # 변환된 데이터를 JSON으로 반환
        return jsonify({'message': '파일이 성공적으로 업로드되었습니다!', 'summary': summary}), 200
    except Exception as e:
        return jsonify({'error': f'파일 처리 중 오류가 발생했습니다: {str(e)}'}), 500


def parse_kakao_talk(txt_content):
    """
    카카오톡 대화 내용을 CSV로 변환하는 함수입니다.
    """
    # 정규 표현식을 사용하여 날짜와 메시지를 추출합니다.
    date_pattern = re.compile(r"\d{4}년 \d{1,2}월 \d{1,2}일 [월화수목금토일]요일")
    message_pattern = re.compile(r"(\d{4}\. \d{1,2}\. \d{1,2}\. (오전|오후) \d{1,2}:\d{2}), (.*?): (.*)")

    lines = txt_content.splitlines()  # 텍스트 파일을 줄 단위로 분리
    data = []  # 데이터를 저장할 리스트
    current_date = None  # 현재 대화의 날짜를 저장할 변수

    for line in lines:
        # 날짜 패턴이 있는 경우 현재 날짜로 설정
        if date_pattern.match(line):
            current_date = line.strip()
        # 메시지 패턴이 있는 경우 데이터를 추출하여 리스트에 추가
        elif message_pattern.match(line):
            time, period, sender, message = message_pattern.findall(line)[0]
            timestamp = f"{current_date} {time}"  # 날짜와 시간을 합쳐 타임스탬프 생성
            data.append([timestamp, sender, message])  # 데이터 리스트에 추가

    # 데이터를 DataFrame으로 변환
    df = pd.DataFrame(data, columns=["Timestamp", "Sender", "Message"])
    print(df)
    return df