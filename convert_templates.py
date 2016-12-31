#!/usr/bin/python2
import cv2
import numpy as np

image_color = []
image_gray = []

image_color.append(cv2.imread("/home/joseph/scratch/CV/inf_templates/inf_loop_1.png"))
image_color.append(cv2.imread("/home/joseph/scratch/CV/inf_templates/inf_loop_2c.png"))
image_color.append(cv2.imread("/home/joseph/scratch/CV/inf_templates/inf_loop_2s.png"))
image_color.append(cv2.imread("/home/joseph/scratch/CV/inf_templates/inf_loop_3.png"))
image_color.append(cv2.imread("/home/joseph/scratch/CV/inf_templates/inf_loop_4.png"))

for i in range(0,5):
    image_gray.append(cv2.cvtColor(image_color[i], cv2.COLOR_BGR2GRAY))

image_gray_arr = []

for i in range(0,5):
    image_gray_arr.append([])
    for j in range(0,4):
        rows,cols = image_gray[i].shape
        M = cv2.getRotationMatrix2D((cols/2,rows/2),-90*j,1)
        image_gray_arr[i].append(cv2.warpAffine(image_gray[i],M,(cols,rows)))
        if not ( (i == 2 and j == 2 ) or (i == 2 and j == 3) or (i == 4 and j != 0)): 
            cv2.imwrite("/home/joseph/scratch/CV/templates/inf_loop_"+str(i+1)+"_"+str(j+1)+".png",image_gray_arr[i][j]) 
