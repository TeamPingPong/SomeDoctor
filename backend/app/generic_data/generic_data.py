# generic_data.py
from flask import Blueprint, jsonify
from .data_value import participants, final_score, final_score_description, category_descriptions, advice

generic_data_blueprint = Blueprint('generic', __name__)

@generic_data_blueprint.route('/generic', methods=['GET'])
def get_analysis_data():
    # 변수로부터 데이터를 가져와서 JSON 응답을 구성
    analysis_data = {
        "participants": participants, #추후 인원 증가에 대한 생각할것
        "finalScore": final_score,
        "finalScoreDescription": final_score_description,
        "categoryDescriptions": category_descriptions,
        "advice": advice
    }
    return jsonify(analysis_data)