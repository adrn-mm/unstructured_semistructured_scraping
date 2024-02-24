import cv2
import os
import subprocess
from PIL import Image
import numpy as np

# Lokasi folder di HDFS
hdfs_image_path = '/user/csso_adrian.muhammad/images/image_training'

# Lokasi sementara di lokal untuk menyimpan gambar yang diunduh
local_image_path = '/tmp/image_training'

# Mengunduh folder gambar dari HDFS
subprocess.run(['hadoop', 'fs', '-get', hdfs_image_path, local_image_path], check=True)

# Path ke file cascade untuk deteksi wajah
casc_path = 'haarcascade_frontalface_default.xml'
detector = cv2.CascadeClassifier(cv2.data.haarcascades + casc_path)

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')  # convert to grayscale
        img_numpy = np.array(PIL_img, 'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[0])
        faces = detector.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y+h, x:x+w])
            ids.append(id)
    return faceSamples, ids

faces, ids = getImagesAndLabels(local_image_path)
print(f"{len(faces)} faces, {len(ids)} ids in total are detected")

def train_classifier(faces, faceID):
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces, np.array(faceID))
    return face_recognizer

# Train the classifier and save the model
facerecognizer = train_classifier(faces, ids)
facerecognizer.save('trainer.yml')

# Hapus folder gambar sementara di lokal setelah digunakan
subprocess.run(['rm', '-r', local_image_path])