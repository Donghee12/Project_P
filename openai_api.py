#openai의 api를 불러오는 코드입니다.
#openai의 api를 사용하기 위해서는 openai의 api key가 필요합니다.
#openai의 api key는 openai의 홈페이지에서 받을 수 있습니다.
#openai의 api를 사용하기 위해서는 openai의 python sdk를 설치해야합니다.
#openai의 python sdk는 pip install openai로 설치할 수 있습니다.
from dotenv import load_dotenv
import os

# .env 파일을 로드
load_dotenv()

# 환경 변수 가져오기
api_key_ = os.getenv("API_KEY")
from openai import OpenAI

# API 키 설정
client = OpenAI(api_key=api_key_)

# API 요청을 위한 메시지 구성
response = client.chat.completions.create(
    model="gpt-4o-mini",  # 사용할 모델
    messages=[
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
        {"role": "user", "content": "당신은 숙련된 프로그래머입니다. 당신의 목표는 사용자 요청에 맞춰 Java, Python 코드를 작성하는 것입니다."},
        {"role": "user", "content": "Java, Python 코드를 작성해 주세요. 수준은 데이터 입출력, 제어문. Java는 클래스, 추상 클래스와 형 변환, 상속, 예외처리에 관한 내용을 담을 것."}
        {"role": "user", "content": "Python은 자료형, Slice, Range, 리스트, 람다 식에 관한 내용을 담을 것"},
        {"role": "user", "content": "코드의 수준은 중급으로 작성하고, 한국의 정보처리기사 실기에 나올만한 코드로 작성할 것"},
        
    ]
)

# 결과 출력
result = response.choices[0].message.content
print(result)