# backend/app/calculate.py
from flask import Blueprint, request, jsonify

# 블루프린트 생성
calculate_blueprint = Blueprint('calculate', __name__)

# 계산 수식을 적용하는 함수
@calculate_blueprint.route('/calculate', methods=['POST'])
def calculate_data():
    # 요청에서 JSON 데이터 추출
    data = request.json.get('data', {})

    # 로그 출력으로 데이터 확인
    print("Received Data:", data)

    # JSON 데이터에서 필요한 지수를 추출
    boundary_index = float(data.get('경계 지수', 0))
    affection_index = float(data.get('애정 지수', 0))
    intimacy_index = float(data.get('친밀 지수', 0))
    conversation_flow_index = float(data.get('대화 흐름 지수', 0))
    respect_empathy_index = float(data.get('상호존중 및 공감 지수', 0))
    curiosity_index = float(data.get('호기심 지수', 0))
    humor_index = float(data.get('유머 지수', 0))

    # 로그로 각 값 확인
    print(f"Boundary Index: {boundary_index}, Affection Index: {affection_index}, Intimacy Index: {intimacy_index}")
    print(f"Conversation Flow Index: {conversation_flow_index}, Respect Empathy Index: {respect_empathy_index}")
    print(f"Curiosity Index: {curiosity_index}, Humor Index: {humor_index}")

    # 수식에 따라 H 값을 계산
    H = (
        (boundary_index * 0.15) +
        (affection_index * 0.20) +
        (intimacy_index * 0.25) +
        (conversation_flow_index * 0.10) +
        (respect_empathy_index * 0.20) +
        (curiosity_index * 0.05) +
        (humor_index * 0.05)
    ) / 1.00

    # 계산된 결과 반환
    print(f"Calculated H: {H}")
    return jsonify({"H": H})