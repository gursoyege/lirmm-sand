import numpy as np
import cv2
from matplotlib import pyplot as plt
import glob

bBoxThresh = 500

allImages = []

template = cv2.imread("templates/tap_hand.png", cv2.IMREAD_GRAYSCALE)
template=cv2.medianBlur(template,1)

for img in sorted(glob.glob("images/*.png")):
    raw = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    img=cv2.medianBlur(raw,9)
    img2 = img.copy()

    w, h = template.shape[::]
    
    res = cv2.matchTemplate(img,template,cv2.TM_CCORR)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(min_val)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(img,top_left, bottom_right, 255, 2)
    cv2.imshow("img",img)
    cv2.waitKey()