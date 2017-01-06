from matplotlib import pyplot as plt
import cv2

def orb_plot(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(edgeThreshold=1)
    kp = orb.detect(img)
    img_kp = cv2.drawKeypoints(img, kp, None, color=(255,0,0), flags=0)
    plt.imshow(img_kp)
    plt.show()

