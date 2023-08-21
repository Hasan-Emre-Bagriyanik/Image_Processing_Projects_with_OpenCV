# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 15:13:06 2023
@author: Hasan Emre
"""

# Import the necessary libraries (Gerekli kütüphaneleri içe aktar)
import cv2
import mediapipe as mp
import time
import math
import numpy as np
 
def findAngle(img, p1, p2, p3, lmList, draw = True):
    x1, y1 = lmList[p1][1:] 
    x2, y2 = lmList[p2][1:] 
    x3, y3 = lmList[p3][1:] 
    
    # açı hesaplama 
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    
    if angle < 0: 
        angle += 360
    
    if draw == True:
        cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 3)
        cv2.line(img, (x2,y2), (x3,y3), (0,0,255), 3)
        cv2.circle(img,(x1,y1), 10, (0,255,255), cv2.FILLED)
        cv2.circle(img,(x2,y2), 10, (0,255,255), cv2.FILLED)
        cv2.circle(img,(x3,y3), 10, (0,255,255), cv2.FILLED)
        
        cv2.circle(img,(x1,y1), 15, (0,255,255))
        cv2.circle(img,(x2,y2), 15, (0,255,255))
        cv2.circle(img,(x3,y3), 15, (0,255,255))
        
        cv2.putText(img, str(int(angle)), (x2 -40, y2 + 40), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,255), 2)
    return angle


# Create the Mediapipe Pose class (Mediapipe Pose sınıfını oluştur)
mpPose = mp.solutions.pose
pose = mpPose.Pose()

# Mediapipe drawing utils object (Mediapipe drawing utils nesnesini oluştur)
mpDraw = mp.solutions.drawing_utils

# Open the video stream (Video akışını aç)
cap = cv2.VideoCapture("video5.mp4")  # If using a video file, specify the file name (Eğer bir video dosyası kullanılıyorsa, dosya adını belirtin)
# If using the camera:  (Eğer kamera kullanılıyorsa:)
# cap = cv2.VideoCapture(0)

# Time variables for calculating FPS (FPS hesaplamak için zaman değişkenleri)
pTime = 0
cTime = 0

while True:
    # Read a frame from the video stream  (Video akışından bir kare oku)
    success, img = cap.read()
    # img = cv2.resize(img, (1200,900))
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Process the image with the pose algorithm  (Görüntüyü pose algoritmasıyla işle)
    results = pose.process(imgRGB)
    print(results.pose_landmarks)
    lmList = []
    if results.pose_landmarks:
        # Draw the pose landmarks  (Pose landmarklarını çiz)
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        
         
        # Sol ve sağ dirseklerin landmarklarına erişim
        left_elbow = results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW]
        right_elbow = results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW]
        
        left_knee = results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE]
        right_knee = results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE]
        
        left_ankle = results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ANKLE]
        right_ankle = results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE]
        
        left_foot_index = results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_FOOT_INDEX]
        right_foot_index  = results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_FOOT_INDEX]
        
        left_wrist = results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_WRIST]
        right_wrist = results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_WRIST]
        
        
        
        
        # Place a marker on a specific landmark ( Belirli bir landmark üzerine işaretçi koy)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id,cx,cy])
            
            
            if (id == 13):  # For instance, you can place a marker on a specific landmark (e.g., landmark number 13)
                # Örneğin, belirli bir landmark üzerine işaretçi koyabilirsiniz (örneğin, 13 numaralı landmark)
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)  # In circle the marker (İşaretçiyi çember içine al)
    
    
        if lmList != 0:
            angle = findAngle(img, 11, 13, 15, lmList)
            angle2 = findAngle(img, 12, 14, 16, lmList)
            # print(angle)
            per = np.interp(angle, (90, 170), (0,100))
            per2 = np.interp(angle2, (190, 270), (0,100))
            if (0 < per < 100 ) and (0 < per2 < 100) and (abs(left_elbow.y - right_elbow.y) < 0.03) and (abs(left_knee.y - right_knee.y) < 0.03)  and (abs(left_knee.x - right_knee.x) < 0.15)and (abs(left_ankle.y - right_ankle.y) < 0.03) and (abs(left_ankle.x - right_ankle.x) < 0.1) and (abs(left_foot_index.y - right_foot_index.y) < 0.03)  and (abs(left_wrist.y - right_wrist.y) < 0.03) and (abs(left_wrist.x - right_wrist.x) < 0.7) :  # Belirlediğiniz açı aralığına göre kontrolü ayarlayabilirsiniz
                cv2.putText(img, "IP ATLIYOR", (180, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
        

    
        
    # Calculate FPS  (FPS hesapla)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    
    # Display FPS on the image (FPS bilgisini görüntü üzerine ekle)
    cv2.putText(img, "FPS: " + str(int(fps)), (10, 65), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    
    # Display the image (Görüntüyü göster)
    cv2.imshow("img", img)
    
    # Break the loop when 'q' key is pressed  ('q' tuşuna basıldığında döngüyü kır)
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

# Release the video stream and close windows (Video akışını serbest bırak ve pencereleri kapat)
cap.release()
cv2.destroyAllWindows()

