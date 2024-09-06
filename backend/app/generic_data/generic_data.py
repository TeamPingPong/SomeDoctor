# generic_data.py
from flask import Blueprint, jsonify
from .data_value import *

generic_data_blueprint = Blueprint('generic', __name__)
@generic_data_blueprint.route('/generic', methods=['GET'])

def get_analysis_data():
    # 실제로는 이곳에서 데이터를 분석하고 결과를 생성해야 합니다
    analysis_data = {
        'yourScore': your_score,
        'partnerScore': partner_score,
        'finalScore': final_score,
        'finalScoreDescription': final_score_description,
        'radarData': {
            'labels': radar_labels,
            'datasets': [
                {
                    'label': '대화 분석',
                    'data': radar_data,
                    'backgroundColor': radar_background_color,
                    'borderColor': radar_border_color,
                    'borderWidth': radar_border_width,
                },
            ],
        },
        'categoryDescriptions': category_descriptions,
        'advice': advice
    }
    return jsonify(analysis_data)