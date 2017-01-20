import cv2
import numpy as np
import glob

#import objects.py
import test_dead_3

"""
Image detector functions

Tasks completed
    Init object
    Capture Image
    Identify different shapes
    Populate data in object and output
"""

img_path = "/home/joseph/scratch/CV/app_vm/data/screenshot.png"
#img_path = "/home/joseph/Pictures/kfmIkJC.png"

img_color = cv2.imread(img_path)
img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
img_canny = cv2.Canny(img_gray,50,200)

#thresh  = cv2.adaptiveThreshold(img_canny,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
#        cv2.THRESH_BINARY, 11,2)

x=np.where(img_canny==255) #find in image where solid line
minLoc = (min(x[1]),min(x[0]))
maxLoc = (max(x[1]),max(x[0]))
cv2.rectangle(img_color,minLoc, maxLoc,(0,0,255),1)

#Next, divide image into grid
#How? Find >1 template, scale, divide
scaledSize = int(round(test_dead_3.find_scale(img_path,"/home/joseph/scratch/CV/app_vm/data/templates/")))

#scaledSize from image isn't exact. Find how many grid spaces fit in a line,
#then overwrite with actual value
yLength = float(maxLoc[0]-minLoc[0])
xLength = float(maxLoc[1]-minLoc[1])
ydiv = int(round(yLength/scaledSize))
xdiv = int(round(xLength/scaledSize))
scaledSize = int(round(yLength/ydiv))

for i in range(1,xdiv):
    cv2.line(img_color,(minLoc[0],minLoc[1]+i*scaledSize),(maxLoc[0],minLoc[1]+i*scaledSize),(0,0,255),1)
for i in range(1,ydiv):
    cv2.line(img_color,(minLoc[0]+i*scaledSize,minLoc[1]),(minLoc[0]+i*scaledSize,maxLoc[1]),(0,0,255),1)

window_name="test"
cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name,400,600)
cv2.imshow(window_name, img_color)
cv2.waitKey(0)
cv2.destroyAllWindows()


"""



templates = []

window_name = "test"
cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name,400,600)
cv2.imshow(window_name, img_gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
for i,item in enumerate(glob.glob("/home/joseph/scratch/CV/app_vm/data/templates/inf_loop_*.png")):
    print item
    templates.append(cv2.imread(item))
    templates[i] = cv2.cvtColor(templates[i], cv2.COLOR_BGR2GRAY)
    templates[i] = cv2.Canny(templates[i],50,200)
    templates[i], temp_contour, hier = cv2.findContours(templates[i],
            cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    w,h = templates[i].shape[::-1]
    print len(temp_contour)
#    for i in contours:
#        for j in temp_contour:
#            res = cv2.matchShapes(i,j,1,0)
#            print "RES is: " + str(res)

#    res = cv2.matchTemplate(img_gray, templates[i], cv2.TM_CCOEFF_NORMED)
    shape_type = int(item.split('/')[-1].split('_')[2])
    res = 0
#    for pt in zip(*loc[::-1]):
#        cv2.rectangle(img_color_temp, pt, (pt[0]+w, pt[1]+h),(0,0,255),2)
    window_name='out_'+item.split('/')[-1]
    cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name,400,600)
    cv2.imshow(window_name, templates[i])
    cv2.waitKey(0)
    cv2.destroyAllWindows()

"""

#cv2.minMaxLoc(x[0])[0:2] #find min and max of 
#cv2.minMaxLoc(x[1])[0:2]

