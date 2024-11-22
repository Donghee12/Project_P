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

#파이썬 코드 생성
def get_python_code_from_openai():
    try:
        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 사용할 모델
            messages=[
                {"role": "system", "content": "You are a helpful assistant Programmer."},
                {"role": "system", "content": "당신은 사용자가 다양한 Python Code를 경험할 수 있게 도와주는 문제 생성 프로그램입니다."},
                {"role": "user", "content": "문제 생성 시 반드시 순수한 코드만 작성하고, 주석이나 설명 텍스트는 포함하지 말 것"},
                {"role": "user", "content": "반드시 ```python과 같은 구분자를 포함하지 말고 순수한 코드만 반환할 것"},
                {"role": "user", "content": "Python 문제 1개를 생성하세요. 다음 주제 중 하나를 포함해야 합니다:"},
                {"role": "user", "content": (
                    "1. 데이터 구조 (리스트, 딕셔너리, 셋)\n"
                    "2. 문자열 처리 (문자열 조작, 정규 표현식)\n"
                    "3. 알고리즘 문제 (탐색, 정렬, 그래프)\n"
                    "4. 수학적 계산 (소수, 확률, 통계)\n"
                    "5. 클래스와 객체지향 프로그래밍 (상속, 다형성)"
                    )}
            ]
        )
        
        # 응답 디버깅
        print("Full OpenAI Response:", response)

        # 코드 추출
        code = response.choices[0].message.content.strip()
        print("Generated Python Code:\n", code)
        return code
    except Exception as e:
        print(f"Error generating Python code: {str(e)}")
        raise



#Jdoodle 파이썬 코드 컴파일
def execute_python_code_with_jdoodle(code):
    try:
        # JDoodle API 호출용 페이로드
        payload = {
            "clientId": jdoodle_client_id,
            "clientSecret": jdoodle_client_secret,
            "script": code,
            "language": "python3",  # Python 언어 설정
            "versionIndex": "3",  # JDoodle Python 버전
        }

        # JDoodle API 호출
        response = requests.post(jdoodle_url, json=payload)

        # 응답 상태 코드 확인
        if response.status_code == 200:
            result = response.json()
            output = result.get("output", "No output")

            # 오류 또는 예외가 감지되었는지 확인
            if "error" in output.lower() or "exception" in output.lower():
                print("Compilation Error Detected:", output)

                # OpenAI에 오류 메시지와 원본 코드 전달
                fixed_code = request_python_code_fix_from_openai(code, output)

                print("Fixed Code Generated by OpenAI:\n", fixed_code)

                # 수정된 코드로 다시 재귀 호출
                return execute_python_code_with_jdoodle(fixed_code)
            else:
                # 정상 출력 반환
                return {
                    "output": output,
                    "cpu_time": result.get("cpuTime"),
                    "memory": result.get("memory"),
                }
        else:
            # JDoodle API 오류 반환
            return {"error": f"JDoodle API Error: {response.status_code} - {response.text}"}
    except Exception as e:
        # 예외 발생 시 에러 반환
        return {"error": f"Exception occurred: {str(e)}"}
    

#파이썬 코드 수정 요청
def request_python_code_fix_from_openai(original_code, error_message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 사용할 모델
            messages=[
                {"role": "system", "content": "You are a helpful assistant Programmer."},
                {"role": "user", "content": "아래 Python 코드에서 실행 중 오류가 발생했습니다. 오류 메시지와 원본 코드를 참고하여 수정된 코드를 작성해 주세요."},
                {"role": "user", "content": f"오류 메시지:\n{error_message}"},
                {"role": "user", "content": f"원본 코드:\n{original_code}"},
                {"role": "user", "content": "수정된 코드만 순수한 형태로 반환하세요. 주석이나 추가 설명은 포함하지 말 것."},
                {"role": "user", "content": "```python와 같은 구분자도 포함하지 말고 코드만 반환할 것."}
            ]
        )
        fixed_code = response.choices[0].message.content.strip()
        print("Fixed Python Code:\n", fixed_code)
        return fixed_code
    except Exception as e:
        print(f"Error fixing Python code: {str(e)}")
        raise

 #파이썬 코드 해설 요청
def get_python_code_explanation(code):
    try:
        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 사용할 모델
            messages=[
                {"role": "system", "content": "You are a helpful assistant Programmer."},
                {"role": "system", "content": "당신은 사용자가 이해하지 못하는 Python 코드를 이해시키도록 도와주는 프로그래밍 선생님입니다."},
                {"role": "user", "content": "다음 Python 코드를 해설해 주세요."},
                {"role": "user", "content": code},
                {"role": "user", "content": "선생님처럼 설명해주세요"},
                {"role": "user", "content": "시작을 알리는 문장 없이 바로 해설 해주세요"}
            ]
        )

        # 응답 디버깅
        print("Full OpenAI Response:", response)

        # 코드 해설 추출
        explanation = response.choices[0].message.content.strip()
        print("Generated Python Code Explanation:\n", explanation)
        return explanation
    except Exception as e:
        print(f"Error explaining Python code: {str(e)}")
        return {"error": f"Exception occurred: {str(e)}"}
