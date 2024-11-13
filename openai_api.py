from dotenv import load_dotenv
import os
import requests

# .env 파일을 로드
load_dotenv()

# 환경 변수 가져오기
api_key_ = os.getenv("API_KEY")
from openai import OpenAI
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
jdoodle_url_env = os.getenv("jdoodle_url_env")
# API 키 설정
client = OpenAI(api_key=api_key_)
jdoodle_client_id = client_id
jdoodle_client_secret = client_secret
jdoodle_url = jdoodle_url_env

# API 요청을 위한 메시지 구성
def get_java_code_from_openai():
    response = client.chat.completions.create(
    model="gpt-4o-mini",  # 사용할 모델
    messages=[
        {"role": "system", "content": "You are a helpful assistant Programmer."},
        {"role": "user", "content": "당신은 숙련된 프로그래머입니다. 당신의 목표는 사용자 요청에 맞춰 Java코드를 작성하는 것입니다."},
        {"role": "user", "content": "반드시 텍스트도 없고 주석도 없는 순수한 코드만으로 응답할 것."},
       ## {"role": "user", "content": "Java는 클래스, 추상 클래스와 형 변환, 상속, 예외처리에 관한 내용을 담을 것."},
        ##{"role": "user", "content": "각 문제는 개별적으로 실습할 수 있도록 구성할 것"},
        {"role": "user", "content": "초급 수준의 간단한 코드로 작성할 것"},
    ]
)
    code = response.choices[0].message.content
    cleaned_code = code.replace("```java", "").replace("```", "")
    print("Generated Java Code:\n", cleaned_code)
    return cleaned_code

def execute_java_code_with_jdoodle(code):
    # JDoodle API 요청을 위한 설정
    payload = {
        "clientId": jdoodle_client_id,
        "clientSecret": jdoodle_client_secret,
        "script": code,
        "language": "java",       # Java로 설정
        "versionIndex": "0"       # JDoodle에서 Java 버전 인덱스 (보통 "0" 사용)
    }

    # JDoodle API로 코드 실행 요청
    response = requests.post(jdoodle_url, json=payload)
    
    # 결과 처리
    if response.status_code == 200:
        result = response.json()
        print("Output:", result.get("output", "No output"))
        print("CPU Time:", result.get("cpuTime"))
        print("Memory:", result.get("memory"))
    else:
        print("Error:", response.status_code, response.text)

# 1. OpenAI로부터 Java 코드 생성
generated_java_code = get_java_code_from_openai()

# 2. JDoodle API를 통해 Java 코드 실행
execute_java_code_with_jdoodle(generated_java_code)