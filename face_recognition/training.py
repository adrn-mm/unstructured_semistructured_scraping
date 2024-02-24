import cv2
import os 
from PIL import Image, ImageDraw
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.image import imread

image_path = os.path.join(os.getcwd(), 'image_raw_data')

casc_path = os.path.join(os.getcwd(), 'haarcascade_frontalface_default.xml')

detector = cv2.CascadeClassifier(casc_path)

recognizer = cv2.face.LBPHFaceRecognizer_create()

image_full_list = ['0.1', '0.2', '0.3', '0.4', '0.5',
                 '1.1', '1.2', '1.3', '1.4', '1.5',
                 '2.1', '2.2', '2.3', '2.4', '2.5']

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)] 
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') #Luminance  ==> greystyle
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[0])
        faces = detector.detectMultiScale(img_numpy)
        if len(faces) > 1:
            print("The following image detect more than 1 face", imagePath)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
            #print(ids)
            
    return faceSamples,ids

faces,ids = getImagesAndLabels(image_path)
print("{0} faces, {0} id in total are detected".format(len(faces), len(ids)))

face_recognizer = cv2.face.LBPHFaceRecognizer_create() 
face_recognizer.train(faces, np.array(ids))

def train_classifier(faces, faceID):
    face_recognizer=cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces, np.array(faceID))
    return face_recognizer

# Save the model as bdktrainer.yml
facerecognizer = train_classifier(faces, ids) 
facerecognizer.save('bdktrainer.yml')