# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 15:43:54 2023
@author: Hasan Emre
"""

# Import necessary libraries
# Gerekli kütüphaneleri içe aktar
import cv2
import time
import mediapipe as mp

# Open the video stream
# Video akışını aç
cap = cv2.VideoCapture("video2.mp4")  # If using a video file, specify the file name
# cap = cv2.VideoCapture(0)
# Create the Mediapipe face mesh class
# Mediapipe yüz örgüsü sınıfını oluştur
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)

# Mediapipe drawing utils object
# Mediapipe çizim yardımcıları nesnesini oluştur
mpDraw = mp.solutions.drawing_utils
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)

cTime = 0
pTime = 0

while True:
    # Read a frame from the video stream
    # Video akışından bir kare oku
    success, img =  cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # Process the image with the face mesh algorithm
    # Görüntüyü yüz örgüsü algoritmasıyla işle
    results = faceMesh.process(imgRGB)
    
    # print(results.multi_face_landmarks)
    
    if results.multi_face_landmarks:
        for facelms in results.multi_face_landmarks:
            # Draw the face mesh landmarks on the image
            # Yüz örgüsündeki işaret noktalarını resme çiz
            mpDraw.draw_landmarks(img, facelms, mpFaceMesh.FACEMESH_TESSELATION, drawSpec, drawSpec)
            
        for id ,lm in enumerate(facelms.landmark):
            h, w, _ = img.shape
            cx,cy = int(lm.x*w) , int(lm.y*h)
            print([id,cx,cy])
    
    # Calculate and display FPS
    # FPS hesapla ve göster
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, "FPS: "+ str(int(fps)), (10,65), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)
    
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
