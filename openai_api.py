from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from openai import OpenAI
import os
import requests
import subprocess
import re


# .env 파일을 로드
load_dotenv()

# 환경 변수 가져오기
api_key_ = os.getenv("API_KEY")
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
jdoodle_url_env = os.getenv("jdoodle_url_env")

# API 키 설정
client = OpenAI(api_key=api_key_)
jdoodle_client_id = client_id
jdoodle_client_secret = client_secret
jdoodle_url = jdoodle_url_env

# Flask 애플리케이션 초기화
app = Flask(__name__)
CORS(app)  # CORS 설정 추가

# API 요청을 위한 메시지 구성
def get_java_code_from_openai():
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 사용할 모델
        messages=[
            {"role": "system", "content": "You are a helpful assistant Programmer."},
            {"role": "user", "content": "숙련된 프로그래머로서 Java 중급 수준의 코드를 작성할 것."},
            {"role": "user", "content": "반드시 순수한 코드만 작성하고, 절대 주석이나 설명 텍스트는 포함하지 말 것."},
            {"role": "user", "content": "라이브러리와 API를 사용하지 않는 코드일 것."},
            {"role": "user", "content": "```java와 같은 구분자도 포함하지 말고 코드만 반환할 것."},
        ]
    )
    code = response.choices[0].message.content
    
     # 코드에 public class가 없으면 추가
    if "public class" not in code:
        code = "public class Main {\n" + code + "\n}"

    return code

def get_code_explanation(code):
    explanation = ""  # 설명 초기화  

    try:
        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 사용할 모델
            messages=[
                {"role": "system", "content": "You are a helpful assistant Programmer."},
                {"role": "user", "content": "아래 Java 코드에 대한 상세한 설명을 작성해 주세요."},
                {"role": "user", "content": f"코드:\n{code}"}
            ]
        )

        # 응답 구조 전체 출력
        print("Full OpenAI Response: ", response)

        # choices가 있는지 확인
        if 'choices' in response and len(response['choices']) > 0:
            choice = response['choices'][0]
            explanation = choice.get('message', {}).get('content', "No explanation content available")
            print("Explanation Found: ", explanation)
        else:
            # choices가 없으면 error 필드 확인
            if 'error' in response:
                explanation = f"Error: {response['error'].get('message', 'Unknown error occurred')}"
            else:
                explanation = "No choices found in the response."

    except Exception as e:
        explanation = f"Error: {str(e)}"

    return explanation





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
            # OpenAI에 오류 메시지와 함께 코드 수정 요청
            fixed_code = request_code_fix_from_openai(code, output)
            # 수정된 코드를 다시 JDoodle로 전송하여 실행 결과 확인
            execute_java_code_with_jdoodle(fixed_code)
        else:
            return output
    else:
        return f"Error: {response.status_code} - {response.text}"

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
    fixed_code = response.choices[0].message.content.strip()
    return fixed_code

# 홈 페이지로 index.html 렌더링
@app.route('/')
def index():
    return render_template('index.html')

# Java 코드 생성 API
@app.route('/generate_code', methods=['POST'])
def generate_code():
    try:
        code = get_java_code_from_openai()
        return jsonify({"code": code})
    except Exception as e:
        return jsonify({"error": str(e)})
    
# Java 코드 실행 API
@app.route('/execute_code', methods=['POST'])
def execute_code():
    try:
        # 요청에서 데이터 받기
        data = request.get_json()
        if not data or 'code' not in data:
            return jsonify({'error': 'No code provided'}), 400
        
        code = data['code']
        # public class 이름 추출
        match = re.search(r'public class (\w+)', code)
        if not match:
            return jsonify({'error': 'No public class found'}), 400
        class_name = match.group(1)

        # 코드 저장
        file_name = f"{class_name}.java"
        with open(file_name, 'w') as f:
            f.write(code)

        # Java 코드 컴파일
        compile_result = subprocess.run(['javac', file_name], capture_output=True, text=True)
        if compile_result.returncode != 0:
            return jsonify({'error': 'Compilation failed', 'details': compile_result.stderr}), 400

        # 실행
        run_result = subprocess.run(['java', class_name], capture_output=True, text=True)
        if run_result.returncode != 0:
            return jsonify({'error': 'Execution failed', 'details': run_result.stderr}), 400

        return jsonify({'output': run_result.stdout})

    except Exception as e:
        return jsonify({'error': f'Error executing code: {str(e)}'}), 500

#Java 코드에 대한 해설 API
# 해설 생성 API
@app.route('/generate_explanation', methods=['POST'])
def generate_explanation():
    try:
        data = request.get_json()  # 클라이언트에서 보낸 JSON 데이터
        print("Received data:", data)  # 데이터 확인

        code = data.get("code")  # 코드 받기
        if not code:
            raise ValueError("No code provided.")  # 코드가 없으면 오류 발생

        # OpenAI에서 설명 생성 요청
        explanation = get_code_explanation(code)
        print("Generated explanation:", explanation)  # 생성된 해설 확인
        return jsonify({"explanation": explanation})

    except Exception as e:
        print(f"Error: {str(e)}")  # 오류 로그 출력
        return jsonify({"error": str(e)}), 500  # 오류 발생시 500 상태코드와 함께 에러 메시지 반환


if __name__ == "__main__":
    app.run(debug=True)