import cv2
import numpy as np
import os
import playsound

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
        center = person['center']
        d.append(np.linalg.norm(now_center-center))
    d = np.array(d)
    return np.where(d == np.amin(d))[0][0]

def play_sound(type=0):
    path = 'sound/beep-0%d.mp3'%(type)
    try:
        playsound.playsound(path, True)
    except:
        pass