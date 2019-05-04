
import numpy as np
import cv2

camera = cv2.VideoCapture(0)
img = camera.read(0)[1]
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img = cv2.medianBlur(img, 5)
cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20,
                            param1=100, param2=15, minRadius=1, maxRadius=20)

circles = np.uint16(np.around(circles))

centers = list()
for circle_num, i in enumerate(circles[0,:]):
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]), i[2], (0, 255, 0), 2)

    # draw the center of the circle
    if np.all(cimg[i[1], i[0]] / 100 > 1.5):
        cv2.circle(cimg,(i[0],i[1]), 2, (0, 0, 255), 3)
    else:
        print('{}'.format(circle_num), end = '\n')
        cv2.circle(cimg,(i[0],i[1]), 2, (255, 0, 0), 3)

    centers.append((i[0], i[1]))

# Sort circle centers by position and annotate with number
centers.sort(key = lambda v: (v[1], v[0]))
for count, i in enumerate(centers):
	cv2.putText(cimg, str(count), (i[0],i[1]),  cv2.FONT_HERSHEY_SIMPLEX, .35, (255, 255, 255), 2)

cv2.imwrite('tmp.jpg', cimg)

