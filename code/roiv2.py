import numpy as np
import cv2
from matplotlib import pyplot as plt
import glob

bBoxThresh = 500

allImages = []

template = cv2.imread("templates/tap_hand.png", cv2.IMREAD_GRAYSCALE)
template=cv2.medianBlur(template,9)

for img in sorted(glob.glob("images/*.png")):
    raw = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    img=cv2.medianBlur(raw,9)
    img2 = img.copy()

    w, h = template.shape[::]
    # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    i = 0
    for meth in methods:
        img = img2.copy()
        method = eval(meth)
        # Apply template Matching
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(img,top_left, bottom_right, 255, 2)
        plt.subplot(6,2,2*i+1),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(6,2,2*i+2),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        i = i + 1
        plt.suptitle(meth)
        mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()
