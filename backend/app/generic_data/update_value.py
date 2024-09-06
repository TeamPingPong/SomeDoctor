import json
from flask import current_app

# 호감도 계산에 사용될 가중치
weights = {
    "개방 지수": 0.15,
    "애정 지수": 0.20,
    "친밀 지수": 0.10,
    "대화연결 지수": 0.10,
    "공감 지수": 0.20,
    "호기심 지수": 0.20,
    "유머 지수": 0.05
}

# 지수별 설명 기준
descriptions = {
    "개방 지수": {
        "높음": "두 사람은 서로의 감정과 생각을 솔직하게 나누며, 신뢰를 바탕으로 한 깊은 대화를 이어갑니다.",
        "중간": "기본적인 대화는 원활하지만, 감정이나 생각을 깊이 나누는 데에는 한계가 있습니다.",
        "낮음": "서로에게 마음을 열지 않으며, 대화에서 자신을 표현하는 데 주저함이 있습니다."
    },
    "애정 지수": {
        "높음": "두 사람은 서로에 대한 애정을 깊이 느끼고 있으며, 이를 적극적으로 표현합니다.",
        "중간": "기본적인 호감과 애정은 있지만, 이를 표현하는 방식에 있어 다소 제한적일 수 있습니다.",
        "낮음": "두 사람 사이에서 애정 표현이 거의 보이지 않으며, 감정적으로 거리가 느껴집니다."
    },
    "친밀 지수": {
        "높음": "두 사람은 감정적, 신체적으로 매우 가까운 관계를 형성하고 있습니다.",
        "중간": "기본적인 친밀감을 공유하지만, 더 깊은 연결을 위해서는 감정적 소통이 더 필요합니다.",
        "낮음": "서로에 대한 감정적 친밀감이 부족하며, 거리감이 느껴집니다."
    },
    "대화연결 지수": {
        "높음": "두 사람의 대화는 매우 자연스럽고 유연하게 이어집니다.",
        "중간": "대화가 기본적으로 잘 이어지지만, 때때로 어색한 침묵이나 주제 전환이 어려운 상황이 발생할 수 있습니다.",
        "낮음": "대화가 자주 끊기며, 서로의 말에 대한 이해나 관심이 부족합니다."
    },
    "공감 지수": {
        "높음": "두 사람은 서로의 감정과 상황을 깊이 이해하고, 이에 대해 진심으로 공감합니다.",
        "중간": "기본적인 공감은 있지만, 상대방의 감정이나 상황을 깊이 이해하는 데에 한계가 있을 수 있습니다.",
        "낮음": "상대방의 감정이나 상황을 이해하는 데 어려움을 겪고 있으며, 공감 능력이 부족합니다."
    },
    "호기심 지수": {
        "높음": "상대방에 대한 호기심이 매우 강하며, 그에 대해 더 알고자 하는 욕구가 큽니다.",
        "중간": "기본적인 호기심은 있지만, 그다지 깊은 질문이나 대화를 시도하지는 않는 편입니다.",
        "낮음": "상대방에 대한 호기심이 거의 없으며, 상대방에 대해 더 알고자 하는 의지가 부족합니다."
    },
    "유머 지수": {
        "높음": "두 사람은 유머 코드가 잘 맞으며, 대화에서 자주 웃음을 나눕니다.",
        "중간": "가끔은 유머가 대화에 섞이지만, 대화의 주요 요소는 아닙니다.",
        "낮음": "유머 코드가 맞지 않으며, 대화에서 웃음이나 장난이 거의 없습니다."
    }
}

# 점수의 높음, 중간, 낮음 분류 함수
def categorize_score(value):
    if value >= 85:
        return "높음"
    elif 60 <= value < 85:
        return "중간"
    else:
        return "낮음"

# 애정 단계 계산 함수
def calculate_stage(score):
    if 0 <= score <= 24:
        return 1
    elif 25 <= score <= 49:
        return 2
    elif 50 <= score <= 74:
        return 3
    elif 75 <= score <= 100:
        return 4
    else:
        return None

