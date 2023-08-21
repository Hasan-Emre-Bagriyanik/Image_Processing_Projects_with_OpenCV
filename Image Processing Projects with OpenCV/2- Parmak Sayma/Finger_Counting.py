# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 12:57:54 2023
@author: Hasan Emre
"""

# Import required libraries (Gerekli kütüphaneleri içe aktar)
import cv2
import mediapipe as mp

# Camera settings (Kamera ayarları)
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Set camera width (Kamera genişliği ayarla)
cap.set(4, 480)  # Set camera height (Kamera yüksekliği ayarla)

# Create mediapipe object for hands detection (Elleri algılama için mediapipe objesini oluştur)
mpHand = mp.solutions.hands
hands = mpHand.Hands()

# Create mediapipe drawing utils object for drawing hands (Elleri çizim için mediapipe drawing utils objesini oluştur)
mpDraw = mp.solutions.drawing_utils

# Index finger, ring finger, middle finger, little finger, tip of thumb
# (İşaret parmağı, yüzük parmağı, orta parmak, serçe parmak, baş parmağın uç noktalarının indeksleri)
tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    results = hands.process(imgRGB)
    print(results.multi_hand_landmarks)
    
    lmList = []  # List of Landmarks  (Landmark'ların listesi)
    totalF = 0 
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handlms, mpHand.HAND_CONNECTIONS)
            
            for id, lm in enumerate(handlms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
    
    # Determining the state of the fingers (Parmakların durumunu belirleme)
    if len(lmList) != 0:
        fingers = []  # List that stores the state of each finger (Her bir parmağın durumunu saklayan liste)
        
        # Determining the index finger pointing (İşaret parmağının durumunu belirleme)
        if lmList[tipIds[0]][1] < lmList[tipIds[1]][1]:
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                fingers.append(1)  # index finger up ( İşaret parmağı yukarı kalkık durumda)
            else:
                fingers.append(0)  # index finger down (İşaret parmağı aşağı kalkık durumda)
        else:
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        # Determining the state of other fingers (Diğer parmakların durumunu belirleme)
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)  # with the finger up (Parmağı yukarı kaldırmış durumda)
            else:
                fingers.append(0)  # with the finger down (Parmağı aşağı kaldırmış durumda)
                
        totalF = fingers.count(1)  # Calculating the number of fingers removed (Kaldırılan parmak sayısını hesaplama)
    
    # Printing the number of fingers on the screen (Eldeki parmak sayısını ekrana yazdırma)
    cv2.putText(img, str(totalF), (30, 130), cv2.FONT_HERSHEY_PLAIN, 8, (255, 0, 0), thickness=10)
    
    #  Show the image (Görüntüyü gösterme)
    cv2.imshow("img", img)
    
    # break loop when 'q' keys are pressed ('q' tuşuna basıldığında döngüyü kır)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Releasing camera feed and closing windows (Kamera akışını serbest bırakma ve pencereleri kapatma)
cap.release()
cv2.destroyAllWindows()
