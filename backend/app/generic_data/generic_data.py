from flask import Blueprint, jsonify, current_app

generic_data_blueprint = Blueprint('generic', __name__)

@generic_data_blueprint.route('/generic', methods=['GET'])
def get_analysis_data():
    # Flask 전역 상태에서 업데이트된 데이터 가져오기
    participants = current_app.config.get('participants', [])
    final_score_description = current_app.config.get('final_score_description', "아직 분석 결과가 없습니다.")
    advice = current_app.config.get('advice', "아직 분석 결과가 없습니다.")

    # 지수별 설명을 전역 상태에서 가져오도록 하여 유연성을 높임
    default_category_descriptions = {
        "개방 지수": "상대방의 감정과 생각을 얼마나 솔직하게 나누는지를 평가합니다. 개방적인 대화는 높은 점수를 받으며, 방어적이거나 닫힌 태도는 낮은 점수를 받습니다.",
        "애정 지수": "상대방이 애정이나 관심을 얼마나 표현하는지를 측정합니다. 따뜻한 말이나 애정 어린 행동이 많을수록 높은 점수를 받습니다.",
        "친밀 지수": "감정적, 신체적, 심리적 거리감을 측정합니다. 사적인 이야기나 깊은 공감이 많을수록 높은 점수를 받습니다.",
        "대화연결 지수": "대화가 얼마나 자연스럽고 끊김 없이 이어지는지를 평가합니다. 대화의 흐름이 원활하면 높은 점수를, 자주 끊기거나 어색하면 낮은 점수를 받습니다.",
        "공감 지수": "상대방이 감정이나 상황에 얼마나 공감하는지를 평가합니다. 진심으로 이해하고 반응을 보일 때 높은 점수를 받습니다.",
        "호기심 지수": "상대방이 나에 대해 얼마나 관심을 가지고 질문하거나 대화를 이끌어가는지를 측정합니다. 질문이 많고 깊이 있는 대화가 많으면 높은 점수를 받습니다.",
        "유머 지수": "대화 중 유머를 얼마나 자주 사용하는지를 평가합니다. 유머가 자주 등장하고 대화가 즐거운 경우 높은 점수를 받습니다."
    }
    
    # Flask 전역 상태에서 가져오거나 기본 설명 사용
    category_descriptions = current_app.config.get('category_descriptions', default_category_descriptions)

    # 데이터 구성하여 반환
    analysis_data = {
        "participants": participants,
        "finalScoreDescription": final_score_description,
        "categoryDescriptions": category_descriptions,
        "advice": advice
    }

    # 각 데이터의 타입 및 값 검증
    if not isinstance(participants, list):
        analysis_data["participants"] = []
        analysis_data["finalScoreDescription"] = "참가자 데이터가 유효하지 않습니다."
    if not isinstance(advice, str):
        analysis_data["advice"] = "조언 데이터가 유효하지 않습니다."

    return jsonify(analysis_data)