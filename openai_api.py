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
api_key = os.getenv("API_KEY")
print(api_key)
