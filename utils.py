import cv2
import numpy as np
import os
import playsound
from threading import Thread

palette = (2 ** 11 - 1, 2 ** 15 - 1, 2 ** 20 - 1)


def compute_color_for_labels(label):
    """
    Simple function that adds fixed color depending on the class
    """
    color = [int((p * (label ** 2 - label + 1)) % 255) for p in palette]
    return tuple(color)


def get_center(face):
    x_center = (face[0] + face[2])/2
    y_center = (face[1] + face[3])/2
    return np.array([x_center, y_center])


def center_match(now_center, people):
    d = []
    for idx, person in enumerate(people):
        center = get_center(person['box'])
        d.append(np.linalg.norm(now_center-center))
    d = np.array(d)
    return np.where(d == np.amin(d))[0][0]


def sound(type=0):
    path = 'sound/beep-0%d.mp3'%(type)
    try:
        playsound.playsound(path, True)
    except:
        pass


def play_sound(type=0):
    Thread(target=sound, args=[type]).start()


def save_new_image(dir, image):
    c = 1
    while os.path.exists(os.path.join(dir, '%d.jpg'%(c))):
        c += 1
    cv2.imwrite(os.path.join(dir, '%d.jpg'%(c)), image)

def hello(id):
    def run():
        playsound.playsound('sound/' + id + '.mp3', True)
    Thread(target=run, args=[]).start()


import requests
import json

def download(id, name):
    url = 'https://api.fpt.ai/hmi/tts/v5'
    payload = 'Xin chào ' + name
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
    open(f'sound/{id}.mp3', 'wb').write(r.content)