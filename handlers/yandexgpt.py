import os
import requests
from aiogram import Router
from aiogram.types import Message
from dotenv import find_dotenv, load_dotenv

from filters.chat_types import ChatTypeFilter
load_dotenv(find_dotenv())

yagpt_router = Router()
yagpt_router.message.filter(ChatTypeFilter(["private"]))


Ya_katalogID=os.getenv("katalogID")
YaAPI=os.getenv("YAGPT_key")
url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"


async def generate_answer(user_message):
    print('Сообщение генерируется...')
    prompt = {
    "modelUri": "gpt://b1gginuulth9hup34bk6/yandexgpt-lite",
    "completionOptions": {
        "stream": False,
        "temperature": 0.6,
        "maxTokens": "2000"
    },
    "messages": [
        {
            "role": "system",
            "text": "Ты - компаньон(ассистент) МТУСИ, который даст ответ на любой вопрос по университету."
        },
        {
            "role": "assistant",
            "text": f"{user_message}"
        },
    ]}
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key AQVNwsOZal98QJkYpBkpSCby89OWpIeMIShhJUBw"
    }
    response = requests.post(url, headers=headers, json=prompt)
    result = response.json()
    #print(type(result))
    #print(len(result['result']['alternatives']))
    finish=result['result']['alternatives'][0]['message']['text']
    return finish

