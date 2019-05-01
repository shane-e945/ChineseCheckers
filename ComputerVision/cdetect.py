# Python program for Detection of a  
# specific color using OpenCV with Python 
import cv2 
import numpy as np
import pyautogui
import threading
import time, sys

BSIZE = 10 #how many pixels wide is a ball
WIDTH = 0
HEIGHT = 0
VID = 0
# Webcamera no 0 is used to capture the frames 
cap = cv2.VideoCapture(0)



table = [0,
         0, 0,
         0, 0, 0,
         0, 0, 0, 0,
         0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0,
         0, 0, 0, 0,
         0, 0, 0,
         0, 0,
         0
         ]

# x, y
space = 30
srad = int(space/2)
gap = 0
sgap = int(space + gap)

#set to bound the board
y = 0
h = int(17 * space)
x = 0
w = int((9 * sgap) - gap)

pos = [(int(w/2),int(srad)),
       (int((w/2)-(sgap/2)),int(space + srad)),(int((w/2) + (0.5 * sgap)),int(space + srad)),
       (int((w/2) - sgap),int(2*space + srad)),(int((w/2)),int(2*space + srad)),(int((w/2) + (1 * sgap)),int(2*space +srad)),
       (int((w/2) - (1.5 * sgap)),int(3*space + srad)),(int((w/2) - (0.5 * sgap)),int(3*space + srad)),(int((w/2) + (sgap/2)),int(3*space + srad)),(int((w/2) + (1.5 * sgap)),int(3*space + srad)),
       (int((w/2) - (2 * sgap)),int(4*space + srad)),(int((w/2) - (1 * sgap)),int(4*space + srad)),(int((w/2) - (0 * sgap)),int(4*space + srad)),(int((w/2) + (1 * sgap)),int(4*space + srad)),(int((w/2) + (2 * sgap)),int(4*space + srad)),
       (int((w/2) - (2.5 * sgap)),int(5*space + srad)),(int((w/2) - (1.5 * sgap)),int(5*space + srad)),(int((w/2) - (0.5 * sgap)),int(5*space + srad)),(int((w/2) + (0.5 * sgap)),int(5*space + srad)),(int((w/2) + (1.5 * sgap)),int(5*space + srad)),(int((w/2) + (2.5 * sgap)),int(5*space + srad)),
       (int((w/2) - (3 * sgap)),int(6*space + srad)),(int((w/2) - (2 * sgap)),int(6*space + srad)),(int((w/2) - (1 * sgap)),int(6*space + srad)),(int((w/2) - (0 * sgap)),int(6*space + srad)),(int((w/2) + (1 * sgap)),int(6*space + srad)),(int((w/2) + (2 * sgap)),int(6*space + srad)),(int((w/2) + (3 * sgap)),int(6*space + srad)),
       (int((w/2) - (3.5 * sgap)),int(7*space + srad)),(int((w/2) - (2.5 * sgap)),int(7*space + srad)),(int((w/2) - (1.5 * sgap)),int(7*space + srad)),(int((w/2) - (0.5 * sgap)),int(7*space + srad)),(int((w/2) + (0.5 * sgap)),int(7*space + srad)),(int((w/2) + (1.5 * sgap)),int(7*space + srad)),(int((w/2) + (2.5 * sgap)),int(7*space + srad)),(int((w/2) + (3.5 * sgap)),int(7*space + srad)),
       (int((w/2) - (4 * sgap)),int(8*space + srad)),(int((w/2) - (3 * sgap)),int(8*space + srad)),(int((w/2) - (2 * sgap)),int(8*space + srad)),(int((w/2) - (1 * sgap)),int(8*space + srad)),(int((w/2) - (0 * sgap)),int(8*space + srad)),(int((w/2) + (1 * sgap)),int(8*space + srad)),(int((w/2) + (2 * sgap)),int(8*space + srad)),(int((w/2) + (3 * sgap)),int(8*space + srad)),(int((w/2) + (4 * sgap)),int(8*space + srad)),
       (int((w/2) - (3.5 * sgap)),int(9*space + srad)),(int((w/2) - (2.5 * sgap)),int(9*space + srad)),(int((w/2) - (1.5 * sgap)),int(9*space + srad)),(int((w/2) - (0.5 * sgap)),int(9*space + srad)),(int((w/2) + (0.5 * sgap)),int(9*space + srad)),(int((w/2) + (1.5 * sgap)),int(9*space + srad)),(int((w/2) + (2.5 * sgap)),int(9*space + srad)),(int((w/2) + (3.5 * sgap)),int(9*space + srad)),
       (int((w/2) - (3 * sgap)),int(10*space + srad)),(int((w/2) - (2 * sgap)),int(10*space + srad)),(int((w/2) - (1 * sgap)),int(10*space + srad)),(int((w/2) - (0 * sgap)),int(10*space + srad)),(int((w/2) + (1 * sgap)),int(10*space + srad)),(int((w/2) + (2 * sgap)),int(10*space + srad)),(int((w/2) + (3 * sgap)),int(10*space + srad)),
       (int((w/2) - (2.5 * sgap)),int(11*space + srad)),(int((w/2) - (1.5 * sgap)),int(11*space + srad)),(int((w/2) - (0.5 * sgap)),int(11*space + srad)),(int((w/2) + (0.5 * sgap)),int(11*space + srad)),(int((w/2) + (1.5 * sgap)),int(11*space + srad)),(int((w/2) + (2.5 * sgap)),int(11*space + srad)),
       (int((w/2) - (2 * sgap)),int(12*space + srad)),(int((w/2) - (1 * sgap)),int(12*space + srad)),(int((w/2) - (0 * sgap)),int(12*space + srad)),(int((w/2) + (1 * sgap)),int(12*space + srad)),(int((w/2) + (2 * sgap)),int(12*space + srad)),
       (int((w/2) - (1.5 * sgap)),int(13*space + srad)),(int((w/2) - (0.5 * sgap)),int(13*space + srad)),(int((w/2) + (0.5 * sgap)),int(13*space + srad)),(int((w/2) + (1.5 * sgap)),int(13*space + srad)),
       (int((w/2) - (1 * sgap)),int(14*space + srad)),(int((w/2) - (0 * sgap)),int(14*space + srad)),(int((w/2) + (1 * sgap)),int(14*space + srad)),
       (int((w/2) - (0.5 * sgap)),int(15*space + srad)),(int((w/2) + (0.5 * sgap)),int(15*space + srad)),
       (int((w/2) - (0 * sgap)),int(16*space + srad))
       ]

