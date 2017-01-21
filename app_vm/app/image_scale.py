from __future__ import print_function
import cv2
import glob
import numpy as np
import imutils
import sys

def find_scale(imagePath,templatePaths):
    '''
    Searches the input image using the input templates to find appropriate scale.

    Input: String to image file to find template in
    Input: String to directory containing the template images
           Template images should be of form "inf_loop_[image type 1-5]_[rotation
           type 1-4].png"
    Output: Integer length of one size of the template square

    Loops over the templates in range of best case template to worst case template, 
    then iterates over multiple scales of the input image to find best matching 
    scale. If template is not found, attempts to find next best case template. Once
    template is found, returns the scaled size of the template with best match. 

    Code is adapted from an example of this brute-forcing method by Adrian
    Rosebrock (2015)
    http://www.pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/

    '''
    # load the image, convert it to grayscale, and initialize the
    # bookkeeping variable to keep track of the matched region
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    better_images = [1,5,4,2,3]
    for image_type in better_images:
        # loop template images
        for templatePath in glob.glob(templatePaths+"/inf_loop_"+str(image_type)+"*.png"):
            # load the image, convert it to grayscale, and detect edges
            template = cv2.imread(templatePath)
            template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            template = cv2.Canny(template, 50, 200)
            (tH, tW) = template.shape[:2]
            found = None
            rot_type = templatePath.split('_')[-1].split('.')[0]

            print("\tSearching for images of shape "+str(image_type) + 
                    " rotation " + str(rot_type))
            # loop over the scales of the image
            for scale in np.linspace(0.5, 2, 50)[::-1]:
                print("\tCompleted:\t"+str(round(1-(scale-.5)/(2-.5),3)*100)+"%", end="\r")
                sys.stdout.flush()
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
                result = cv2.matchTemplate(edged, template,
                        cv2.TM_CCOEFF_NORMED)
                (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

                # if we have found a new maximum correlation value, then ipdate
                # the bookkeeping variable
                if found is None or maxVal > found[0]:
                    # ensuring no false positives
                    if maxVal < 0.5:
                        pass
                    else:
                        print("\tFound new max. Template size of " +
                                str(int(round(r*tW)))+ " with accuracy of " +
                                str(round(maxVal,3)))
                        found = (maxVal, maxLoc, r)

            if found is not None:
                print("\tCompleted:\t"+str(100.000)+"%")
                # unpack the bookkeeping variable to retrieve the scale r
                (_, maxLoc, r) = found
                
                # return the scaled template size
                return int(round(tW*r))
