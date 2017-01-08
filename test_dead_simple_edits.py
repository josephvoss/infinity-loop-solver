# import the necessary packages
import numpy as np
import imutils
import os
import cv2
from matplotlib import pyplot as plt

imagePath = "/home/joseph/Pictures/kfmIkJC.png"
# load the image, convert it to grayscale, and initialize the
# bookkeeping variable to keep track of the matched region
image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
found = None
for i,item in enumerate(os.listdir("/home/joseph/scratch/CV/templates")):
    # load the image image, convert it to grayscale, and detect edges
    template = cv2.imread("/home/joseph/scratch/CV/templates/"+item)
    print item
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    template = cv2.Canny(template, 50, 200)
    (tH, tW) = template.shape[:2]

    # loop over the scales of the image
    for scale in np.linspace(0.2, 1.0, 10)[::-1]:
        # resize the image according to the scale, and keep track
        # of the ratio of the resizing
        resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
        r = gray.shape[1] / float(resized.shape[1])

        # if the resized image is smaller than the template, then break
        # from the loop
        if resized.shape[0] < tH or resized.shape[1] < tW:
            break

        # detect edges in the resized, grayscale image and apply template
        # matching to find the template in the image
        edged = cv2.Canny(resized, 50, 200)
        result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(result >= threshold) 

        # check to see if the iteration should be visualized
        #if args.get("visualize", False):
        # draw a bounding box around the detected region
        clone = np.dstack([edged, edged, edged])
        for pt in zip(*loc[::-1]):
            cv2.rectangle(image, pt, (pt[0] + tW, pt[1] + tH), (255,0,0), 2)
            print "Found"
        plt.imshow(image)
        plt.show()

        # if we have found a new maximum correlation value, then ipdate
        # the bookkeeping variable
#        if found is None or maxVal > found[0]:
#            found = (maxVal, maxLoc, r)
