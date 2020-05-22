import numpy as np
import cv2
from skimage.measure import compare_ssim
import glob

bBoxThresh = 500

allImages = []

for img in sorted(glob.glob("images/*.png")):
    n = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    allImages.append(n)

for n in range (0, (len(allImages)),2):
    image1Raw =  allImages[n]
    image2Raw =  allImages[n+1]

    image1=cv2.medianBlur(image1Raw,9)
    image2=cv2.medianBlur(image2Raw,9)



    # Compute SSIM between two images
    score, diff = compare_ssim(image1, image2, full=True)
    print("Similarity score : ", score)
    
    # Convert [0,1] diff to [0,255]
    diff = (diff * 255).astype("uint8")
    diff = image1-image2
    cv2.imshow('diff',diff)
    cv2.waitKey(0)
    sum = cv2.addWeighted(image1,0.5,image2,0.5,0)

    # Segmentation
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # obtain the regions of the two input images that differ
    src,contours,hrc = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    mask = np.zeros(image1.shape, dtype='uint8')

    mask = cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB)
    sum = cv2.cvtColor(sum,cv2.COLOR_GRAY2RGB)

    for c in contours:
        area = cv2.contourArea(c)
        if area > bBoxThresh:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(sum, (x, y), (x + w, y + h), (36,255,12), 2)
            cv2.drawContours(mask, [c], 0, (0,255,0), -1)

    sum = cv2.addWeighted(sum,0.9,mask,0.1,0)

    cv2.imshow('sum', sum)
    cv2.waitKey(0)