def c_check(): 
    # This drives the program into an infinite loop. 
    # Captures the live stream frame-by-frame 
    rval, frame = cap.read()
    # Converts images from BGR to HSV 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
    lower_g = np.array([20,40,20]) 
    upper_g = np.array([85,255,220]) 
  
    # Here we are defining range of bluecolor in HSV 
    # This creates a mask of blue coloured  
    # objects found in the frame. 
    #maskg = cv2.inRange(hsv, lower_g, upper_g)
    maskg = cv2.inRange(frame, lower_g, upper_g)

    lower_o = np.array([0, 30, 30])
    upper_o = np.array([40, 255, 255])

    #masko = cv2.inRange(hsv, lower_o, upper_o)
    masko = cv2.inRange(frame, lower_o, upper_o)

    pixel = hsv[300, 300]
    print(pixel)
    
 
    # The bitwise and of the frame and mask is done so  
    # that only the blue coloured objects are highlighted  
    # and stored in res
    mask = masko | maskg
    
    #cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    #cv2.imshow('res',res)

    # Create an image that barely fits the board
    #       |  x x x  |
    #       | x x x x |
    #       |x x x x x|
    #       | x x x x |
    #       |  x x x  |

    crop_img = mask[y:y+h, x:x+w]
    c_crop = frame[y:y+h, x:x+w]
       
    cv2.imshow('cropped', crop_img)
    frame_size = cv2.getWindowImageRect('cropped')
    # check first space
    #cv2.circle(c_crop, (int(w/2),int(space/2)), 10, (0,0,255), -1)
    #for j in range(81):
        #cv2.circle(c_crop, pos[j], int(0.9*srad), (0,0,255), -1)
    for i in range(81):
        dot1 = (int(pos[i][1] + (0.2 * space)),pos[i][0])
        dot2 = (int(pos[i][1] - (0.2 * space)),pos[i][0])
        dot3 = (int(pos[i][1] + (0.1 * space)),int(pos[i][0] + (0.1 *space)))
        dot4 = (int(pos[i][1] + (0.1 * space)),int(pos[i][0] - (0.1 *space)))
        dot5 = (int(pos[i][1] - (0.1 * space)),int(pos[i][0] + (0.1 *space)))
        dot6 = (int(pos[i][1] - (0.1 * space)),int(pos[i][0] - (0.1 *space)))
        dot7 = (pos[i][1],int(pos[i][0] + (0.2 *space)))
        dot8 = (pos[i][1],int(pos[i][0] - (0.2 *space)))
        counter = 0
        #try:
        if (crop_img[pos[i][1],pos[i][0]] != 0) or (crop_img[dot1] == 255) or (crop_img[dot2] == 255) or (crop_img[dot3] == 255) or (crop_img[dot4] == 255) or (crop_img[dot5] == 255) or (crop_img[dot6] == 255) or (crop_img[dot7] == 255) or (crop_img[dot8] == 255):
            print("i is: %d" % i)
            print("(%d, %d)" % (pos[i][0],pos[i][1]))
            print("%d is occupied." % i)
            cv2.circle(c_crop, pos[i], int(0.9*srad), (0,0,255), -1)
        else:
            print("Nope %d" % i)
        #except IndexError:
            #print(i)
            #print(pos[i])
##            print(crop_img[pos[i]])
##            print(crop_img[dot1])
##            print(crop_img[dot2])
##            print(crop_img[dot3])
##            print(crop_img[dot4])
##            print(crop_img[dot5])
##            print(crop_img[dot6])
##            print(crop_img[dot7])
##            print(crop_img[dot8])
    cv2.imshow('dot', c_crop)
    if (crop_img[int(space/2),int(w/2)] == 255):
        print("Yes")
    # This displays the frame, mask  
    # and res which we created in 3 separate windows. 

      
def main():
    cv2.namedWindow("Image")
    while(1):
        k = cv2.waitKey(1)
        if (k == 119) or VID:
            c_check()
        elif (k == 113):
            break

    # Destroys all of the HighGUI windows. 
    cv2.destroyAllWindows() 
    # release the captured frame 
    cap.release()

main()
