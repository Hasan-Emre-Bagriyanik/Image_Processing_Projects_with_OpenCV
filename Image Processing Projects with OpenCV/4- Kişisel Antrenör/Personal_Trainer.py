# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 12:09:22 2023
@author: Hasan Emre
"""

# Import necessary libraries  (Gerekli kütüphaneleri içe aktar)
import cv2
import mediapipe as mp
import numpy as np
import math

# Define a function to find the angle between three points
# Üç nokta arasındaki açıyı bulmak için bir işlev tanımlama
def findAngle(img, p1, p2, p3, lmList, draw=True):
    x1, y1 = lmList[p1][1:] 
    x2, y2 = lmList[p2][1:] 
    x3, y3 = lmList[p3][1:] 
    
    # Calculate the angle
    # Açıyı hesapla
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    
    if angle < 0: 
        angle += 360
    
    if draw == True:
        # Draw lines and circles on the image to visualize the points and angle
        # Noktaları ve açıyı görselleştirmek için resim üzerine çizgiler ve daireler çiz
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
        cv2.line(img, (x2, y2), (x3, y3), (0, 0, 255), 3)
        cv2.circle(img, (x1, y1), 10, (0, 255, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (0, 255, 255), cv2.FILLED)
        cv2.circle(img, (x3, y3), 10, (0, 255, 255), cv2.FILLED)
        
        cv2.circle(img, (x1, y1), 15, (0, 255, 255))
        cv2.circle(img, (x2, y2), 15, (0, 255, 255))
        cv2.circle(img, (x3, y3), 15, (0, 255, 255))
        
        cv2.putText(img, str(int(angle)), (x2 - 40, y2 + 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
    return angle

# Open the video stream
# Video akışını aç
cap = cv2.VideoCapture("video1.mp4")  # If using a video file, specify the file name
# Eğer bir video dosyası kullanılıyorsa, dosya adını belirtin
# If using the camera:
# Eğer kamera kullanılıyorsa:
# cap = cv2.VideoCapture(0)

mpPose = mp.solutions.pose
pose = mpPose.Pose()

mpDraw = mp.solutions.drawing_utils

dir = 0
count = 0

while True:
    success, img = cap.read()
    # img = cv2.resize(img, (1200, 900))
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    lmList = []
    
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
    # print(lmList)
    
    if len(lmList) != 0:
        # Push-up counter
        # Şınav sayacı
        angle = findAngle(img, 11, 13, 15, lmList)
        per = np.interp(angle, (185, 245), (0, 100))
        
        if per == 100:
            if dir == 0:
                count += 0.5
                dir = 1
                
        if per == 0:
            if dir == 1:
                count += 0.5
                dir = 0
        
        cv2.putText(img, str(int(count)), (45, 125), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 7)
        
        # You can implement similar logic for other exercises
        # Diğer egzersizler için benzer mantığı uygulayabilirsiniz
        
    cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
