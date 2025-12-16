import requests
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoTest.settings')
django.setup()
from .models import ProgrammingLanguage, Prompt
from .utils import *
from asgiref.sync import sync_to_async

@sync_to_async
def getPromptText(prompt_id):
    try:
        return Prompt.objects.get(id=prompt_id).prompt_text
    except Prompt.DoesNotExist:
        return None
    except Exception as e:
        print(f"Database error: {str(e)}")
        return None

@sync_to_async
def getProgLng(language_id):
    try:
        return ProgrammingLanguage.objects.get(id=language_id).language_name
    except ProgrammingLanguage.DoesNotExist:
        return None
    except Exception as e:
        print(f"Database error: {str(e)}")
        return None

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.client_id = self.scope['url_route']['kwargs']['client_id']
        await self.accept()
        print(f"WebSocket connected for client {self.client_id}")

    async def disconnect(self, close_code):
        print(f"Connection closed for client {self.client_id}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            print(f"Received data: {data}")

            # Обработка нажатия кнопки Clear Context
            if data.get('action') == 'clear_context':
                # Очищаем историю в utils.py
                if self.client_id in hist:
                    hist[self.client_id] = []
                self.old_language = None
                # Отправляем простое сообщение без тегов think
                await self.send(text_data="Контекст очищен")
                return

            type = data.get('type', '1')
            message = data.get('message', '')
            language = data.get('language', 'Russian')
            value = data.get("value", "DeepSeek_R1")
            
            print(f"Processing message: type={type}, language={language}, model={value}")

            # Обработка языка
            if hasattr(self, 'old_language') and self.old_language != language:
                language_instruction = ""
                if language == "Русский":
                    language_instruction = ". Разговаривай со мной только по-русски"
                elif language == "Français":
                    language_instruction = ". Communiquez avec moi uniquement en français"
                elif language == "English":
                    language_instruction = ". Communicate with me only in English"
                
                if language_instruction:
                    message += language_instruction
            
            self.old_language = language

            # Обработка специальных типов сообщений
            if type == "2":
                progLng = await getProgLng(data.get('progLng'))
                promptText = await getPromptText(data.get('preprompt'))
                message = f"У меня есть задача по программированию, решай ее на языке {progLng}\n{message}"
                if promptText and (not hasattr(self, 'last_prompt') or self.last_prompt != promptText):
                    message += f". Препромпт: {promptText}"
                    self.last_prompt = promptText
            
            elif type == "3":
                progLng = await getProgLng(data.get('progLng'))
                code = data.get('code', '')
                promptText = await getPromptText(data.get('preprompt'))
                message = f"У меня есть задача по программированию, я написал для нее код на языке {progLng}, код не работает, найди пожалуйста ошибку. Задача: {message}. Код: {code}."
                if promptText and (not hasattr(self, 'last_prompt') or self.last_prompt != promptText):
                    message += f". Препромпт: {promptText}"
                    self.last_prompt = promptText

            # Отправляем сообщение пользователю
            await self.send(text_data=f"<think>Обрабатываю запрос пользователя</think>Вы: {message}")

            # Обработка модели AI
            response = "Что-то пошло не так. Попробуйте еще раз."
            
            try:
                # Используем выбранную модель
                if value == "Meta_Llama_3_1_70B_Instruct":
                    response = await ask_Meta_Llama_3_1_70B_Instruct_async(message, self.client_id)
                elif value == "Mixtral_8x7B":
                    # Используем Mixtral 8x22b как замену
                    response = await ask_Mixtral_8x22b_async(message, self.client_id)
                elif value == "Mixtral_8x22b":
                    response = await ask_Mixtral_8x22b_async(message, self.client_id)
                elif value == "DeepSeek_R1_Distill_Llama_70B":
                    response = await ask_DeepSeek_R1_Distill_Llama_70B_async(message, self.client_id)
                elif value == "Llama_3_1_Tulu_3_405B":
                    response = await ask_Llama_3_1_Tulu_3_405B_async(message, self.client_id)
                elif value == "DeepSeek_R1":
                    response = await ask_DeepSeek_R1_async(message, self.client_id)
                elif value == "QwQ_32B":
                    response = await ask_QwQ_32B_async(message, self.client_id)
                else:
                    response = f"Модель {value} не найдена. Используйте доступные модели."
                        
            except Exception as e:
                print(f"Error in AI model processing: {str(e)}")
                response = f"Ошибка при обработке запроса: {str(e)}"

            # Отправляем ответ
            await self.send(text_data=f"<think>Запрос успешно обработан</think>Ассистент: {response}")

        except json.JSONDecodeError as e:
            await self.send(text_data="Ошибка: Неверный формат JSON")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            await self.send(text_data="Что-то пошло не так. Очистка контекста, введите новый запрос.")