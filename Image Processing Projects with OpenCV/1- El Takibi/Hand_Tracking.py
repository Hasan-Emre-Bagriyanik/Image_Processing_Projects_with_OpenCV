# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 12:08:30 2023
@author: Hasan Emre
"""

# Import required libraries (Gerekli kütüphaneleri içe aktar)
import cv2
import time
import mediapipe as mp

# Start camera or video stream (Kamera veya video akışını başlat)
cap = cv2.VideoCapture(0)  # 0, represents the current camera (0, mevcut kamerayı temsil eder)
# If video is to be used: (Eğer video kullanılacaksa:)
# cap = cv2.VideoCapture('video.mp4') # Replace 'video.mp4' with the name of the video file to be used
# (cap = cv2.VideoCapture('video.mp4')  # 'video.mp4' yerine kullanılacak video dosyasının adı verilmelidir)

# Create mediapipe object for hands detection (Elleri algılama için mediapipe objesini oluştur)
mpHand = mp.solutions.hands

# Create the mediapipe drawing utils object for drawing hands (Elleri çizim için mediapipe drawing utils objesini oluştur)
mpDraw = mp.solutions.drawing_utils

# Variables to store time information (Zaman bilgilerini saklamak için değişkenler)
pTime = 0
cTime = 0

# Configure mediapipe Hands class to detect hands (Elleri tespit etmek için mediapipe Hands sınıfını yapılandır)
hands = mpHand.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
# - static_image_mode: If False, a continuous stream of video will be processed.
# - max_num_hands: Number of hands that can be detected
# - min_detection_confidence: Detection confidence level (between 0 and 1), higher value means more reliable but less detection.

# (- static_image_mode: Eğer False ise, sürekli bir video akışı üzerinde işlem yapılacak demektir.)
# (- max_num_hands: Algılanabilecek el sayısı)
# (- min_detection_confidence: Algılama güven seviyesi (0 ile 1 arasında), daha yüksek değer daha güvenilir ancak daha az algılama anlamına gelir.)


while True:
    # Capture an image from the camera (Kameradan bir görüntü yakala)
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Detect hands (Elleri tespit et)
    results = hands.process(imgRGB)
    print(results.multi_hand_landmarks)  # View detected hand landmarks (Algılanan el landmark'larını görüntüle)
    
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            # Drawing landmarks on hands (Eller üzerindeki landmark'ları çiz)
            mpDraw.draw_landmarks(img, handlms, mpHand.HAND_CONNECTIONS)
            
            for id, lm in enumerate(handlms.landmark):
                h, w, c = img.shape
                
                # Calculate screen coordinates of landmarks (Landmark'ların ekran koordinatlarını hesapla)
                cx, cy = int(lm.x * w), int(lm.y * h)
                
                # Mark wrist (Bileği işaretle)
                if id == 0:
                    cv2.circle(img, (cx, cy), 9, (255, 0, 0), cv2.FILLED)
                    
    # FPS account (FPS hesapla)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    
    # Add FPS info on image (Görüntü üzerine FPS bilgisini ekle)
    cv2.putText(img, "FPS: " + str(int(fps)), (10, 75), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0))
    
    # Show image (Görüntüyü göster)
    cv2.imshow("img", img)
    
    # break the loop when pressing the 'q' key ('q' tuşuna basıldığında döngüyü kır)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release camera or video stream (Kamera veya video akışını serbest bırak)
cap.release()
cv2.destroyAllWindows()
