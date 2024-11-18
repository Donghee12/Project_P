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
git clone https://github.com/your-username/java-code-executor.git
cd java-code-executor

---

2. 의존성 설치
python3 -m venv venv
source venv/bin/activate  # Windows의 경우 `venv\Scripts\activate` 명령 사용
pip install -r requirements.txt

3.
