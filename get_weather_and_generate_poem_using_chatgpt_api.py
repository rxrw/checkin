import requests
import json
import os

# get the weather of beijing from tianxing api
response = requests.get('https://apis.tianapi.com/tianqi/index', params={'key': os.environ.get('TIANAPI_KEY'), 'city': '北京'})
weather_info = response.json()['result']

headers = {
    "Authorization": "Bearer " + os.environ.get('CHAT_KEY')
}
response = requests.post('https://' + os.environ.get('OPENAI_DOMAIN') + '/v1/chat/completions', json={
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "assistant",
            "content": "你是一个编写早上问候的工具。我会给你今天的天气情况,你只需要根据天气情况写一段话,大概100字左右。内容表达的意思是“我这里天气是这样的,不知道你那里的天气如何。希望你一切都好这种的”。要添加一些诗意或伤感的话。要暧昧一些。整体的语句可以像诗一样，也可以小红书风格，或知乎风格，随机即可。"
        },
        {
            "role": "user",
            "content": json.dumps(weather_info)
        }
    ]
}, headers=headers)

chat_result = response.json()['choices'][0]['message']['content']

response = requests.get('https://api2.pushdeer.com/message/push', params={'pushkey': os.environ.get('PUSHDEER_KEY'), 'text': chat_result})
result = response.json()

print(result)
