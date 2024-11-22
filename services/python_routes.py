from flask import Blueprint, jsonify, request
from services.python_handler import *

python_routes = Blueprint('python_routes', __name__)


# 파이썬 코드 생성 엔드포인트
@python_routes.route('/generate_python_code', methods=['POST'])
def generate_python_code():
    try:
        code = get_python_code_from_openai()
        return jsonify({"code": code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#파이썬 코드 실행 엔드포인트
@python_routes.route('/execute_python_code', methods=['POST'])
def execute_python_code():
    code = request.json.get('code')  # 클라이언트로부터 코드 입력 받기
    if not code:
        return jsonify({'error': 'No code provided'}), 400

    try:
        # 수정된 함수로 Python 코드 실행 (컴파일 에러가 있으면 재귀적으로 수정)
        output = execute_python_code_with_jdoodle(code)

        # 최종 결과를 반환
        return jsonify(output)

    except Exception as e:
        # 예외 발생 시 에러 메시지 반환
        python_routes.logger.exception("Error executing Python code")
        return jsonify({'error': f"Error: {str(e)}"}), 500


#파이썬 코드 해설 엔드포인트
@python_routes.route('/generate_python_explanation', methods=['POST'])
def generate_python_explanation():
    try:
        data = request.get_json()  # 클라이언트로부터 요청 데이터 받기
        code = data.get("code")
        if not code:
            return jsonify({"error": "No code provided"}), 400

        # OpenAI API를 통해 해설 생성
        response_python = get_python_code_explanation(code)
        explanation_python = response_python

        return jsonify({"explanation": explanation_python})
    except Exception as e:
        return jsonify({"error": str(e)}), 500