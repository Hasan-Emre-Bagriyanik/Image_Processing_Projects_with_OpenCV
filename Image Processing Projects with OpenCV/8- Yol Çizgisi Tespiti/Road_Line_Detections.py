# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 13:51:37 2023

This program processes a video to detect and draw lanes on the road. 
It utilizes the Canny edge detection and Hough line transformation techniques.

Bu program, bir videoyu işleyerek yoldaki şeritleri tespit eder ve çizer.
Canny kenar tespiti ve Hough çizgi dönüşümü tekniklerini kullanmaktadır.

Author: Hasan Emre
"""

import cv2
import numpy as np

# Define a function to create a mask for a region of interest in the image
# Görüntü içinde ilgi alanını belirlemek için bir fonksiyon tanımla
def region_of_interest(image, vertices):
    mask = np.zeros_like(image)  # Create a black mask with the same dimensions as the image (Görüntüyle aynı boyutlara sahip siyah bir maske oluşturun)
    match_mask_color = 255  # Define the color intensity for the mask to match (Maskenin eşleşeceği renk yoğunluğunu tanımlayın)
    
    cv2.fillPoly(mask, vertices, match_mask_color)  # Fill the mask with white polygons based on the vertices  (Maskeyi köşelere göre beyaz çokgenlerle doldurun)
    masked_image = cv2.bitwise_and(image, mask)  # Apply the mask to the image using bitwise AND operation (Maskeyi görüntüye bit düzeyinde AND işlemini kullanarak uygulayın)
    return masked_image


# Define a function to draw lines on an image
# Görüntü üzerine çizgi çizmek için bir fonksiyon tanımla
def drawLines(image, lines):
    image = np.copy(image)  # Create a copy of the image  (Resmin bir kopyasını oluştur)
    blank_image = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)  # Create a blank black image  (Boş bir siyah görüntü oluştur)
    
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(blank_image, (x1, y1), (x2, y2), (0, 255, 0), thickness=10)  # Draw green lines on the blank image  (Boş görüntünün üzerine yeşil çizgiler çizin)
            
    image = cv2.addWeighted(image, 0.7, blank_image, 1, 0.0)  # Combine the original image and the lines image  (Orijinal görüntüyü ve çizgi görüntüsünü birleştirin)
    return image

# Define a function to process the image and detect lanes
# Görüntüyü işlemek ve şeritleri tespit etmek için bir fonksiyon tanımla
def process(image):
    height, width = img.shape[0], img.shape[1]  # Get the height and width of the image  (Resmin yüksekliğini ve genişliğini alın)
    region_of_interest_vertices = [(width * 0.7, 0), (width, height), (0, height)]  # Define vertices for region of interest  (İlgi alanı için köşeleri tanımlayın)
    
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert the image to grayscale  (Görüntüyü gri tonlamaya dönüştürün)
    canny_img = cv2.Canny(imgGray, 370, 150)  # Apply Canny edge detection  (Canny kenar algılamayı uygula)
    cropped_image = region_of_interest(canny_img, np.array([region_of_interest_vertices], np.int32))  # Apply region of interest mask  (İlgi bölgesi maskesini uygula)
    lines = cv2.HoughLinesP(cropped_image, rho=2, theta=np.pi / 180, threshold=220, lines=np.array([]), minLineLength=150, maxLineGap=5)  # Apply Hough line transformation (Hough çizgi dönüşümünü uygula)
    
    imageWithLines = drawLines(image, lines)  # Draw detected lines on the image  (Görüntü üzerinde tespit edilen çizgileri çizin)
    return imageWithLines

# Open the video stream
# Video akışını aç
cap = cv2.VideoCapture("video1.mp4")  # Open the video file for processing  (Video dosyasını işlenmek üzere açın)

while True:
    success, img = cap.read()  # Read a frame from the video  (Videodan bir kare oku)
    
    if success:
        img = process(img)  # Process the frame to detect and draw lanes  (Şeritleri algılamak ve çizmek için çerçeveyi işleyin)
        cv2.imshow("img", img)  # Display the processed frame  (İşlenen çerçeveyi göster)
        
        if cv2.waitKey(1) & 0xFF == ord("q"):  # Exit the loop if the 'q' key is pressed  
            # 'q' tuşuna basılırsa döngüden çık
            break
    else:
        break
    
cap.release()  # Release the video stream  (Video akışını serbest bırak)
cv2.destroyAllWindows()  # Close windows  (Pencereleri kapat)
