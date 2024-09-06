import re
import pandas as pd

def prep_cnt_msg(msg) :
    '''
    Description :
    - '이모티콘' 제거
    - '사진 *장', "사진" 제거
    '''
    if msg == "사진" :
        return ""
    msg = re.sub(r'이모티콘', '', msg).strip()
    msg = re.sub(r'사진 \d+장', '', msg).strip()
    return msg


# txt to dataFrame
def katalk_msg_parse(file_path):
    my_katalk_data = list()
    katalk_msg_pattern = r"[0-9]{4}[년.] [0-9]{1,2}[월.] [0-9]{1,2}[일.] 오\S [0-9]{1,2}:[0-9]{1,2},.*:"
    date_info = "[0-9]{4}년 [0-9]{1,2}월 [0-9]{1,2}일 \S요일"
    in_out_info = "[0-9]{4}[년.] [0-9]{1,2}[월.] [0-9]{1,2}[일.] 오\S [0-9]{1,2}:[0-9]{1,2}:.*"

    for line in open(file_path):
        if re.match(date_info, line) or re.match(in_out_info, line):
            continue
        elif line == '\n':
            continue
        elif re.match(katalk_msg_pattern, line):
            line = line.split(",")
            date_time = line[0]
            user_text = line[1].split(" : ", maxsplit=1)
            user_name = user_text[0].strip()
            text = user_text[1].strip()
            my_katalk_data.append({'Date': date_time,
                                   'User': user_name,
                                   'Message': text
                                   })

        else:
            if len(my_katalk_data) > 0:
                my_katalk_data[-1]['Message'] += "\n"+line.strip()

    my_katalk_df = pd.DataFrame(my_katalk_data)

    return my_katalk_df


def file2DataFrame(filePath : str) :
    '''
    Description : txt/csv파일을 dataFrame처리
    FilePath 형식 :
        1) " ~/fileName.txt"  --Phone 
        2) " ~/fileName.csv"  --PC
    '''
    # filePath를 보고 .csv 인지 .txt 구분
    fileForm = filePath[-3:]
    print(fileForm)
    
    # Phone Kakao의 대화내용 내보내기
    if fileForm == 'txt' :
        txtDf = katalk_msg_parse(filePath)
    
    # PC Kakao의 대화내용 내보내기
    if fileForm == 'csv' :
        print("df")
        txtDf = pd.read_csv(filePath)
        
    return txtDf


def df2Prompt(df, tokens=1000) :
    '''
    Description : DataFrame 처리된 대화내용을 받아 token자까지 처리
    '''
    result = []
    temp_conversation = df.iloc[len(df)-1]['Message']  # 마지막 대화 시작
    previous_user = df.iloc[len(df)-1]['User']  # 마지막 화자
    cur_words = ''
    temp_conversation = prep_cnt_msg(temp_conversation)
    users = []
    
    for i in range(len(df)-2, 0, -1):
        if len(cur_words) > 1000 :
            break

        current_user = df.iloc[i]['User']
        current_message = df.iloc[i]['Message']
        # current_message처리 (이모티콘, 사진*장 제거)
        current_message = prep_cnt_msg(current_message)
        if current_user == previous_user:
            # 화자가 같으면 메시지를 묶기
            temp_conversation += ' ' + current_message
        else:
            # 화자가 달라지면 이전 대화를 저장하고 새로운 대화 시작
            result.append(temp_conversation)
            temp_conversation = current_message

        # 1000자 대화중 가장 첫번째 대화를 한 사람 찾기
        previous_user = current_user
        
        # users에 다른 유저가 들어오면 추가하기
        if current_user not in users :
            users.append(current_user)

        cur_words+=current_message

    # 마지막 대화 추가
    result.append(temp_conversation)

    # 두 명의 users 뽑아내기
    if users[0] != current_user :
        another_user = users[0]
    else :
        another_user = users[1]
    return str(result[::-1])[1:-1], current_user, another_user


# 파일 경로 지정
filePath = "conversation file을 넣어주세요"

# 전처리
df = file2DataFrame(filePath)
conversation, user1, user2 = df2Prompt(df)

# chatGPT 대화 분석
result = chatAnalyze(conversation)
print(result)