import numpy as np
import cv2
from matplotlib import pyplot as plt
import glob

bBoxThresh = 500

allImages = []

template = cv2.imread("templates/tap_hand.png", cv2.IMREAD_GRAYSCALE)
template=cv2.medianBlur(template,1)

for img in sorted(glob.glob("images_test/*.png")):
    raw = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    img=cv2.medianBlur(raw,9)
    img2 = img.copy()

    w, h = template.shape[::]
    # Apply template Matching
    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.5
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::]):
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), 255, 2)
        print(pt)
    cv2.imshow("img",img)
    cv2.waitKey()
