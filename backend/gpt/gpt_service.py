#아래에 코드는 예시 코드입니다!! 수정하실수 있습니다!

import openai

# OpenAI API 키 설정 (실제 프로젝트에서는 환경 변수나 .env 파일 사용 권장)
openai.api_key = "YOUR_OPENAI_API_KEY"

def analyze_conversation_with_gpt(conversation):
    """GPT 모델을 사용하여 대화 내용을 분석하고 추천 답변을 제공"""
    try:
        # GPT 모델에게 대화 내용을 분석하도록 요청
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 대화 분석 전문가입니다."},
                {"role": "user", "content": f"다음 대화를 분석하고 감정을 분류하고, 감정을 수치로 표현해주세요: {conversation}"}
            ],
            max_tokens=500,
            temperature=0.7
        )

        # GPT의 분석 결과를 텍스트로 추출
        analysis_text = response.choices[0].message['content']

        # 감정 분석 결과를 수치화하는 함수 호출
        emotion_scores = calculate_emotion_scores(analysis_text)

        return {
            "message": "파일 분석 성공",
            "analysis": analysis_text,
            "emotion_scores": emotion_scores
        }
    except Exception as e:
        return {"error": str(e)}

def calculate_emotion_scores(analysis_text):
    """
    GPT 분석 결과 텍스트를 기반으로 감정을 수치화하는 함수.
    단순한 키워드 기반 분석을 통해 감정별 점수를 계산.
    """
    # 감정 키워드와 초기 점수 설정
    emotions = {
        "anger": 0,
        "sadness": 0,
        "joy": 0,
        "fear": 0,
        "surprise": 0
    }

    # 간단한 키워드 기반 분석 (감정 키워드가 포함된 횟수로 점수 계산)
    keywords = {
        "anger": ["화남", "분노", "짜증"],
        "sadness": ["슬픔", "눈물", "우울"],
        "joy": ["기쁨", "행복", "웃음"],
        "fear": ["두려움", "걱정", "불안"],
        "surprise": ["놀람", "충격", "경악"]
    }

    # 감정 키워드에 따라 점수를 부여
    for emotion, words in keywords.items():
        for word in words:
            emotions[emotion] += analysis_text.count(word)

    # 점수를 백분율로 변환하여 합계가 100이 되도록 조정
    total = sum(emotions.values())
    if total > 0:
        for emotion in emotions:
            emotions[emotion] = round((emotions[emotion] / total) * 100, 2)
    else:
        # 모든 점수가 0일 경우 기본 값을 설정
        emotions = {emotion: 0 for emotion in emotions}

    return emotions