import json
from channels.generic.websocket import AsyncWebsocketConsumer
import os
import uuid
import asyncio
import copy
#from chat.database import insert_into_bd,start_bd
from http import cookies
import requests
from requests.auth import HTTPBasicAuth
from huggingface_hub import InferenceClient
from dotenv import load_dotenv


load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
SECRET = os.getenv("SBER_SECRET")
HF_TOKEN = os.getenv("HF_TOKEN")
SC_TOKEN=os.getenv("SC_TOKEN")
MIST_TOKEN = os.getenv("MIST_TOKEN")
GROQ_TOKEN = os.getenv("GROQ_TOKEN")


hist=dict([])

proxies = {
            'http': os.getenv("PROXY"),
            'https': os.getenv("PROXY")
        }


async def ask_DeepSeek_R1_async(messages: str, user_id: int) -> str:
    if user_id not in hist:
        hist[user_id] = []
    hist[user_id].append({"role": "user", "content": messages})
    try:
        response = await asyncio.to_thread(requests.post, 'https://api.sambanova.ai/v1/chat/completions', json={
            "model": "DeepSeek-R1",
            "messages": hist[user_id],
            "max_tokens": 9000
        }, headers={
            'Authorization': f'Bearer {SC_TOKEN}',
        },
        proxies=proxies
        )

        # Логирование статуса ответа и содержимого
        print(f"Response Status: {response.status_code}")
        print(f"Response Content: {response.text}")

        response_content = response.content.decode('utf-8')
        if not response_content:
            raise ValueError("Пустой ответ от сервера.")

        try:
            obj = json.loads(response_content)
        except json.JSONDecodeError as e:
            print(f"Ошибка при декодировании JSON: {e}")
            print(f"Содержимое ответа: {response_content}")
            return 'Что-то пошло не так с обработкой JSON.'

        hist[user_id].append({"role": "assistant", "content": obj['choices'][0]['message']['content']})
        return obj['choices'][0]['message']['content']
    except Exception as e:
        print(f"Общая ошибка: {e}")
        hist[user_id]=[]
        return 'Что-то пошло не так. Контекст очищен, введите новый запрос.'

async def ask_DeepSeek_R1_Distill_Llama_70B_async(messages: str, user_id: int) -> str:
    if user_id not in hist:
        hist[user_id] = []
    hist[user_id].append({"role": "user", "content": messages})
    try:
        response = await asyncio.to_thread(requests.post, 'https://api.sambanova.ai/v1/chat/completions', json={
            "model": "DeepSeek-R1-Distill-Llama-70B",
            "messages": hist[user_id],
            "max_tokens": 9000
        }, headers={
            'Authorization': f'Bearer {SC_TOKEN}',
        },
        proxies=proxies
        )

        # Логирование статуса ответа и содержимого
        print(f"Response Status: {response.status_code}")
        print(f"Response Content: {response.text}")

        response_content = response.content.decode('utf-8')
        if not response_content:
            raise ValueError("Пустой ответ от сервера.")

        try:
            obj = json.loads(response_content)
        except json.JSONDecodeError as e:
            print(f"Ошибка при декодировании JSON: {e}")
            print(f"Содержимое ответа: {response_content}")
            return 'Что-то пошло не так с обработкой JSON.'

        hist[user_id].append({"role": "assistant", "content": obj['choices'][0]['message']['content']})
        return obj['choices'][0]['message']['content']
    except Exception as e:
        print(f"Общая ошибка: {e}")
        hist[user_id]=[]
        return 'Что-то пошло не так. Контекст очищен, введите новый запрос.'

async def ask_Llama_3_1_Tulu_3_405B_async(messages: str, user_id: int) -> str:
    if user_id not in hist:
        hist[user_id] = []
    hist[user_id].append({"role": "user", "content": messages})
    try:
        response = await asyncio.to_thread(requests.post, 'https://api.sambanova.ai/v1/chat/completions', json={
            "model": "Meta-Llama-3.1-405B-Instruct",
            "messages": hist[user_id],
            "max_tokens": 9000
        }, headers={
            'Authorization': f'Bearer {SC_TOKEN}',
        },
        proxies=proxies
        )

        # Логирование статуса ответа и содержимого
        print(f"Response Status: {response.status_code}")
        print(f"Response Content: {response.text}")

        response_content = response.content.decode('utf-8')
        if not response_content:
            raise ValueError("Пустой ответ от сервера.")

        try:
            obj = json.loads(response_content)
        except json.JSONDecodeError as e:
            print(f"Ошибка при декодировании JSON: {e}")
            print(f"Содержимое ответа: {response_content}")
            return 'Что-то пошло не так с обработкой JSON.'

        hist[user_id].append({"role": "assistant", "content": obj['choices'][0]['message']['content']})
        return obj['choices'][0]['message']['content']
    except Exception as e:
        print(f"Общая ошибка: {e}")
        return 'Что-то пошло не так.'


async def ask_Meta_Llama_3_1_70B_Instruct_async(messages: str, user_id: int) -> str:
    if user_id not in hist:
        hist[user_id] = []
    hist[user_id].append({"role": "user", "content": messages})
    try:
        response = await asyncio.to_thread(requests.post, 'https://api.sambanova.ai/v1/chat/completions', json={
            "model": "Meta-Llama-3.3-70B-Instruct",
            "messages": hist[user_id],
            "max_tokens": 9000
        }, headers={
            'Authorization': f'Bearer {SC_TOKEN}',
        },
        proxies=proxies
        )

        # Логирование статуса ответа и содержимого
        print(f"Response Status: {response.status_code}")
        print(f"Response Content: {response.text}")
        response_content = response.content.decode('utf-8')
        if not response_content:
            raise ValueError("Пустой ответ от сервера.")

        try:
            obj = json.loads(response_content)
        except json.JSONDecodeError as e:
            print(f"Ошибка при декодировании JSON: {e}")
            print(f"Содержимое ответа: {response_content}")
            return 'Что-то пошло не так с обработкой JSON.'

        hist[user_id].append({"role": "assistant", "content": obj['choices'][0]['message']['content']})
        return obj['choices'][0]['message']['content']
    except Exception as e:
        print(f"Общая ошибка: {e}")
        return 'Что-то пошло не так.'



