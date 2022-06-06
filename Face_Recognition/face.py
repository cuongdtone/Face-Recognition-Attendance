import cv2
import numpy as np
from .deepface import Face, RetinaFace, ArcFaceONNX
import time
import os
import glob
import pickle
from test_sql import add_employee


class Face_Model():

    def __init__(self, root_path='Employee_Infomation'): 
        # task is "half create":  create from directory image of employee
        # task is "full create":  create with take photos
        # task is "load":  load infor to use
        self.root_path = root_path
        self.Face_Recognition = ArcFaceONNX(model_file='FaceModels/w600k_mbf.onnx')
        self.Face_Detection = RetinaFace(model_file='FaceModels/det_500m.onnx')
        # if task == 'half create': 
        #     self.create_data_file()
        # elif task == 'full create': 
        #     #mkdir dir
        #     #take photo
        #     #create data file
        #     pass
        # elif task == 'load': 
        #     #load data file:  position, office, feets
        #     pass


    def detect(self, img):
        return self.Face_Detection.detect(img, max_num=0, metric='default', input_size=(640, 640))


    def create_data_file(self, id, name, position, office, sex):
        path_to_dir = os.path.join(self.root_path, name)
        # position = input("Position:  ")
        # office = input("Office:  ")
        list_img = glob.glob(path_to_dir + '/*.jpg')
        feets = []
        for i in list_img: 
            image = cv2.imread(i)
            # convert all format image to jpg
            if i.split('.')[-1] != 'jpg': 
                os.remove(i)
                path = i.split('.')
                path.pop()
                cv2.imwrite('.'.join(path) + '.jpg', image)
                
            id_img = i.split('/')[-1].split('.')[0]
            try: 
                faces, kpss = self.Face_Detection.detect(image, max_num=0, metric='default', input_size=(640, 640))
                feet = self.face_encoding(image, kpss[0])
                feets.append(feet.tolist())
            except: 
                continue
        feets = np.sum(np.array(feets), axis=0) / len(feets)
        print(feets)
        embed = np.array(feets, dtype='float')
        print(embed.shape)
        data = (id, name, sex, position, office, embed)
        add_employee(data)


    def load_data(self, name): 
        path = os.path.join(self.root_path, name) + '/data.pkl'
        if os.path.exists(path): 
            with open(path, 'rb') as f: 
                data = pickle.load(f)
            return data
        else: 
            return False

    def face_encoding(self, image, kps): 
        face_box_class = {'kps':  kps}
        face_box_class = Face(face_box_class)
        feet = self.Face_Recognition.get(image, face_box_class)
        return feet

    def face_compare(self, feet, data,threshold=0.3):
        info = {'id': None, 'Name': 'uknown', 'Sim': 0, 'Position': 'None', 'Office': 'None'}
        for employee in data:
            feet2 = np.array(employee[5][0])
            sim = self.Face_Recognition.compute_sim(feet, feet2)
            if sim>threshold:
                info['id'] = employee[0]
                info['Name'] = employee[1]
                info['Sim'] = sim
                info['Position'] = employee[3]
                info["Office"] = employee[4]
        return info

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    a = Face_Model()
    a.create_data_file('Trump')
    a.create_data_file('Binden')
    # data = a.load_data('Binden')
    # print(data)

    image = cv2.imread('sample/test2.jpg')
    faces, kpss = a.detect(image)

    time_last = time.time()

    feet = a.face_encoding(image, kpss[0])
    info = a.face_compare(feet)
    time_compare = time.time() - time_last
    print("Time per one compare : ", time_compare)
    print("FPS of compare phase:  ", 1/time_compare)
    print(info)

    plt.subplot(1, 2, 1)
    plt.imshow(image[..., ::-1])
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.imread(info['path'])[..., ::-1])
    plt.show()






