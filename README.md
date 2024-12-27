# Java, Python 코드 생성기 및 실행기

이 웹 애플리케이션은 사용자가 Java, Python 코드를 생성하고 실행하며 디버깅할 수 있도록 도와주는 Flask 기반의 프로젝트입니다. OpenAI GPT를 활용하여 코드 오류를 수정하고, 코드에 대한 설명을 제공합니다.

---

## 📌 목차

- [기술스택](#기술스택)
- [기능](#기능)
- [설치](#설치)
- [사용법](#사용법)
- [API 엔드포인트](#api-엔드포인트)
- [프론트엔드 기능](#프론트엔드-기능)
- [보안 고려 사항](#보안-고려-사항)
- [클라우드](#클라우드)
---
## 📑기술스택
이 프로젝트에서 사용된 주요 기술 스택을 나열합니다:

  프로그래밍 언어: Python, Java
  웹 프레임워크: Flask
  API: OpenAI GPT, JDoodle API
  버전 관리: Git, GitHub
  클라우드 서비스: Pythonanywhere
---

## 💡기능

- **코드 생성**: OpenAI GPT를 사용하여 자동으로 Java 코드를 생성합니다.
- **코드 실행**: JDoodle API를 통해 생성된 Java 코드를 실행하고 결과를 출력합니다.
- **코드 디버깅**: 코드 실행 중 발생하는 오류를 OpenAI GPT를 통해 수정하고, 수정된 코드와 결과를 출력합니다.
- **코드 설명**: 생성된 Java, Python 코드에 대한 설명을 OpenAI GPT로 제공받습니다.

---

## 🛠️ 설치

### 필수 사항

- Python 3.7 이상
- Flask
- OpenAI API 키
- JDoodle API 자격 증명

### 1. 리포지토리 클론

```bash
git clone https://github.com/Donghee12/Project_P.git
cd java-code-executor


```

### 2. 의존성 설치

```bash
python3 -m venv venv
source venv/bin/activate  # Windows의 경우 `venv\Scripts\activate` 명령 사용
pip install -r requirements.txt
```

### 3. 환경 변수 설정
```bash
OPENAI_API_KEY=your-openai-api-key
JDoodle_CLIENT_ID=your-jdoodle-client-id
JDoodle_CLIENT_SECRET=your-jdoodle-client-secret
```

###  Flask 애플리케이션 실행

```bash
python main.py
```

---
## 🚀 사용법

### 1. 메인 페이지
메인 페이지에서 Get Started Now 버튼을 클릭하여 서비스 시작 페이지로 이동합니다.
이 페이지에서는 Java와 Python 언어를 선택할 수 있습니다.

### 2. 언어 선택 페이지
language_select.html에서 Java나 Python을 선택하여 각 언어에 대한 코드 생성 및 실행 기능을 시작할 수 있습니다.

### 3. Java 및 Python 코드 생성 및 실행 페이지
**java_page.html**에서 Generate Java Code 버튼을 클릭하여 Java 코드를 자동 생성합니다.
생성된 Java 및 Python 코드는 화면에 표시됩니다.
Execute Code 버튼을 클릭하여 생성된 코드를 실행하고 결과를 확인할 수 있습니다.
Generate Explanation 버튼을 클릭하여 생성된 코드에 대한 설명을 받을 수 있습니다.

### 4. 실행 예시
Java 및 Python 코드 생성: Generate Java Code 버튼을 클릭하면 Java 및 Python 코드가 자동으로 생성됩니다.
코드 실행: 생성된 코드를 Execute Code 버튼을 통해 실행하여 결과를 확인합니다.
코드 설명: Generate Explanation 버튼을 클릭하여 코드의 기능과 동작에 대해 설명을 받을 수 있습니다.

---

##  API 엔드포인트

/generate_code
Method: POST
설명: OpenAI GPT를 사용하여 Java 및 Python 코드를 생성합니다.
요청 본문: 빈 요청 본문으로 코드를 생성합니다.

응답 예시:
```json
{
  "code": "public class Main { ... }"
}
```

/execute_code
Method: POST
설명: JDoodle API를 사용하여 Java 및 Python 코드를 실행합니다.
요청 본문 :
```json
{
  "code": "public class Main { ... }"
}
```
응답 예시 :
```json
{
  "output": "Hello, World!"
}
```
/generate_explanation
Method: POST
설명: 생성된 Java 및 Python 코드에 대한 설명을 제공합니다.
요청 본문:
```json
{
  "code": "public class Main { ... }"
}
```
응답 예시:
```json
{
  "explanation": "이 코드는 콘솔에 'Hello, World!'를 출력합니다."
}
```

---

## 🌍프론트엔드 기능

이 애플리케이션은 사용자가 생성된 코드를 실행하고 수정하는 등 여러 기능을 웹 페이지에서 직접 사용할 수 있도록 합니다. 주요 JavaScript 함수는 다음과 같습니다:

1. generateCode()
목적: /generate_code 엔드포인트로 Java 코드 생성을 요청합니다.
동작 방식:
빈 POST 요청을 서버로 보냅니다.
서버에서 OpenAI GPT를 통해 Java 코드를 생성하고, 생성된 코드를 클라이언트로 반환합니다.
반환된 코드를 웹 페이지에 표시합니다.

2. executeCode()
목적: 생성된 Java 코드를 실행하여 실행 결과를 화면에 출력합니다.
동작 방식:
페이지에서 생성된 코드를 가져옵니다.
/execute_code 엔드포인트에 POST 요청을 보내어 JDoodle API를 사용해 코드를 실행합니다.
만약 코드가 정상적으로 실행이 되지 않는경우에는 코드를 실행이 가능하도록 수정하는 코드로 넘어갑니다.
자바인 경우 java_handler.py에서 execute_java_code_with_jdoodle의 함수를 불러온 후  원본 코드와 오류 메시지를
OpenAI에 전달을 합니다(java_handler.py에서 request_code_fix_from_openai를 실행) (Python은 함수이름만 다를뿐 동작원리는 같습니다)
이후 실행 결과를 페이지에 표시합니다.

3. generateExplanation()
목적: 생성된 코드에 대한 설명을 제공합니다.
동작 방식:
페이지에서 생성된 코드를 가져옵니다.
/generate_explanation 엔드포인트에 POST 요청을 보내어 OpenAI GPT가 생성된 코드에 대해 설명을 제공합니다.
설명을 페이지의 출력 영역에 표시합니다.

---

## 🔒보안 고려 사항

 ### OpenAI API키와 JDoodele API 키 관리법
 #### 1.python에 .env파일을 생성
 .env파일을 생성하여 아래와 같이 변수를 저장합니다.
 ```plaintext
 OPENAI_API_KEY=your-openai-api-key
 JDoodle_CLIENT_ID=your-jdoodle-client-id
 JDoodle_CLIENT_SECRET=your-jdoodle-client-secret
 ```

 #### 2. .gitignore에 추가
 .env 파일에 민감한 정보가 포함되어 있기 때문에 Git에 커밋하지 않도록
 .gitignore 파일에 .env를 추가합니다. .gitignore 파일에 아래와 같이 추가합니다:
 ```plaintext
 # .env 파일을 Git에 커밋하지 않기 위해 추가
.env
 ```

 #### 3. python-dotenv 라이브러리 설치
 Flask 애플리케이션에서 .env 파일을 로드하려면 python-dotenv 라이브러리를 사용할 수 있습니다.
 이 라이브러리는 .env 파일의 내용을 자동으로 로드하고 환경 변수로 설정해줍니다.
 ```plaintext
pip install python-dotenv
 ```

 #### 4. 보안 고려사항
.env 파일에는 민감한 정보를 저장하므로, 이를 공유하지 않도록 주의해야 합니다.
GitHub에 배포하거나 클라우드 서비스를 사용할 때, .env 파일의 정보는 보안적으로 안전한 방법으로 저장해야 합니다 (예: 환경 변수 관리 서비스 이용).
이러한 방법으로 .env 파일을 사용하면 코드에 민감한 정보를 안전하게 관리할 수 있습니다.

---

## 🌐클라우드

이 프로젝트는 **PythonAnywhere** 클라우드 호스팅 서비스를 사용하여 배포되었습니다. PythonAnywhere는 Python 웹 애플리케이션을 쉽게 호스팅할 수 있는 플랫폼으로, 웹 서버와 데이터베이스 설정 없이도 간단하게 클라우드 환경에서 애플리케이션을 실행할 수 있게 도와줍니다.

### PythonAnywhere를 사용한 배포

1. **계정 생성 및 로그인**: PythonAnywhere 계정을 생성한 후 로그인하여 대시보드에 접근합니다.
2. **애플리케이션 설정**: `Flask` 웹 애플리케이션을 설정하기 위해, 대시보드에서 웹 탭을 선택한 후 새 웹 앱을 생성합니다. 생성 시 Python 버전과 Flask를 선택하고, 애플리케이션의 코드 파일 위치를 지정합니다.
3. **코드 배포**: 로컬에서 작성한 코드를 PythonAnywhere의 파일 관리자를 통해 업로드하거나 GitHub에서 직접 클론하여 서버에 배포할 수 있습니다.
4. **환경 변수 설정**: PythonAnywhere 대시보드의 "Web" 탭에서 환경 변수를 설정하여 OpenAI API 키와 JDoodle API 자격 증명 등 필요한 민감 정보를 안전하게 관리합니다.
5. **애플리케이션 실행**: 배포가 완료되면, PythonAnywhere에서 제공하는 URL을 통해 애플리케이션을 접속할 수 있습니다. 클라우드에서 실행되는 Flask 애플리케이션을 통해 코드 생성, 실행 및 디버깅을 실시간으로 테스트할 수 있습니다.

PythonAnywhere를 통해 이 애플리케이션을 클라우드에서 손쉽게 운영할 수 있으며, 안정적이고 확장 가능한 방식으로 사용자에게 서비스를 제공할 수 있습니다.