async def ask_Mistral_Nemo_Instruct_async(messages: str, user_id: int) -> str:
    if user_id not in hist:
        hist[user_id] = []
    client = InferenceClient(
        "mistralai/Mistral-Nemo-Instruct-2407",
        token=HF_TOKEN,
    )
    answer = ""
    hist[user_id].append({"role": "user", "content": messages})
    async for message in client.chat_completion(
        messages=hist[user_id],
        max_tokens=9000,
        stream=True,
    ):
        answer += message.choices[0].delta.content
    hist[user_id].append({"role": "assistant", "content": answer})
    return answer


async def ask_QwQ_32B_async(messages: str, user_id: int) -> str:
    if user_id not in hist:
        hist[user_id] = []
    hist[user_id].append({"role": "user", "content": messages})
    try:
        response = await asyncio.to_thread(requests.post, 'https://api.sambanova.ai/v1/chat/completions', json={
            "model": "QwQ-32B",
            "messages": hist[user_id],
            "max_tokens": 4000
        }, headers={
            'Authorization': f'Bearer {SC_TOKEN}',
        },
        proxies=proxies
        )

        # Логирование статуса ответа и содержимого
        print(f"Response Status: {response.status_code}")
        print(f"Response Content: {response.text}")

        response_content = response.content.decode('utf-8')
        if not response_content:
            raise ValueError("Пустой ответ от сервера.")

        try:
            obj = json.loads(response_content)
        except json.JSONDecodeError as e:
            print(f"Ошибка при декодировании JSON: {e}")
            print(f"Содержимое ответа: {response_content}")
            return 'Что-то пошло не так с обработкой JSON.'

        hist[user_id].append({"role": "assistant", "content": '<think>'+obj['choices'][0]['message']['content']})
        return '<think>'+obj['choices'][0]['message']['content']
    except Exception as e:
        print(f"Общая ошибка: {e}")
        return 'Что-то пошло не так.'

async def ask_Mixtral_8x22b_async(messages: str, user_id: int) -> str:
    if user_id not in hist:
        hist[user_id] = []
    hist[user_id].append({"role": "user", "content": messages})
    try:
        response = await asyncio.to_thread(requests.post, 'https://api.mistral.ai/v1/chat/completions', json={
            "model": "open-mixtral-8x22b",
            "messages": hist[user_id],
            "max_tokens": 9000
        }, headers={
            'Authorization': f'Bearer {MIST_TOKEN}',
        }, proxies=proxies
        )
        response_content = response.content.decode('utf-8')
        if not response_content:
            raise ValueError("Пустой ответ от сервера.")
        obj = json.loads(response_content)
        hist[user_id].append({"role": "assistant", "content": obj['choices'][0]['message']['content']})
        return obj['choices'][0]['message']['content']
    except json.JSONDecodeError as e:
        print(f"Ошибка при декодировании JSON: {e}")
        print(f"Содержимое ответа: {response_content}")
        return 'Что-то пошло не так с обработкой JSON.'
    except Exception as e:
        print(f"Общая ошибка: {e}")
        return 'Что-то пошло не так.'


async def ask_Gemma_7b_async(messages: str, user_id: int) -> str:
    if user_id not in hist:
        hist[user_id] = []
    hist[user_id].append({"role": "user", "content": messages})
    try:
        response = await asyncio.to_thread(requests.post, 'https://api.groq.com/openai/v1/chat/completions', json={
            "model": "gemma-7b-it",
            "messages": hist[user_id],
            "max_tokens": 8192
        }, headers={
            'Authorization': f'Bearer {GROQ_TOKEN}',
        }, proxies=proxies
        )
        response_content = response.content.decode('utf-8')
        if not response_content:
            raise ValueError("Пустой ответ от сервера.")
        obj = json.loads(response_content)
        hist[user_id].append({"role": "assistant", "content": obj['choices'][0]['message']['content']})
        return obj['choices'][0]['message']['content']
    except json.JSONDecodeError as e:
        print(f"Ошибка при декодировании JSON: {e}")
        print(f"Содержимое ответа: {response_content}")
        return 'Что-то пошло не так с обработкой JSON.'
    except Exception as e:
        print(f"Общая ошибка: {e}")
        return 'Что-то пошло не так.'

async def send_prompt_async(msg: str, access_token: str) -> str:
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    payload = json.dumps({
        "model": "GigaChat-Pro",
        "messages": [
            {
                "role": "user",
                "content": msg,
            }
        ],
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = await asyncio.to_thread(requests.post, url, headers=headers, data=payload, verify=False)
    response_content = response.content.decode('utf-8')
    try:
        return response.json()["choices"][0]["message"]["content"]
    except json.JSONDecodeError as e:
        print(f"Ошибка при декодировании JSON: {e}")
        print(f"Содержимое ответа: {response_content}")
        return 'Что-то пошло не так с обработкой JSON.'
    except Exception as e:
        print(f"Общая ошибка: {e}")
        return 'Что-то пошло не так.'
