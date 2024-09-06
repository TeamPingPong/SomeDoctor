import json
import os
from openai import OpenAI

def call_gpt_api(model, prompt, conversation, max_tokens=2000, temperature=0.7):
    try:
        client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": conversation}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        print("GPT 호출 성공, 응답:", response)  # GPT 호출 성공 시 응답 출력
    except Exception as e:
        print("GPT 호출 중 예외 발생:", e)
        return None
    return response


def chatAnalyze(conversation, user1, user2):
    print("=== chatAnalyze 시작 ===")  # 디버그 시작 로그
    print(f"전달된 대화 내용: {conversation}")  # 대화 내용 출력
    print(f"전달된 사용자: user1={user1}, user2={user2}")  # 사용자 정보 출력

    # OpenAI API 키 설정
    model = "gpt-4"

    # 프롬프트 설정 (프롬프트 수정 불가 요청에 따라 기존 유지)
    prompt = f"""
    당신은 남녀의 썸을 진단하고, 둘이 연인으로 발전할 가능성을 분석합니다. 향후 두 사람의 관계 발전을 위한 도움이 되는 조언을 제시합니다.
    주어진 대화를 바탕으로 {user1}과 {user2}의 관계 지수를 파악합니다. 관계 지수는 7개로 구성되고(개방 지수, 애정 지수, 친밀 지수, 대화연결 지수, 공감 지수, 호기심 지수, 유머 지수) 각각 100점 만점입니다.
    두 명의 대화이므로, {user1}과 {user2}의 지수를 따로 계산하고 각 지수에 대한 이유도 출력합니다.
    연인으로 관계 발전을 위한 조언을 500~600자로 작성합니다.
    json 형식으로 출력합니다.
    
    {user1}과 {user2}의 관계 지수 점수
    점수 산출 근거 및 이유 (user별로 모든 이유를 하나의 글로 이어 붙여서 존댓말로)
    조언 (실질적이고 구체적으로)
    """

    # GPT API 호출
    response = call_gpt_api(model, prompt, conversation)
    
    if response is None:
        return {"error": "GPT 호출 실패"}
    
    try:
        # Response 처리
        result_content = response.choices[0].message.content
        print("GPT 응답 내용:", result_content)  # GPT 응답 내용 출력
        result = json.loads(result_content)
    except Exception as e:
        print("GPT 응답 파싱 중 오류 발생:", e)
        return {"error": "GPT 응답 파싱 실패", "details": str(e)}

    print("=== chatAnalyze 종료 ===")  # 디버그 종료 로그
    return result