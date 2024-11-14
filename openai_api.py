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
        {"role": "user", "content": "숙련된 프로그래머로서 Java 중급 수준의 코드를 작성할 것."},
        {"role": "user", "content": "반드시 순수한 코드만 작성하고, 절대 주석이나 설명 텍스트는 포함하지 말 것."},
        {"role": "user", "content": "라이브러리와 API를 사용하지 않는 코드일 것."},
        {"role": "user", "content": "```java와 같은 구분자도 포함하지 말고 코드만 반환할 것."}
        ## {"role": "user", "content": "Java는 클래스, 추상 클래스와 형 변환, 상속, 예외처리에 관한 내용을 담을 것."},
        ##{"role": "user", "content": "각 문제는 개별적으로 실습할 수 있도록 구성할 것"},
    ]
)
    code = response.choices[0].message.content
    print("Generated Java Code:\n", code)
    return code

# JDoodle API 요청을 위한 설정
def execute_java_code_with_jdoodle(code):
    payload = {
        "clientId": jdoodle_client_id,
        "clientSecret": jdoodle_client_secret,
        "script": code,
        "language": "java",
        "versionIndex": "0"
    }

    # JDoodle API로 코드 실행 요청
    response = requests.post(jdoodle_url, json=payload)
    
    # 결과 처리
    if response.status_code == 200:
        result = response.json()
        output = result.get("output", "No output")
        
        # 오류가 포함된 경우 감지하여 수정 요청
        if "error" in output.lower() or "exception" in output.lower():
            print("Compilation Error:", output)
            # OpenAI에 오류 메시지와 함께 코드 수정 요청
            fixed_code = request_code_fix_from_openai(code, output)
            print("Fixed Code:\n", fixed_code)
            # 수정된 코드를 다시 JDoodle로 전송하여 실행 결과 확인
            execute_java_code_with_jdoodle(fixed_code)
        else:
            print("Output:", output)
            print("CPU Time:", result.get("cpuTime"))
            print("Memory:", result.get("memory"))
    else:
        print("Error:", response.status_code, response.text)

# OpenAI에 컴파일 오류 수정 요청
def request_code_fix_from_openai(original_code, error_message):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant Programmer."},
            {"role": "user", "content": "아래 Java 코드에서 컴파일 오류가 발생했습니다. 오류 메시지와 코드를 참고하여 오류를 수정해 주세요."},
            {"role": "user", "content": f"오류 메시지:\n{error_message}"},
            {"role": "user", "content": f"원본 코드:\n{original_code}"},
            {"role": "user", "content": "수정된 코드만 순수한 형태로 응답해 주세요."},
            {"role": "user", "content": "```java와 같은 구분자도 포함하지 말고 코드만 반환할 것."},
            {"role": "user", "content": "반드시 주석을 포함하지 말 것"}
        ]
    )
    # 수정된 코드 반환
    fixed_code = response.choices[0].message.content.strip()
    return fixed_code

# 컴파일 오류가 있는 Java 코드 설정
def get_error_java_code():
    # 컴파일 오류가 발생하도록 의도한 코드
    error_code = """
    public class Main {
        public static void main(String[] args) {
            int number = 10;
            int a = number / 0;
            System.out.println(a);
        }
    }
    """
    print("Test Java Code with Compilation Error:\n", error_code)
    return error_code

# 1. OpenAI로부터 Java 코드 생성
##generated_java_code = get_java_code_from_openai()

# 2. JDoodle API를 통해 Java 코드 실행 및 오류 처리
##execute_java_code_with_jdoodle(generated_java_code)

# 1. 오류가 있는 Java 코드 가져오기
error_java_code = get_error_java_code()

# 2. JDoodle API를 통해 Java 코드 실행 및 오류 처리
execute_java_code_with_jdoodle(error_java_code)