# 관계 유형 결정 함수
def determine_relationship_type(user1_score, user2_score):
    user1_stage = calculate_stage(user1_score)
    user2_stage = calculate_stage(user2_score)

    if user1_stage == 4 and user2_stage == 4:
        return "핑크빛 두근두근형 (Mutual Sparks)"
    elif user1_stage == 1 and user2_stage == 1:
        return "서로 관심 無형 (Indifferent Pair)"
    elif (user1_stage == 1 and user2_stage == 4) or (user1_stage == 4 and user2_stage == 1):
        return "한쪽만 불도저형 (One-Sided Flame)"
    elif (user1_stage == 1 and user2_stage == 2) or (user1_stage == 2 and user2_stage == 1):
        return "살짝 거리두기형 (Subtle Distance)"
    elif (user1_stage == 1 and user2_stage == 3) or (user1_stage == 2 and user2_stage == 3) or (user1_stage == 3 and user2_stage == 2) or (user1_stage == 3 and user2_stage == 1):
        return "살짝 거리두기형 (Subtle Distance)"
    elif (user1_stage == 2 and user2_stage == 4) or (user1_stage == 4 and user2_stage == 2):
        return "적극적 직진형 (Confident Chaser)"
    elif (user1_stage == 3 and user2_stage == 4) or (user1_stage == 4 and user2_stage == 3):
        return "기대의 움틀형 (Budding Anticipation)"
    elif user1_stage == 2 and user2_stage == 2:
        return "잔잔한 물결형 (Even Tides)"
    elif user1_stage == 3 and user2_stage == 3:
        return "잔잔한 물결형 (Even Tides)"
    else:
        return "Unknown Type"

def update_data_values(gpt_response):
    try:
        # 응답을 문자열로 받았다면 JSON으로 파싱
        if isinstance(gpt_response, str):
            gpt_response = gpt_response.strip()
            gpt_result = json.loads(gpt_response)
        else:
            gpt_result = gpt_response

        participants = []

        # 참가자 데이터를 순회하며 처리
        for user, data in gpt_result.items():
            # 점수 산출 근거 및 이유와 조언은 참가자가 아니므로 건너뜀
            if user in ["점수 산출 근거 및 이유", "조언"]:
                continue

            # 데이터가 딕셔너리인지 확인
            if not isinstance(data, dict):
                print(f"{user}의 데이터가 dict가 아닙니다. 데이터: {data}")
                continue

            # 점수 추출 및 호감도 점수 계산
            scores = {key: value for key, value in data.items() if key in weights}
            interest_score = sum(scores[key] * weights[key] for key in scores)
            stage = calculate_stage(interest_score)

            # 지수별 설명 추가 및 점수에 따른 상태 평가
            radar_data = {}
            for key, value in scores.items():
                status = categorize_score(value)
                radar_data[key] = {
                    "value": value,
                    "status": status,
                    "description": descriptions[key][status]
                }

            # 참가자 데이터 추가
            participants.append({
                "name": user,
                "score": interest_score,
                "stage": stage,
                "radarData": radar_data,
                "reasoning": gpt_result.get("점수 산출 근거 및 이유", "근거 없음.")
            })

        # 두 명의 참가자가 있을 때 관계 유형 결정
        if len(participants) == 2:
            relationship_type = determine_relationship_type(participants[0]['score'], participants[1]['score'])
            participants[0]['relationship_type'] = relationship_type
            participants[1]['relationship_type'] = relationship_type

        # 조언 내용 추출
        advice = gpt_result.get("조언", "추가적인 조언 없음.")

        # Flask 애플리케이션 상태 업데이트
        current_app.config['participants'] = participants
        current_app.config['advice'] = advice

        print("업데이트된 participants:", participants)
        print("업데이트된 advice:", advice)

    except json.JSONDecodeError as e:
        print(f"GPT 응답 파싱 중 오류 발생: {str(e)}")
    except Exception as e:
        print(f"예기치 않은 오류 발생: {str(e)}")