import requests
import json

url = 'https://api.fpt.ai/hmi/tts/v5'

payload = 'Xin chào Duy Ngu'
headers = {
    'api-key': '2si7NCyCvtiURDC7CD1YZXly7eTknsj1',
    'speed': '',
    'voice': 'banmai'
}

response = requests.request('POST', url, data=payload.encode('utf-8'), headers=headers)
rep = response.json()
print(rep)
link = rep['async']

r = requests.get(link, allow_redirects=True)
open(f'{payload}.mp3', 'wb').write(r.content)