import re
import pandas as pd

def prep_cnt_msg(msg):
    '''
    Description :
    - '이모티콘' 제거
    - '사진 *장', "사진" 제거
    '''
    if msg == "사진":
        return ""
    msg = re.sub(r'이모티콘', '', msg).strip()
    msg = re.sub(r'사진 \d+장', '', msg).strip()
    return msg

def katalk_msg_parse(lines):
    """
    카카오톡 메시지 파일을 DataFrame으로 변환합니다.
    """
    print("=== katalk_msg_parse 시작 ===")  # 디버그 시작 로그
    my_katalk_data = []
    katalk_msg_pattern = re.compile(r"(\d{4}\.\s?\d{1,2}\.\s?\d{1,2}\.\s오[전후]\s\d{1,2}:\d{2}),\s(.*?):\s(.*)")

    for line in lines:
        print(f"처리 중인 라인: {line}")  # 현재 처리 중인 라인 출력
        match = katalk_msg_pattern.match(line)
        if match:
            date_time = match.group(1)
            user_name = match.group(2).strip()
            text = match.group(3).strip()
            print(f"추출된 데이터 - 날짜: {date_time}, 사용자: {user_name}, 메시지: {text}")  # 추출된 데이터 출력
            my_katalk_data.append({'Date': date_time, 'User': user_name, 'Message': text})

    df = pd.DataFrame(my_katalk_data)
    print("생성된 DataFrame:\n", df.head())  # 생성된 DataFrame의 상위 5개 출력
    print("=== katalk_msg_parse 종료 ===")  # 디버그 종료 로그
    return df

def file2DataFrame(file, file_type: str):
    '''
    Description : txt/csv 파일을 dataFrame 처리
    '''
    if file_type == 'txt':
        txtDf = katalk_msg_parse(file)
    elif file_type == 'csv':
        txtDf = pd.read_csv(file)
    else:
        raise ValueError("지원하지 않는 파일 형식입니다. .txt 또는 .csv 파일만 지원합니다.")

    return txtDf

def df2Prompt(df, tokens=1000):
    """
    DataFrame 처리된 대화내용을 받아 1000자까지 처리하고 두 명의 사용자를 반환합니다.
    """
    print("=== df2Prompt 시작 ===")  # 디버그 시작 로그
    result = []
    temp_conversation = df.iloc[len(df) - 1]['Message']
    previous_user = df.iloc[len(df) - 1]['User']
    cur_words = ''
    temp_conversation = prep_cnt_msg(temp_conversation)
    users = set()

    print(f"초기 메시지: {temp_conversation}, 초기 사용자: {previous_user}")  # 초기 메시지와 사용자 출력

    for i in range(len(df) - 2, -1, -1):
        if len(cur_words) > tokens:
            print("토큰 제한 도달, 처리 중단")  # 토큰 제한 도달 시 로그 출력
            break

        current_user = df.iloc[i]['User']
        current_message = df.iloc[i]['Message']
        current_message = prep_cnt_msg(current_message)

        print(f"현재 메시지: {current_message}, 현재 사용자: {current_user}")  # 현재 메시지와 사용자 출력

        if current_user == previous_user:
            temp_conversation += ' ' + current_message
        else:
            result.append(temp_conversation)
            temp_conversation = current_message

        previous_user = current_user
        users.add(current_user)
        cur_words += current_message

    result.append(temp_conversation)
    print(f"추출된 대화 내용: {result}")  # 추출된 대화 내용 출력

    # 사용자 수가 2명 이상인지 확인
    if len(users) < 2:
        print("사용자가 두 명 이상 존재하지 않습니다.")  # 사용자 수가 부족할 때 로그 출력
        raise ValueError("사용자가 두 명 이상 존재하지 않습니다. 대화 데이터를 확인하세요.")

    users_list = list(users)
    user1 = users_list[0]
    user2 = users_list[1]
    print(f"추출된 사용자: user1={user1}, user2={user2}")  # 추출된 사용자 출력
    print("=== df2Prompt 종료 ===")  # 디버그 종료 로그

    return str(result[::-1])[1:-1], user1, user2