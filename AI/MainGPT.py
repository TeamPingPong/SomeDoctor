from preprocess import *
from openai import OpenAI
import json
import os

def call_gpt_api(model, prompt, conversation, max_tokens=2000, temperature=0.7):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": conversation}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
    except :
        print("예외처리 되었습니다.")
        return None
    return response



def chatAnalyze(conversation) :
    client = OpenAI()
    # OpenAI API 키 설정
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    model = "gpt-4o-mini"

    # 프롬프트 설정
    prompt = f"""
    당신은 남녀의 썸을 진단하고, 둘이 연인으로 발전할 가능성을 분석합니다. 향후 두 사람의 관계 발전을 위한 도움이 되는 조언을 제시합니다.
    주어진 대화를 바탕으로 {user1}과 {user2}의 관계 지수를 파악합니다. 관계 지수는 7개로 구성되고(개방 지수, 애정 지수, 친밀 지수, 대화연결 지수, 공감 지수, 호기심 지수, 유머 지수) 각각 100점 만점입니다.
    두 명의 대화이므로, {user1}과 {user2}의 지수를 따로 계산하고 각 지수에 대한 이유도 출력합니다.
    연인으로 관계 발전을 위한 조언을 500~600자로 작성합니다.
    json 형식으로 출력합니다.
    1. {user1}과 {user2}의 관계 지수 점수
    2. 점수 산출 근거 및 이유 (index별로 나누지 않고 모든 이유를 하나의 글로 이어 붙이기)
    3. 조언 (세부적일수록 좋음)
    """
    
    # API 호출
    response = call_gpt_api(model, prompt, conversation)

    # Response 처리
    result = json.loads(response.choices[0].message.content[8:-4])
    return result