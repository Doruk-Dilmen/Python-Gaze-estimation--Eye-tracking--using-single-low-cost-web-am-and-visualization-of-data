import numpy as np
import cv2
import autopy
from matplotlib import pyplot as plt
import pygame

ESCAPE_KEY = 27

k=1
sumx=0
sumy=0
orn=7

cap = cv2.VideoCapture(0)

screen_resolution=(1280,720)
video_resolution=(1280,720)


pygame.init()
screen =pygame.display.set_mode((600,480))

screen_resolution = autopy.screen.size()

eye_x_positions = list()
eye_y_positions = list()

while 1:
    success, image = cap.read()
    image=cv2.flip(image,1)
    roi = image[150:250 , 230:330]
    resized1 = cv2.resize(roi, (200,200), interpolation = cv2.INTER_AREA)
    
    cv2.circle(resized1, (160, 127), 2, (155, 155, 255), 4)
    cv2.circle(resized1, (50, 127), 2, (155, 155, 255), 4)
    
    cv2.imshow("Parça",resized1)
    
    resized1=resized1[80:170 , 50:160] 
    resized = cv2.resize(resized1, (440,360), interpolation = cv2.INTER_AREA)
    rows,cols,_ = resized1.shape
    gray1 = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    eye_blur = cv2.bilateralFilter(gray1,  10, 195,195)
    cv2.imshow("eye_blur",eye_blur)
    img_blur = cv2.Canny(eye_blur,10,30)
    
    cv2.imshow("img_blur",img_blur)
    #img_blur = cv2.Canny(eye_blur,10,51)
    #eye_blur = cv2.bilateralFilter(gray1,  10, 80,95)
    #img_blur = cv2.Canny(eye_blur,10,35)   
    
    
    
    cv2.imshow('Canny', img_blur)
    circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, 0.1, 400, param1=200, param2=10, minRadius=76, maxRadius=84)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv2.circle(resized, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(resized, (i[0], i[1]), 2, (0, 0, 255), 5)
            print(i[0],i[1])
            #pygame.draw.circle(screen, (0,0,255), ((i[0]-64)*17, (i[1]-60)*40), 5)
            #cv2.putText(frame,"Left eye x location = " + str(i[0]) , (20,30), cv2.FONT_HERSHEY_SIMPLEX,0.5, (155, 255, 0), 2)
            #cv2.putText(frame,"Left eye y location = " + str(i[1]) , (20,50), cv2.FONT_HERSHEY_SIMPLEX,0.5, (155, 255, 0), 2)
            if k==orn:
                k=1
                sumx=sumx/orn
                sumx=round(sumx,2)
                sumy=sumy/orn
                sumy=round(sumy,2)
                print("_______\n",sumx,sumy,"\n_______")
                eye_x_p=round((sumx-145),2)
                #eye_y_p=(sumy-62)
                eye_y_p=round((sumy-145),2)
                pygame.draw.circle(screen, (0,0,255), (eye_x_p*4, eye_y_p*9), 5)
                
               
                
                eye_x_positions.append(eye_x_p)
                eye_y_positions.append(eye_y_p)
                
                
            elif k==0:
                pygame.display.update()
                screen.fill((0,0,0))
                sumx=0
                sumy=0
                k=k+1
                
            elif k==1:
                pygame.display.update()
                screen.fill((0,0,0))
                sumx=sumx+i[0]
                sumy=sumy+i[1]
                k=k+1
                
            else:
                sumx=sumx+i[0]
                sumy=sumy+i[1]
                k=k+1
            
            cv2.putText(image, str(i[0]) , (200,30), cv2.FONT_HERSHEY_SIMPLEX,0.5, (155, 255, 0), 2)
            cv2.putText(image, str(i[1]) , (200,50), cv2.FONT_HERSHEY_SIMPLEX,0.5, (155, 255, 0), 2)
    
    
    cv2.putText(image,"Left eye x location = " , (20,30), cv2.FONT_HERSHEY_SIMPLEX,0.5, (155, 255, 0), 2)
    cv2.putText(image,"Left eye y location = " , (20,50), cv2.FONT_HERSHEY_SIMPLEX,0.5, (155, 255, 0), 2)
    cv2.imshow("Eye", resized)
    #cv2.imshow("Roi", resized1)
    
    cv2.imshow("frame", image) 
    key_pressed = cv2.waitKey(1) & 0xff
    if key_pressed == ESCAPE_KEY:
        break


data_all = list(zip(eye_x_positions,eye_y_positions ))
print(data_all)
plt.scatter(eye_x_positions, eye_y_positions ,color="blue")
plt.title("Eye position")
plt.xlabel("X position")
plt.ylabel("Y position")
plt.axis([0, 150, 55, 0])
plt.show()


'''
x_axis_labels = [0,10,20,30,40,50,60,70,80,90,100] 
y_axis_labels = [0,2.5,5,7.5,10,12.5,15,17.5,20]
sns.heatmap(data_all, xticklabels=x_axis_labels, yticklabels=y_axis_labels, cbar=False)
plt.xlabel("X position")
plt.ylabel("Y position")
plt.show()

vid.release()

'''

pygame.display.quit()
cap.release()
cv2.destroyAllWindows()