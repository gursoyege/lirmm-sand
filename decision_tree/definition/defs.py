import numpy as np
import cv2
import glob
import os
import shutil
import tensorflow as tf

def r_generator(IM_SIZE, U0, V0, FX, FY):
    r_matrix = np.zeros((IM_SIZE[1],IM_SIZE[0], 1))
    for y in range(IM_SIZE[1]):
        for x in range(IM_SIZE[0]):
            r_matrix[y,x,0] = np.sqrt(1 + ((x-U0)/FX)**2 + ((y-V0)/FY)**2)
    return r_matrix

def dist(a, b, IM_SIZE):
    return np.sum(np.abs(a-b)/(IM_SIZE[0] * IM_SIZE[1] * 1.568))

def roi2img(loc, pred, image):
    image_temp =  image.copy()
    image_temp[int(loc[1]):int(loc[3]),int(loc[0]):int(loc[2]),:] = pred
    return image_temp

def img2roi(i, j, act, image, IM_SIZE, GRID_SIZE):
    if act == 'tap':
        roiSize = (190,199)
         
    if act == 'poke':
        roiSize = (55,52)

    center = np.zeros([2])
    center[0] = IM_SIZE[0]/(GRID_SIZE[0]*2) *(2*i-1)
    center[1] = IM_SIZE[1]/(GRID_SIZE[1]*2) *(2*j-1)

    loc = np.zeros([4])
    loc[0] = center[0] - roiSize[0]/2
    loc[2] = center[0] + roiSize[0]/2

    loc[1] = center[1] - roiSize[1]/2
    loc[3] = center[1] + roiSize[1]/2
    
    while loc[0]<0:
        loc[0] += 1
        loc[2] += 1
    while loc[1]<0:
        loc[1] += 1
        loc[3] += 1
    while loc[2]>IM_SIZE[0]:
        loc[0] -= 1
        loc[2] -= 1
    while loc[3]>IM_SIZE[1]:
        loc[1] -= 1
        loc[3] -= 1
    
    roi = np.zeros([roiSize[1],roiSize[0]])
    roi = image[int(loc[1]):int(loc[3]),int(loc[0]):int(loc[2]),:]
    return loc, roi

def img2rimg(image, r):
    rimg = r * image
    return rimg

def create_model(act, MODEL_PATH):
    md = MODEL_PATH + act
    ae = tf.keras.models.load_model(md)
    return ae