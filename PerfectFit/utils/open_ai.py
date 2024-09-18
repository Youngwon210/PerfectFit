import os
from dotenv import load_dotenv
import requests

# .env 파일 로드
load_dotenv()

# OpenAI API 키 가져오기
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


def get_dinner_recommendation():
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {'role': 'system', 'content': '넌 지금부터 유사 백종원 선생이야'},
            {'role': 'user', 'content': '오늘의 저녁 메뉴를 선택 해줘 난 매운게 땡겨'}
        ],
        'max_tokens': 50,
        'temperature': 0.7
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()['choices'][0]['message']['content'].strip()
        print(result)
        return result
    else:
        return f"Error: {response.status_code}, {response.text}"
