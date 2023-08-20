# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 2023

This program can be used for a parking lot management system. Used to mark empty parking spaces in the car park using mouse clicks.
The marked parking spaces are stored in a file and these marks are restored when the program is run again.

Bu program, bir otopark yönetim sistemi için kullanılabilir. Fare tıklamalarını kullanarak otoparktaki boş park alanlarını işaretlemek için kullanılır.
İşaretlenen park alanları bir dosyada saklanır ve program yeniden çalıştırıldığında bu işaretlemeler geri yüklenir.

Author: Hasan Emre
"""

# Import necessary libraries
# Gerekli kütüphaneler import ediliyor
import cv2
import pickle   # İşaretlenen konumları saklamak için pickle kullanılır

try:
    # Attempt to open a file containing previously marked parking positions
    # Daha önce işaretlenmiş park yeri pozisyonlarını içeren dosya açılmaya çalışılır
    with open("CarParkPos", "rb") as f:
        posList = pickle.load(f)
except:
    # If the file doesn't exist, create an empty list
    # Eğer böyle bir dosya yoksa, boş bir liste oluşturulur
    posList = []

# Dimensions of parking spot boxes
# Park yeri kutularının boyutları belirlenir
width = 50
height = 30

# Function for mouse click event
# Fare tıklama olayı için gereken işlev
def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:   # When left click is detected  (Sol tıklama algılandığında)
        posList.append((x,y))  # Add a parking spot marker at the clicked location
        # Tıklanan yere bir park yeri işareti eklenir
    
    if events == cv2.EVENT_RBUTTONDOWN:  # When right click is detected (Sağ tıklama algılandığında) 
        for i, pos in enumerate(posList):  # Remove the parking spot marker clicked on
            # Sağa tıklanan park yeri işareti silinir
            x1,y1 = pos
            if x1 < x < x1 + width  and y1 < y < y1 + height:
                posList.pop(i)

    # Save the marked positions in a file
    # İşaretlenen konumlar bir dosyada saklanır
    with open("CarParkPos", "wb") as f:
        pickle.dump(posList, f)

# Main loop
# Ana döngü
while True:
    # Load the first frame and resize it
    # İlk kare yüklenir ve boyutu yeniden ayarlanır
    img = cv2.imread("first_frame.png")
    img = cv2.resize(img, (400,800))
    
    # Draw rectangles over the marked parking spots
    # İşaretlenen park yerlerinin üzerine dikdörtgenler çizilir
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height),(255,0,0), 2)
    
    # Display the image and track mouse click events
    # Resim gösterilir ve fare tıklama olayı izlenir
    cv2.imshow("img", img)
    cv2.setMouseCallback("img", mouseClick)
    
    # Exit the loop when 'q' key is pressed
    # 'q' tuşuna basıldığında döngü sonlandırılır
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
# Close windows
# Pencereler kapatılır
cv2.destroyAllWindows()
