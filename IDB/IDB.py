import requests
import json

# DB에 데이터 추가하는 함수. 밑에 'new_data' 있는 정보를 DB에 삽입.


"""
# 로그인시 사용되는 변수
name : String -> 
student_num : int
ex .  name 은 ID로 사용 student_num 은 비밀번호로 사용함. 
error_count : String JSON Type 규격을 따를것.
ex. {"PACKETS":88,"ERROR_COUNT":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}
위와 같은 규격으로 작성 하고 PACKETS 은 ERROR_COUNT 배열의 크기 (책의 갯수?)  ERROR_COUNT 는 각 책마다 에러 카운트 값을 저장함. array index 0 (ERROR_COUNT[0]) 은 책 1번의 오류 카운트 값을 의미함.
# 선생님의 메시지 표출  
MSG : String
MSG_TF : int
ex. MSG : 실질적인 메시지 MSG_TF : 메시지가 있는지 없는지? 이변수의 조작은 ADMIN 이 학생에게 메시지를 보낼경우 1 (TRUE) 학생이 메시지를 확인 했을경우 0 (FALSE) 로 조작함.
"""

msg = str({"PACKETS":88,"ERROR_COUNT":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]})

def insert_data(data):
    for new_data in data:
        post = {'name': new_data['name'], 'student_num': new_data['student_num'],'error_count': new_data['error_count'],'MSG': new_data['MSG'],'MSG_TF': new_data['MSG_TF']}
        response = requests.post('http://tkddn4508.dothome.co.kr/math101/insert_data_IDB.php', data=post)
    json_msg = json.loads(response.text)
    print(json_msg)


# 이름을 기준으로 DB 정보 삭제. 
def delete_data_sn(name):
    post = {'name': name}
    response = requests.post('http://tkddn4508.dothome.co.kr/math101/delete_data_sn_IDB.php', data=post)


# 수정된 fetch_data() 함수
def fetch_data():
    # DB 연결
    # 커서 가져오기 (쿼리 실행하기 위함)
    response = requests.get('http://tkddn4508.dothome.co.kr/math101/fetch_data_IDB.php')
    json_msg = json.loads(response.text)
    small_dic = {}
    if json_msg['result'] == 'success':
        rows = json_msg['row']
        for row in rows:
            name = row['name']
            student_num = row['student_num']
            error_count = row['error_count']
            MSG = row['MSG']
            MSG_TF = row['MSG_TF']
            
            # 해당 이름으로 데이터를 저장
            small_dic[name] = {
                'student_num': student_num,
                'error_count': error_count,
                'MSG': MSG,
                'MSG_TF': MSG_TF
            }
    else:
        # 연결 실패 처리
        return False
    return small_dic


# 메시지 추가하기 함수
def add_MSG(name, MSG):
    a = fetch_data()
    # 새로운 메시지를 포함한 학생 정보 업로드
    sn = a[name]['student_num']
    ec = a[name]['error_count']

    # 이름을 기준으로 해당 학생의 정보 삭제
    delete_data_sn(name)
    
   

    new_data = [
    {'name': name, 'student_num': sn, 'error_count': ec, 'MSG': MSG, 'MSG_TF': 1}
]
    

    # 데이터 추가하기    
    insert_data(new_data)

'''
# 틀린 횟수 수정하기 함수
def update_error_count(name, index, new_value):

    data = fetch_data()
    # 해당 학생의 정보가 없으면 종료
    if name not in data:
        print(f"{name} 학생의 정보가 없습니다.")
        return

    # 기존 틀린 횟수 정보를 가져오기
    error_count = data[name]['error_count']
    new_msg = error_count
    # 새로운 값을 기존 틀린 횟수에 적용
    if index >= 0 and index < len(error_count):
        error_count[index] = new_value
        # error_count[index] = new_value
 
    # 이름을 기준으로 해당 학생의 정보 삭제
    delete_data_sn(name)

    sn = data[name]['student_num']
    ec = data[name]['error_count']
    MSG = data[name]['MSG']
    MSG_TF = data[name]['MSG_TF']

    new_data = [
    {'name': name, 'student_num': sn, 'error_count': error_count, 'MSG': MSG, 'MSG_TF': MSG_TF}
]
    # 데이터 추가하기    
    insert_data(new_data)
 '''   
 # 틀린 횟수 수정하기 함수
def update_error_count(name, new_msg):

    a = fetch_data()
    # 새로운 메시지를 포함한 학생 정보 업로드
    sn = a[name]['student_num']
    MSG = a[name]['MSG']
    MSG_TF = a[name]['MSG_TF']

    # 이름을 기준으로 해당 학생의 정보 삭제
    delete_data_sn(name)
    
   

    new_data = [
    {'name': name, 'student_num': sn, 'error_count': new_msg, 'MSG': MSG, 'MSG_TF': 1}
]

    # 데이터 추가하기    
    insert_data(new_data)


# ======================== 실행 예시 ========================

new_data = [
    {'name': '임준', 'student_num': 30213, 'error_count': msg, 'MSG':' ', 'MSG_TF': 0},
    {'name': '김윤호', 'student_num': 30202, 'error_count': msg, 'MSG':' ', 'MSG_TF': 0},
    {'name': '이상우', 'student_num': 20230001, 'error_count': msg, 'MSG':' ', 'MSG_TF': 0},
]
 


# 데이터 추가하기
# insert_data(new_data)

# 학생 이름으로 삭제하기
# delete_data_sn('임준')
# delete_data_sn('이상우')
# delete_data_sn('김윤호')

# 메세지 추가하기
# add_MSG('김윤호', '수염좀 깎으세요')


# 틀린 횟수 수정하기 함수 호출
new_error_count = {"PACKETS":88,"ERROR_COUNT":[1,2,3,4,5,6,7,8,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}
update_error_count('이상우', new_error_count)

# 데이터 불러오기
# value = fetch_data()
# print(value)
