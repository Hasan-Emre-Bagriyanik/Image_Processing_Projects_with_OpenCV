# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 11:23:43 2023
@author: Hasan Emre
"""

# Import the necessary libraries
# Gerekli kütüphaneleri içe aktar
import cv2
import mediapipe as mp

# Open the video stream
# Video akışını aç
cap = cv2.VideoCapture("video3.mp4")  # If using a video file, specify the file name
#cap = cv2.VideoCapture(0)  # If using the camera: 0

# Create the Mediapipe face detection class
# Mediapipe yüz tespit sınıfını oluştur
mpfaceDetection = mp.solutions.face_detection
faceDetection = mpfaceDetection.FaceDetection()

# Mediapipe drawing utils object
# Mediapipe çizim yardımcıları nesnesini oluştur
mpDraw = mp.solutions.drawing_utils

while True:
    # Read a frame from the video stream
    # Video akışından bir kare oku
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Process the image with the face detection algorithm
    # Görüntüyü yüz tespit algoritmasıyla işle
    results = faceDetection.process(imgRGB)
    
    if results.detections:
        for id, detections in enumerate(results.detections):
            bboxC = detections.location_data.relative_bounding_box
            
            # Get image dimensions
            # Görüntü boyutlarını al
            h, w, _ = img.shape
            
            # Convert relative bounding box to pixel values
            # Göreceli sınırlama kutusunu piksel değerlerine dönüştür
            bbox = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)
            
            # Draw the bounding box
            # Sınırlama kutusunu çiz
            cv2.rectangle(img, bbox, (0, 255, 255), 2)            
            
    # Display the image
    # Görüntüyü göster
    cv2.imshow("img", img)
    
    # Break the loop when 'q' key is pressed
    # 'q' tuşuna basıldığında döngüyü kır
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break
    
# Release the video stream and close windows
# Video akışını serbest bırak ve pencereleri kapat
cap.release()
cv2.destroyAllWindows()
