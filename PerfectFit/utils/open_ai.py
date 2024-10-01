import json
import os

import requests
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM,pipeline

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


# Llama API 키 가져오기 (가정)
LLAMA_API_KEY = os.getenv('LLAMA_API_KEY')

base = 'beomi/Llama-3-Open-Ko-8B-Instruct-preview'
finetuned = 'beomi/KoAlpaca-13B-LoRA'


def get_test_llama():
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3.1:latest",
        "prompt": "<|begin_of_text|><|start_header_id|>너는 IT 기업 채용을 위해 초빙 된, 한국인 면접 전문가야<|end_header_id|> "
                  "너는 한국어로만 말을 해야해.  " # 역할 지정. 
                  "백엔드 개발자 직군 채용 면접을 진행중이야. 질문을 5개 내줘. "
                  "추가로 너가 생각하는 이상적인 답변도 덧붙여줘. "
                  "답변의 구성을  [ 질문, 답변 ] 식으로 구성해. "
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, json=data, headers=headers)

    # 개별 JSON 객체로 분할
    json_objects = response.content.decode().strip().split("\n")

    # 각 JSON 객체를 Python 사전으로 변환
    data = [json.loads(obj) for obj in json_objects]
    res_text = ''
    # 변환된 데이터 출력
    for item in data:
        res_text += item['response']

    print(res_text)

    if response.status_code == 200:
        print('Success')
    else:
        print("Error:", response.status_code, response.text)

def get_test_llama_transformers():
    # Hugging Face의 pipeline 사용
    model_id = "beomi/KoAlpaca-Polyglot-5.8B"
    
    pipe = pipeline("text-generation", model=model_id)

    # 프롬프트 설정
    prompt = "<|begin_of_text|><|start_header_id|>너는 IT 기업 채용을 위해 초빙 된, 한국인 면접 전문가야<|end_header_id|> " \
             "너는 한국어로만 말을 해야해. " \
             "백엔드 개발자 직군 채용 면접을 진행중이야. 질문을 5개 만들어줘" \

    # Hugging Face pipeline을 사용하여 응답 생성
    response = pipe(prompt, max_length=512, num_return_sequences=1)

    # 응답 출력
    res_text = response[0]['generated_text']
    print(res_text)
    res_text = response[0]['generated_text']
    print(response)
    print(response[0])
    print(response[1])

def get_test_transformers_llama() :
    # model_id = 'llama3:latest'

    model_id = "beomi/KoAlpaca-Polyglot-5.8B"

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
    ).to(device=f"cuda", non_blocking=True)
    model.eval()

    pipe = pipeline(
        'text-generation',
        model=model,
        tokenizer=model_id,
        device=0
    )
    messages = [
        {"role": "system", "content": "너는 매우 전문적인 시니어 백엔드 개발자. 면접관으로서 참여한거야."},
        {"role": "user", "content": "백엔드 개발자 주니어 채용 면접 현장에 와있어.너는 면접관으로서 기술에 관련된 질문을 5개 해야해. 질문과 답변 모두 한국어로 해."},
    ]

    input_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)

    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = model.generate(
        input_ids,
        max_new_tokens=512,
        eos_token_id=terminators,
        do_sample=True,
        temperature=1,
        top_p=0.9,
    )
    response = outputs[0][input_ids.shape[-1]:]
    print(tokenizer.decode(response, skip_special_tokens=True))