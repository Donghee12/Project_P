# Java 코드 생성기 및 실행기

이 웹 애플리케이션은 사용자가 Java 코드를 생성하고 실행하며 디버깅할 수 있도록 도와주는 Flask 기반의 프로젝트입니다. OpenAI GPT를 활용하여 코드 오류를 수정하고, 코드에 대한 설명을 제공합니다.

## 목차

- [기능](#기능)
- [설치](#설치)
- [사용법](#사용법)
- [API 엔드포인트](#api-엔드포인트)
- [프론트엔드 기능](#프론트엔드-기능)
- [라이센스](#라이센스)

---

## 기능

- **코드 생성**: OpenAI GPT를 사용하여 자동으로 Java 코드를 생성합니다.
- **코드 실행**: JDoodle API를 통해 생성된 Java 코드를 실행하고 결과를 출력합니다.
- **코드 디버깅**: 코드 실행 중 발생하는 오류를 OpenAI GPT를 통해 수정하고, 수정된 코드와 결과를 출력합니다.
- **코드 설명**: 생성된 Java 코드에 대한 설명을 OpenAI GPT로 제공받습니다.

---

## 설치

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
python openai_api.py
```

---
## 사용법

### 1. 메인 페이지
Welcome to Our Service 페이지에서 Get Started Now 버튼을 클릭하여 서비스 시작 페이지로 이동합니다.
이 페이지에서는 Java와 Python 언어를 선택할 수 있습니다.

### 2. 언어 선택 페이지
language_select.html에서 Java나 Python을 선택하여 각 언어에 대한 코드 생성 및 실행 기능을 시작할 수 있습니다.

### 3. Java 코드 생성 및 실행 페이지
**java_page.html**에서 Generate Java Code 버튼을 클릭하여 Java 코드를 자동 생성합니다.
생성된 Java 코드는 화면에 표시됩니다.
Execute Code 버튼을 클릭하여 생성된 코드를 실행하고 결과를 확인할 수 있습니다.
Generate Explanation 버튼을 클릭하여 생성된 코드에 대한 설명을 받을 수 있습니다.

### 4. 실행 예시
Java 코드 생성: Generate Java Code 버튼을 클릭하면 Java 코드가 자동으로 생성됩니다.
코드 실행: 생성된 코드를 Execute Code 버튼을 통해 실행하여 결과를 확인합니다.
코드 설명: Generate Explanation 버튼을 클릭하여 코드의 기능과 동작에 대해 설명을 받을 수 있습니다.

---

## API 엔드포인트

/generate_code
Method: POST
설명: OpenAI GPT를 사용하여 Java 코드를 생성합니다.
요청 본문: 빈 요청 본문으로 코드를 생성합니다.

응답 예시:
```json
{
  "code": "public class Main { ... }"
}
```

/execute_code
Method: POST
설명: JDoodle API를 사용하여 Java 코드를 실행합니다.
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
설명: 생성된 Java 코드에 대한 설명을 제공합니다.
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

## 프론트엔드 기능

이 애플리케이션은 사용자가 생성된 코드를 실행하고 수정하는 등 여러 기능을 웹 페이지에서 직접 사용할 수 있도록 합니다. 주요 JavaScript 함수는 다음과 같습니다:

1. generateCode()
목적: /generate_code 엔드포인트로 Java 코드 생성을 요청합니다.
동작 방식:
빈 POST 요청을 서버로 보냅니다.
서버에서 OpenAI GPT를 통해 Java 코드를 생성하고, 생성된 코드를 클라이언트로 반환합니다.
반환된 코드를 웹 페이지에 표시합니다.

3. executeCode()
목적: 생성된 Java 코드를 실행하여 실행 결과를 화면에 출력합니다.
동작 방식:
페이지에서 생성된 코드를 가져옵니다.
/execute_code 엔드포인트에 POST 요청을 보내어 JDoodle API를 사용해 코드를 실행합니다.
실행 결과를 페이지에 표시합니다.

5. generateExplanation()
목적: 생성된 코드에 대한 설명을 제공합니다.
동작 방식:
페이지에서 생성된 코드를 가져옵니다.
/generate_explanation 엔드포인트에 POST 요청을 보내어 OpenAI GPT가 생성된 코드에 대해 설명을 제공합니다.
설명을 페이지의 출력 영역에 표시합니다.



