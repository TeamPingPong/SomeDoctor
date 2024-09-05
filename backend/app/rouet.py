from flask import Blueprint, request, jsonify
from gpt.gpt_service import analyze_conversation_with_gpt

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/upload', methods=['POST'])
def upload_file():
    """파일을 업로드하고 AI 모델로 분석 요청을 보내는 엔드포인트"""
    if 'file' not in request.files:
        return jsonify({"error": "파일이 업로드되지 않았습니다."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "파일 이름이 비어있습니다."}), 400

    # 파일 내용을 메모리에서 바로 읽기
    conversation = file.read().decode('utf-8')

    # GPT를 통한 대화 분석
    response = analyze_conversation_with_gpt(conversation)

    return jsonify(response), 200