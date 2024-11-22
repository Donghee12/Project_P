from flask import Blueprint, jsonify, request
from services.java_handler import *
import requests

java_routes = Blueprint('java_routes', __name__)


# Java 코드 생성 엔드포인트
@java_routes.route('/generate_code', methods=['POST'])
def generate_code():
    print("Request received at /java_routes/generate_code")  # 로그로 요청 확인
    try:
        code = get_java_code_from_openai()
        return jsonify({"code": code})
    except Exception as e:
        return jsonify({"error": str(e)})
    


#자바 코드 실행 엔드포인트
@java_routes.route('/execute_code', methods=['POST'])
def execute_code():
    code = request.json.get('code')  # 클라이언트로부터 코드 입력 받기
    if not code:
        return jsonify({'error': 'No code provided'}), 400

    try:
        # 수정된 함수로 코드 실행 (컴파일 에러가 있으면 재귀적으로 수정)
        output = execute_java_code_with_jdoodle(code)

        # 최종 결과를 반환
        return jsonify(output)

    except Exception as e:
        # 예외 발생 시 에러 메시지 반환
        java_routes.logger.exception("Error executing Java code")
        return jsonify({'error': f"Error: {str(e)}"}), 500
    
#Java 코드에 대한 해설 API
@java_routes.route('/generate_explanation', methods=['POST'])
def generate_explanation():
    try:
        data = request.get_json()  # 클라이언트에서 보낸 JSON 데이터

        code = data.get("code")  # 코드 받기
        if not code:
            raise ValueError("No code provided.")  # 코드가 없으면 오류 발생

        # OpenAI에서 설명 생성 요청
        response = get_code_explanation(code)


        # 응답이 어떤 형식인지 확인
        if isinstance(response, dict):
            # 응답 형식 로깅
            print("Response type:", type(response))  
            print("Response content:", response)  # 응답을 출력하여 구조 확인

        explanation = response

        return jsonify({"explanation": explanation})

    except Exception as e:
        print(f"Error: {str(e)}")  # 오류 로그 출력
        return jsonify({"error": str(e)}), 500  # 오류 발생시 500 상태코드와 함께 에러 메시지 반환
