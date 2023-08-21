# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 16:24:13 2023
Author: Hasan Emre
"""

import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

# Open the video stream
# Video akışını aç
cap = cv2.VideoCapture("video2.mp4")

# Initialize the FaceMesh detector
# FaceMesh dedektörünü başlat
detector = FaceMeshDetector()

# Create a LivePlot object for visualizing the plot
# Görselleştirmek için LivePlot nesnesi oluştur
plotY = LivePlot(540, 360, [10, 60])

# Define the list of landmarks IDs for specific points on the face
# Yüzdeki belirli noktalar için landmark ID'lerinin listesini tanımla
idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]

# Initialize an empty list to store blink ratio values
# Göz kırpma oranlarını depolamak için boş bir liste oluştur
ratioList = []

# Define a color for drawing circles on the face
# Yüz üzerine daireler çizmek için bir renk tanımla
color = (0, 0, 255)

# Initialize counters for tracking blink and color change
# Göz kırpma ve renk değişimini izlemek için sayaçları başlat
counter = 0
blickCounter = 0

while True:
    success, img = cap.read()
    
    if success:    
        # Detect the face and facial landmarks in the frame
        # Karedeki yüzü ve yüz hatlarını tespit et
        img, faces = detector.findFaceMesh(img, draw=False)
        
        if faces:
            face = faces[0]
            
            # Draw circles on specified landmarks on the face
            # Yüzde belirtilen noktalara daireler çiz
            for id in idList:
                cv2.circle(img, face[id], 5, color, cv2.FILLED)
                
            # Define specific landmarks for calculating blink ratio
            # Göz kırpma oranını hesaplamak için belirli noktaları tanımla
            leftUp = face[159]
            leftDown = face[23]
            leftLeft = face[130]
            leftRight = face[243]
            
            # Calculate vertical and horizontal distances between landmarks
            # Noktalar arasındaki dikey ve yatay uzaklıkları hesapla
            lengthVer, _ = detector.findDistance(leftUp, leftDown)
            lengthHor, _ = detector.findDistance(leftLeft, leftRight)
            
            # Draw lines to visualize the calculated distances
            # Hesaplanan uzaklıkları görselleştirmek için çizgiler çiz
            cv2.line(img, leftUp, leftDown, (0, 255, 0), 3)
            cv2.line(img, leftLeft, leftRight, (0, 255, 0), 3)
        
            # Calculate the blink ratio based on the distances
            # Uzaklıklara dayalı olarak göz kırpma oranını hesapla
            ratio = int((lengthVer / lengthHor) * 100)
            ratioList.append(ratio)
            
            # Keep a running list of last 3 blink ratios for averaging
            # Ortalama hesaplaması için son 3 göz kırpma oranını sakla
            if len(ratioList) > 3:
                ratioList.pop(0)
            
            ratioAvg = sum(ratioList) / len(ratioList)
            print(ratioAvg)
        
            # Determine if a blink is detected and change the color accordingly
            # Bir göz kırpma tespit edilip edilmediğini belirle ve buna göre rengi değiştir
            if ratioAvg < 35 and counter == 0:
                blickCounter += 1
                color = (0, 255, 0)
                counter = 1
                
            if counter != 0:
                counter += 1
                if counter > 10:
                    counter = 0
                    color = (0, 0, 255)
                    
            # Display blink count on the image using cvzone's putTextRect function
            # cvzone'un putTextRect fonksiyonunu kullanarak göz kırpma sayısını görüntüle
            cvzone.putTextRect(img, f"Blink Count: {blickCounter}", (50, 50), colorR=color)
        
            # Update the plot with the current ratio and get the visualized plot image
            # Grafiği güncelle ve görselleştirilmiş grafik görüntüsünü al
            imgPlot = plotY.update(ratioAvg, color)
            img = cv2.resize(img, (640, 360))
            imgStack = cvzone.stackImages([img, imgPlot], 2, 1)

        cv2.imshow("img", imgStack)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        
    else:
        break

# Release the video stream
# Video akışını serbest bırak
cap.release()
cv2.destroyAllWindows()
