from flask import Blueprint, request, jsonify
from app.exception.file_exceptions import (
    FileNotFoundError,
    FileNameError,
    InvalidFileFormatError,
    FileReadError,
    TooManyParticipantsError
)
from app.AI.preprocess import file2DataFrame, df2Prompt
from app.AI.MainGPT import chatAnalyze
from app.generic_data.update_value import update_data_values  # update_value.py에서 함수 가져오기
import pandas as pd
import io

upload_blueprint = Blueprint('upload', __name__)

@upload_blueprint.route('/upload', methods=['POST'])
def upload_file():
    try:
        # 파일 유무 확인
        if 'file' not in request.files:
            raise FileNotFoundError()

        file = request.files['file']
        # 파일 이름 확인
        if file.filename == '':
            raise FileNameError()
        
        # 파일 형식 확인
        if not (file.filename.endswith('.txt') or file.filename.endswith('.csv')):
            raise InvalidFileFormatError()

        file_type = 'txt' if file.filename.endswith('.txt') else 'csv'

        # 파일을 읽고 데이터프레임으로 변환
        if file_type == 'txt':
            content = file.read().decode('utf-8').splitlines()  # 파일을 문자열로 읽기
            df = file2DataFrame(content, file_type)
        else:
            stream = io.StringIO(file.read().decode('utf-8'))
            df = pd.read_csv(stream)

        # 전처리 및 GPT 호출
        conversation, user1, user2 = df2Prompt(df)
        gpt_result = chatAnalyze(conversation, user1, user2)  # GPT 호출
        
        # 결과 확인 및 업데이트
        if not isinstance(gpt_result, dict):
            return jsonify({'error': 'Invalid GPT result format'}), 500

        # GPT 결과를 업데이트
        update_data_values(gpt_result)

        return gpt_result

    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 400
    except FileNameError:
        return jsonify({'error': 'No file selected'}), 400
    except InvalidFileFormatError:
        return jsonify({'error': 'Invalid file format. Only .txt and .csv are supported.'}), 400
    except TooManyParticipantsError:
        return jsonify({'error': 'Too many participants in the conversation'}), 400
    except FileReadError as e:
        return jsonify({'error': 'File processing failed', 'details': str(e)}), 500
    except Exception as e:
        # 상세한 오류 정보를 제공
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500


@upload_blueprint.route('/health', methods=['GET'])
def health_check():
    return "ok", 200