import cv2
import numpy as np
from Face import Face_Model
from queue import Queue
from threading import Thread
from utils import compute_color_for_labels, get_center, center_match

face_model = Face_Model()
count = 0
out_people = [{'Name': 'uknown', 'Sim':  -1, 'Position': 'None', "Office":  'None', 'path': 'icon/unknown_person.jpg', 'center': np.array([0, 0])}]
def read_thread(cap, frame_ori_queue, frame_detect_queue):
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        frame_ori_queue.put(frame)
        frame_detect_queue.put(frame)
    cap.release()
def detect_thread(cap, frame_detect_queue, data_recognize_queue):
    global count
    while cap.isOpened():
        frame = frame_detect_queue.get()
        count += 1
        faces, kpss = face_model.detect(frame)
        put_data = {'frame': frame, 'faces':faces, 'kpss':kpss}
        data_recognize_queue.put(put_data)
    cap.release()
def recognize_thread(cap, data_recognize_queue, data_final_queue):
    global count
    while cap.isOpened():
        data = data_recognize_queue.get()
        frame = data['frame']
        faces = data['faces']
        kpss = data['kpss']
        people = []
        if count >= 20:
            count = 0
            for idx, kps in enumerate(kpss):
                feet = face_model.face_encoding(frame, kps)
                info = face_model.face_compare(feet)
                center = get_center(faces[idx])
                info.update({'center': center})
                people.append(info)
        final_data = {'faces': faces, 'people': people}
        data_final_queue.put(final_data)
    cap.release()
def draw_thread(cap, frame_ori_queue, data_final_queue, frame_final_queue):
    global out_people
    while cap.isOpened():
        frame = frame_ori_queue.get()
        data = data_final_queue.get()
        faces = data['faces']
        people = data['people']
        for idx, face in enumerate(faces):
            face_box = face.astype(np.int)
            if people == []:
                people = out_people
            out_people = people
            try:
                now_center = get_center(face_box)
                i = center_match(now_center, people)
                info = people[i]
                color = compute_color_for_labels(sum([ord(character) for character in info['Name']]))
                t_size = cv2.getTextSize(info['Name'], fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, thickness=1)[0]
                cv2.rectangle(frame, (face_box[0], face_box[1]), (face_box[0] + t_size[0] + 10, face_box[1] + t_size[1] + 10), color, -1)
                cv2.putText(frame, info['Name'], (face_box[0], face_box[1]+t_size[1]+5), cv2.FONT_HERSHEY_PLAIN,
                            fontScale=1.0, color=(255, 255, 255), thickness=1, lineType=cv2.LINE_AA)
                cv2.rectangle(frame, (face_box[0], face_box[1]), (face_box[2], face_box[3]), color, 2)
            except:
                continue
        frame_final_queue.put(frame)
    cap.release()

def run_thread(cap):
    frame_ori_queue = Queue(maxsize=2)
    frame_detect_queue = Queue(maxsize=2)
    data_recognize_queue = Queue(maxsize=2)
    data_final_queue = Queue(maxsize=2)
    frame_final_queue = Queue(maxsize=2)


    Thread(target=read_thread, args=[cap, frame_ori_queue, frame_detect_queue]).start()
    Thread(target=detect_thread, args=[cap, frame_detect_queue, data_recognize_queue]).start()
    Thread(target=recognize_thread, args=[cap, data_recognize_queue, data_final_queue]).start()
    Thread(target=draw_thread, args=[cap, frame_ori_queue, data_final_queue, frame_final_queue]).start()
    return frame_final_queue

if __name__ == '__main__':
    cap = cv2.VideoCapture('sample/TrumpvsBinden.mp4')
    frame_final_queue = run_thread(cap)

    while True:
        timer = cv2.getTickCount()
        frame = frame_final_queue.get()
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        t_size = cv2.getTextSize('FPS: %d'%(fps), cv2.FONT_HERSHEY_PLAIN, fontScale=2.0, thickness=2)[0]
        cv2.rectangle(frame, (10, 10), (10+t_size[0]+10, 10+t_size[1]+10), (128, 0, 128), -1)
        cv2.putText(frame, "FPS: %d"%(fps), (10, 10+t_size[1]+10-3), cv2.FONT_HERSHEY_PLAIN,
                    fontScale=2.0, color=(255, 255, 255), thickness=2, lineType=cv2.LINE_AA)
        cv2.imshow('img', frame)
        cv2.waitKey(5)