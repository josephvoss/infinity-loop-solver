#!/usr/bin/python2
import cv2

image1_color = cv2.imread("/home/joseph/Pictures/maxresdefault.jpg") 
image2_color = cv2.imread("/home/joseph/Pictures/kfmIkJC.png")

image1_gray = cv2.cvtColor(image1_color, cv2.COLOR_BGR2GRAY)
image2_gray = cv2.cvtColor(image2_color, cv2.COLOR_BGR2GRAY)

#ret,thresh1 = cv2.threshold(image1_gray,127,255,cv2.THRESH_BINARY)
#ret,thresh2 = cv2.threshold(image2_gray,127,255,cv2.THRESH_BINARY)
#thresh1 = cv2.adaptiveThreshold(image1_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
#thresh2 = cv2.adaptiveThreshold(image2_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
#thresh1 = cv2.adaptiveThreshold(image1_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
#thresh2 = cv2.adaptiveThreshold(image2_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)

blur1 = cv2.GaussianBlur(image1_gray, (5,5), 0)
ret,thresh1 = cv2.threshold(image1_gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

#ret,thresh1 = cv2.threshold(image1_gray,127,255,cv2.THRESH_BINARY)
#ret,thresh2 = cv2.threshold(image2_gray,127,255,cv2.THRESH_BINARY)

cv2.imshow("color", image1_color)
cv2.imshow("gray", thresh1)

cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow("color", image2_color)
cv2.imshow("gray", thresh2)

cv2.waitKey(0)
cv2.destroyAllWindows()
