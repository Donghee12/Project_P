from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from openai import OpenAI
import os
import requests


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
    print("OpenAI 응답 받음.")
    code = response.choices[0].message.content
    
     # 코드에 public class가 없으면 추가
    if "public class" not in code:
        code = "public class Main {\n" + code + "\n}"

    return code

#코드에 대한 해설 요청
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
    
        # 응답 구조 디버깅
        print("Full OpenAI Response:", response)

        # 응답에서 설명 추출
        explanation = response['choices'][0]['message']['content']
        

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
    
    print(f"JDoodle response status: {response.status_code}")  # 응답 상태 코드 확인
    print(f"JDoodle response text: {response.text}")  # 응답 내용 확인

    # 응답 상태 코드가 200이 아닌 경우
    if response.status_code != 200:
        return {"error": f"JDoodle Error: {response.status_code} - {response.text}"}

    result = response.json()
    if "output" in result:
        return {"output": result["output"]}
    else:
        return {"error": "No output from JDoodle"}


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
            {"role": "user", "content": "반드시 주석을 포함하지 말 것"},
            # 여기서 오류 메시지를 한글로 설명해달라고 추가
            {"role": "user", "content": "위의 오류 메시지에 대해 한글로 설명해 주세요. 오류가 발생한 이유를 상세히 설명해 주세요."}
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
    
# Java 코드 실행 API - JDoodle 연동
@app.route('/execute_code', methods=['POST'])
def execute_code():
    code = request.json.get('code')
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    
    try:
        # JDoodle API를 통해 코드 실행
        output = execute_java_code_with_jdoodle(code)

        # JDoodle에서 오류가 발생하면
        if "error" in output and output["error"] is not None:
            error_message = output["error"]
            # 오류 메시지를 OpenAI에 전달하여 코드 수정 요청
            fixed_code = request_code_fix_from_openai(code, error_message)
            return jsonify({'output': f"Code fixed:\n{fixed_code}"})
        
        # 정상적으로 출력이 발생하면, 그 값을 JSON으로 반환
        return jsonify({'output': output['output']})

    except Exception as e:
        # 예외 발생 시 에러 메시지 반환
        return jsonify({'output': f"Error: {str(e)}"}), 500

#Java 코드에 대한 해설 API
@app.route('/generate_explanation', methods=['POST'])
def generate_explanation():
    try:
        data = request.get_json()  # 클라이언트에서 보낸 JSON 데이터

        code = data.get("code")  # 코드 받기
        if not code:
            raise ValueError("No code provided.")  # 코드가 없으면 오류 발생

        # OpenAI에서 설명 생성 요청
        response = get_code_explanation(code)

        # 응답 전체 내용 확인
        print("Full OpenAI response:", response)  # 전체 응답 출력

        # 응답이 어떤 형식인지 확인
        if isinstance(response, dict):
            # 응답 형식 로깅
            print("Response type:", type(response))  
            print("Response content:", response)  # 응답을 출력하여 구조 확인

        explanation = response['choices'][0]['message']['content']

        return jsonify({"explanation": explanation})

    except Exception as e:
        print(f"Error: {str(e)}")  # 오류 로그 출력
        return jsonify({"error": str(e)}), 500  # 오류 발생시 500 상태코드와 함께 에러 메시지 반환


if __name__ == "__main__":
    app.run(debug=True)