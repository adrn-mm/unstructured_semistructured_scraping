import cv2
import os
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import subprocess

# Fungsi untuk menampilkan teks pada gambar
def put_text(test_img, text, x, y):
    cv2.putText(test_img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# Lokasi model dan gambar di HDFS
hdfs_image_path = '/user/csso_andrew/images/predict.jpg'
casc_path = 'haarcascade_frontalface_default.xml'

# Lokasi sementara di lokal
local_model_path = 'trainer.yml'
local_image_path = '/tmp/predict.jpg'

# Download gambar dari HDFS
subprocess.run(['hdfs', 'dfs', '-get', hdfs_image_path, local_image_path], check=True)

# Nama untuk setiap label
name = {0: "Anies", 1: "Prabowo", 2: "Ganjar"}

# Memuat detektor wajah dan model pengenalan wajah
detector = cv2.CascadeClassifier(cv2.data.haarcascades + casc_path)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(local_model_path)

# Memuat dan memproses gambar
img = cv2.imread(local_image_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Mendeteksi wajah dalam gambar
faces = detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

print(f'Number of faces detected: {len(faces)}')

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    roi_gray = gray[y:y+h, x:x+w]
    label, confidence = recognizer.predict(roi_gray)
    
    print(f"Confidence: {confidence}, Label: {label}")
    predicted_name = name.get(label, "Unknown")
    put_text(img, predicted_name, x, y-5)

# Mengonversi BGR ke RGB untuk ditampilkan menggunakan matplotlib
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img_rgb)
plt.show()

# Membersihkan file sementara lokal setelah digunakan
os.remove(local_image_path)