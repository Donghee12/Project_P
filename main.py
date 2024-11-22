from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from services.java_handler import *
from services.python_handler import *
from services.java_routes import *
from services.python_routes import *
import sys
import os
# 현재 스크립트의 경로를 기준으로 상위 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # 상위 디렉토리

# 'services' 폴더 경로
services_dir = os.path.join(parent_dir, "services")

# 'services' 폴더를 Python 경로에 추가
sys.path.append(services_dir)

# .env 파일 로드
load_dotenv()

# Flask 애플리케이션 초기화
app = Flask(__name__)
CORS(app)

# Blueprint 등록
app.register_blueprint(java_routes, url_prefix='/java_routes')

app.register_blueprint(python_routes, url_prefix='/python_routes')


# 홈 페이지
@app.route('/')
def index():
    return render_template('index.html')

# 언어 선택 페이지
@app.route('/language')
def language_page():
    return render_template('language_select.html')

# Java 관련 엔드포인트
@app.route('/java')
def java_page():
    return render_template('java_page.html')

#파이썬 페이지
@app.route("/python")
def python_page():
    return render_template("python_page.html")  # Python 관련 HTM






if __name__ == "__main__":
    app.run(debug=True)
