from __future__ import print_function
import cv2
import numpy as np
import glob

import objects
import image_scale

def image_find(img_path, template_path, data_object):
    """
    Image detector functions

    Input: String to image file to find template in
    Input: String to directory containing the template images
           Template images should be of form "inf_loop_[image type 1-5]_[rotation
           type 1-4].png"
    Input: Data_storage object to populate


    Tasks completed
        Init object
        Capture Image
        Identify different shapes
        Populate data in object and output
    """

    #img_path = "/home/joseph/scratch/CV/app_vm/data/screenshot.png"
    #img_path = "/home/joseph/Pictures/kfmIkJC.png"
    #template_path = "/home/joseph/scratch/CV/app_vm/data/templates/"
    print("Beginning image identification process")
    for i in range(80):
        print("-",end='')
    print('')

    img_color = cv2.imread(img_path)
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    img_canny = cv2.Canny(img_gray,50,200)

    ret, thresh = cv2.threshold(img_gray,200,255,cv2.THRESH_BINARY_INV)

    x=np.where(img_canny==255) #find in image where solid line
    minLoc = (min(x[1]),min(x[0]))
    maxLoc = (max(x[1]),max(x[0]))
    cv2.rectangle(img_color,minLoc, maxLoc,(0,0,255),1)

    #Next, divide image into grid
    #How? Find >1 template, scale, divide
    scaledSize = image_scale.find_scale(img_path,template_path)

    #scaledSize from image isn't exact. Find how many grid spaces fit in a line,
    #then overwrite with actual value
    yLength = float(maxLoc[0]-minLoc[0])
    xLength = float(maxLoc[1]-minLoc[1])
    ydiv = int(round(yLength/scaledSize))
    xdiv = int(round(xLength/scaledSize))
    scaledSize = int(round(yLength/ydiv))

    #Size data_object
    data_object.set_size(xdiv,ydiv)

    for i in range(1,xdiv):
        cv2.line(img_color,(minLoc[0],minLoc[1]+i*scaledSize),(maxLoc[0],minLoc[1]+i*scaledSize),(0,0,255),1)
    for i in range(1,ydiv):
        cv2.line(img_color,(minLoc[0]+i*scaledSize,minLoc[1]),(minLoc[0]+i*scaledSize,maxLoc[1]),(0,0,255),1)

    last_point = minLoc
    images = []
    for i in range(0,xdiv):
        for j in range(0,ydiv):
            last_point = (minLoc[0]+scaledSize*j,minLoc[1]+scaledSize*i)
            images.append(thresh[last_point[1]:last_point[1]+scaledSize,
                last_point[0]:last_point[0]+scaledSize])
            k = images[-1]
            total = 0
            total = cv2.sumElems(k)
            val = total[0]/scaledSize**2
            if abs(val - 55) < 5:
                img_type = 1
            elif abs(val - 25) < 3:
                img_type = 2
            elif abs(val - 33) < 3:
                img_type = 3
            elif abs(val - 43) < 3:
                img_type = 4
            elif abs(val - 70) < 3:
                img_type = 5
            elif abs(val) < 1:
                img_type = 0
            else:
                img_type = -1
#            print str(total[0]/scaledSize**2) + ":\t" + str(img_type)
            text_size = cv2.getTextSize(str(img_type),cv2.FONT_HERSHEY_SIMPLEX,2,3)
            x = last_point[0] + scaledSize/2 - text_size[0][0]/2
            y = last_point[1] + scaledSize/2 + text_size[0][1]/2
            cv2.putText(img_color,str(img_type),(x,y), cv2.FONT_HERSHEY_SIMPLEX,2,
                    (0,0,255), 3, bottomLeftOrigin = False)
            data_object.shape_matrix[i][j] = img_type

    window_name="Image Finder"
    cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name,400,600)
    cv2.imshow(window_name, img_color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
