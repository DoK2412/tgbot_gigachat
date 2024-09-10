from database.connection import JobDb
import database.scheme as scheme
import requests
import os
import json
import subprocess



async def writing_request(user):
    user.requests -= 1
    async with JobDb() as connector:
        await connector.execute(scheme.UPPDATA_COUNT, user.requests, user.id)


async def adding_request(user):
    user.requests += 1


async def authorization_token():
    payload = 'scope=GIGACHAT_API_PERS'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': os.getenv('CLIENT'),
        'Authorization': f'Basic {os.getenv("AUTORIZATION")}'
    }
    response = requests.request("POST", os.getenv('URL'), headers=headers, data=payload, verify=False)

    if response.status_code == 200:
        os.environ['ACCESS_TOKEN'] = json.loads(response.text)['access_token']


async def translator_text(user, text):

    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
                "role": "system",
                "content": f"Ты профессиональный переводчик на {user.language} язык. Переведи точно сообщение пользователя."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        "n": 1,
        "stream": False,
        "update_interval": 0
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {os.getenv("ACCESS_TOKEN")}'
    }

    response = requests.request("POST", os.getenv('URL_TRANSLATE'), headers=headers, data=payload, verify=False)
    if response.status_code == 200:
        return json.loads(response.text)['choices'][0]['message']['content']
    else:
        await authorization_token()
        result = await translator_text(user, text)
        return result










