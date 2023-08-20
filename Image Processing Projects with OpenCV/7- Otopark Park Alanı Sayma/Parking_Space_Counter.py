# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 11:44:56 2023

This program can be used for a parking management system. It detects and marks vacant parking spaces in a video stream.
It displays the count of marked parking spots and the total number of parking spots on the image.

Bu program, bir otopark yönetim sistemi için kullanılabilir. Video akışında boş park alanlarını tespit eder ve işaretler.
İşaretlenen park alanlarının sayısını ve toplam park alanı sayısını görüntü üzerinde gösterir.

Author: Hasan Emre
"""

# Import necessary libraries
# Gerekli kütüphaneler import ediliyor
import cv2
import pickle
import numpy as np

# Function to check marked parking spaces
# İşaretilmiş park yerlerini kontrol etmek için fonksiyon
def checkParkSpace(imgg):
    spaceCounter = 0  # Initialize a counter to track vacant parking spots  (Boş park alanlarını saymak için sayaç başlatılır)
    
    # For each marked parking spot location
    # İşaretlenmiş her park yeri konumu için
    for pos in posList:
        x, y = pos  # Obtain the corner coordinates of the parking spot
        # Park yeri köşe koordinatları alınır
        
        img_crop = imgg[y: y+ height, x:x + width]  # Crop the image based on the boundaries of the parking spot
        # Görüntü, park yerinin sınırlarına göre kesilir
        
        count = cv2.countNonZero(img_crop)  # Calculate the count of white pixels in the cropped image
        # Kesilmiş görüntüdeki beyaz piksel sayısı hesaplanır
        
        if count < 150:
            color = (0,255,0)  # If the count of white pixels is less than 150, consider it a vacant space (green color)
            # Eğer beyaz piksel sayısı 150'den azsa, boş park alanı olarak kabul edilir (yeşil renk)
            spaceCounter += 1  # Increment the counter for vacant parking spots
            # Boş park alanı sayacı artırılır
        else:
            color = (0,0,255)   # If the count of white pixels is 150 or more, consider it an occupied space (red color)
            # Eğer beyaz piksel sayısı 150 veya daha fazlaysa, dolu park alanı olarak kabul edilir (kırmızı renk)
        
        # Draw rectangles around the boundaries of parking spots
        # Park yeri sınırlarını dikdörtgen içine çizer
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, 2)
        
        # Write the count of white pixels on the parking spot
        # Park yeri üzerine beyaz piksel sayısını yazar
        cv2.putText(img, str(count), (x, y +height- 2),cv2.FONT_HERSHEY_PLAIN, 1, color,1)
    
    # Write the count of vacant parking spots and total parking spots on the image
    # Boş park alanı sayısını ve toplam park alanı sayısını görüntü üzerine yazar
    cv2.putText(img,f"Boş: {spaceCounter}\{len(posList)}", (15,25),cv2.FONT_HERSHEY_PLAIN, 2, (0,0,255), 2)

# Dimensions of parking spots
# Park yeri boyutları
width = 50
height = 30

# Open the video stream
# Video akışını aç
cap = cv2.VideoCapture("video.mp4")

# Load the file containing marked parking spots
# İşaretlenmiş park yerlerini içeren dosyayı yükle
with open("CarParkPos", "rb") as f:
    posList = pickle.load(f)
    
while True:
    success, img = cap.read()  # Read a frame from the video stream
    # Video akışından bir kare oku
    img = cv2.resize(img, (400,800))  # Resize the frame
    # Kare boyutunu yeniden ayarla
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # Convert the image to grayscale
    # Görüntüyü gri tonlamaya çevir
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)  # Apply Gaussian blur to the image for smoothing
    # Görüntüyü Gaussian bulanıklaştırma ile yumuşat
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)  # Apply adaptive thresholding to the image and invert it
    # Görüntüyü eşikle ve tersine çevir
    imgMedian = cv2.medianBlur(imgThreshold, 5)  # Apply median blur to the image for noise reduction
    # Görüntüyü median bulanıklaştırma ile düzenle
    imgDilate = cv2.dilate(imgMedian,np.ones((3,3), np.uint8), iterations=1)  # Dilate the white regions in the image
    # Beyaz bölgeleri genişlet
    
    # Check the parking spots
    # Park alanlarını kontrol et
    checkParkSpace(imgDilate)
    
    cv2.imshow("img", img)  # Display the frame updated with marked parking spots
    # İşaretlenmiş park alanlarıyla güncellenmiş kareyi göster

    if cv2.waitKey(200) & 0xFF == ord("q"):  # Exit the loop if 'q' key is pressed
        # 'q' tuşuna basılırsa döngüyü sonlandır
        break
    
cap.release()  # Release the video stream
# Video akışını serbest bırak
cv2.destroyAllWindows()  # Close windows
# Pencereleri kapat
