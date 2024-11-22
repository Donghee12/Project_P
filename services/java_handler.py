from flask import jsonify
from openai import OpenAI
from dotenv import load_dotenv
import requests
import os

# .env 파일 로드
load_dotenv()

# API 키 설정
client = OpenAI(api_key= os.getenv("API_KEY"))
jdoodle_client_id = os.getenv("client_id")
jdoodle_client_secret = os.getenv("client_secret")
jdoodle_url = os.getenv("jdoodle_url_env")

#자바코드 생성
def get_java_code_from_openai():
    try:
        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 사용할 모델
            messages=[
                {"role": "system", "content": "You are a helpful assistant Programmer."},
                {"role": "user", "content": "의도적으로 컴파일 에러를 일으키는 간단한 Java 코드를 작성할 것"},
                {"role": "user", "content": "출력이 가능한 프로그램일 것"},
                {"role": "user", "content": "너의 응답으로 온 코드를 바로 컴파일 할 수 있어야 할 것"},
                {"role": "user", "content": "반드시 순수한 코드만 작성하고, 절대 주석이나 설명 텍스트는 포함하지 말 것."},
                {"role": "user", "content": "라이브러리와 API를 사용하지 않는 코드일 것."},
                {"role": "user", "content": "```java와 같은 구분자도 포함하지 말고 코드만 반환할 것."}
            ]
        )

        # 응답 디버깅
        print("Full OpenAI Response:", response)

        # 코드 추출
        code = response.choices[0].message.content.strip()
        print("Generated Java Code:\n", code)
        return code
    except Exception as e:
        print(f"Error generating Java code: {str(e)}")
        raise

# Jdoodle 자바코드 컴파일
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

        # 오류 감지
        if "error" in output.lower() or "exception" in output.lower():
            print("Compilation Error Detected:", output)

            # OpenAI에 오류 메시지와 원본 코드 전달
            fixed_code = request_code_fix_from_openai(code, output)

            print("Fixed Code Generated by OpenAI:\n", fixed_code)

            # 수정된 코드로 다시 재귀 호출
            return execute_java_code_with_jdoodle(fixed_code)
        else:
            # 정상 출력 반환
            return {
                "output": output,
                "cpu_time": result.get("cpuTime"),
                "memory": result.get("memory")
            }
    else:
        # JDoodle API 오류 처리
        return {"error": f"JDoodle API Error: {response.status_code} - {response.text}"}

#자바 코드 수정 요청
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
            {"role": "user", "content": "반드시 주석을 포함하지 말 것"},
        ]
    )
    fixed_code = response.choices[0].message.content.strip()
    return fixed_code

#자바코드에 대한 해설 요청
def get_code_explanation(code):
    try:
        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant Programmer."},
                {"role": "user", "content": "아래 Java 코드에 대한 설명을 최대한 간결히 작성할 것."},
                {"role": "user", "content": "한국어로 3줄 이상 넘어가지 말 것"},
                {"role": "user", "content": f"코드:\n{code}"}
            ]
        )

        # 디버깅: 응답 객체의 타입과 내용 확인
        print("Response Type:", type(response))
        print("Full Response:", response)

        # 응답 구조에서 설명 추출
        explanation = response.choices[0].message.content

        # 디버깅: 추출된 설명 확인
        print("Extracted Explanation:", explanation)
        return explanation

    except Exception as e:
        print(f"Error generating explanation: {e}")
        return f"Error generating explanation: {e}"

 