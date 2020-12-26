import numpy as np
import cv2
import glob
import os
import shutil
import tensorflow as tf
import keras
import lxml.etree as ET

from keras.models import Model
from keras.layers import Input, Dense, Conv2D, MaxPooling2D, UpSampling2D, Flatten, Conv2DTranspose, Reshape, LeakyReLU
from keras import backend as K

def getXml(filepath):
    tree = ET.parse(filepath)

    action = tree.findall('./action')[0].text

    name = tree.findall('./name')[0].text

    xmin = int(tree.findall('./bbox/xmin')[0].text)
    ymin = int(tree.findall('./bbox/ymin')[0].text)
    xmax = int(tree.findall('./bbox/xmax')[0].text)
    ymax = int(tree.findall('./bbox/ymax')[0].text)

    return (action, name, [xmin, ymin, xmax, ymax])

def r_generator(IM_SIZE, U0, V0, FX, FY):
    r_matrix = np.zeros((IM_SIZE[1],IM_SIZE[0], 1))
    for y in range(IM_SIZE[1]):
        for x in range(IM_SIZE[0]):
            r_matrix[y,x,0] = np.sqrt(1 + ((x-U0)/FX)**2 + ((y-V0)/FY)**2)
    return r_matrix

def dist(a, b, IM_SIZE):
    return np.sum(np.abs(a-b)/(IM_SIZE[0] * IM_SIZE[1] * 1.568))


def roi2img(loc, pred, image, BLEND_RATE):
    image_temp =  image.copy()
    pred_blend = pred.copy()

    orig_roi = image_temp[int(loc[1]):int(loc[3]),int(loc[0]):int(loc[2]),:]
    sh = orig_roi.shape
    #sh = [sh[0]-1,sh[1]-1]
    if BLEND_RATE != 0:

        blend_pix = int(np.ceil(np.shape(orig_roi)[0]/BLEND_RATE + np.shape(orig_roi)[1]/BLEND_RATE))

        alpha = 1
        beta = 0
        eps = 1/blend_pix
        for i in range(blend_pix):
            alpha = alpha - eps
            beta = beta + eps

            pred_blend[i,i:sh[1]-i,:]           = cv2.addWeighted(orig_roi[i,i:sh[1]-i,:], alpha, pred[i,i:sh[1]-i,:], beta, 0.0)
            pred_blend[1+i:sh[0]-i,sh[1]-1-i,:]   = cv2.addWeighted(orig_roi[1+i:sh[0]-i,sh[1]-1-i,:], alpha, pred[1+i:sh[0]-i,sh[1]-1-i,:], beta, 0.0)
            pred_blend[sh[0]-1-i,i:sh[1]-1-i,:]   = cv2.addWeighted(orig_roi[sh[0]-1-i,i:sh[1]-1-i,:], alpha, pred[sh[0]-1-i,i:sh[1]-1-i,:], beta, 0.0)
            pred_blend[1+i:sh[0]-1-i,i,:]       = cv2.addWeighted(orig_roi[1+i:sh[0]-1-i,i,:], alpha, pred[1+i:sh[0]-1-i,i,:], beta, 0.0)

    image_temp[int(loc[1]):int(loc[3]),int(loc[0]):int(loc[2]),:] = pred_blend

    return image_temp

def img2roi(act, image, IM_SIZE, center, roi_size):

    loc = np.zeros([4])
    loc[0] = center[0] - roi_size[1]/2
    loc[2] = center[0] + roi_size[1]/2

    loc[1] = center[1] - roi_size[0]/2
    loc[3] = center[1] + roi_size[0]/2
    
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
    
    roi = np.zeros([roi_size[1],roi_size[0]])
    roi = image[int(loc[1]):int(loc[3]),int(loc[0]):int(loc[2]),:]
    return loc, roi

def img2rimg(image, r):
    rimg = r * image
    return rimg

def model_template(roi_size):

    img_w = roi_size[0]
    img_h = roi_size[1]
    input_img = Input(shape=(img_w, img_h, 1),name='input')
    r_input_img = keras.layers.Lambda(lambda x: x, name='r_input')(input_img)
    x = Conv2D(32, (5, 5), padding='same', name='conv1')(r_input_img)
    x = LeakyReLU(alpha=0.2, name='leaky1')(x)
    x = MaxPooling2D((2, 2), padding='same', name='pool1')(x)
    x = Conv2D(64, (5, 5), padding='same', name='conv2')(x)
    x = LeakyReLU(alpha=0.2, name='leaky2')(x)
    x = MaxPooling2D((2, 2), padding='same', name='pool2')(x)
    x = Conv2D(128, (3, 3), padding='same', name='conv3')(x)
    x = LeakyReLU(alpha=0.2, name='leaky3')(x)
    x = MaxPooling2D((2, 2), padding='same', name='pool3')(x)
    x = Conv2D(256, (1, 1), padding='same', name='conv4')(x)
    x = LeakyReLU(alpha=0.2, name='leaky4')(x)
    x = MaxPooling2D((2, 2), padding='same', name='pool4')(x)

    shape = x.shape
    x = Flatten(name='flatten_conv2fc')(x)

    x = Dense(4096, activation='relu', name='fc_encoder')(x)
    x = Dense(1024, activation='relu', name='fc_latent')(x)
    x = Dense(4096, activation='relu', name='fc_decoder')(x)

    x = Dense(shape[1]*shape[2]*shape[3], activation='linear', name='map_fc2deconv')(x)
    x = Reshape((shape[1],shape[2],shape[3]), name='reshape_fc2deconv')(x)

    x = UpSampling2D((2, 2), name='unpool1')(x)
    x = Conv2DTranspose(128, (1, 1), activation='relu', padding='same', name='deconv1')(x)
    x = UpSampling2D((2, 2), name='unpool2')(x)
    x = Conv2DTranspose(64, (3, 3), activation='relu', padding='same', name='deconv2')(x)
    x = UpSampling2D((2, 2), name='unpool3')(x)
    x = Conv2DTranspose(32, (5, 5), activation='relu', padding='same', name='deconv3')(x)
    x = UpSampling2D((2, 2), name='unpool4')(x)
    x = Conv2DTranspose(1, (5, 5), activation='relu', padding='same', name='deconv4')(x)

    unpad_h = np.array([np.ceil((x.shape[1]-img_w)/2), x.shape[1] - np.floor((x.shape[1]-img_w)/2)])
    unpad_v = np.array([np.ceil((x.shape[2]-img_h)/2), x.shape[2] - np.floor((x.shape[2]-img_h)/2)])

    decoded = keras.layers.Lambda(lambda x: x[:,int(unpad_h[0]):int(unpad_h[1]),int(unpad_v[0]):int(unpad_v[1]),:], name='reshape_out')(x)

    autoencoder = Model(input_img, decoded, name='autoencoder')
    return autoencoder

def create_model(MODEL_PATH, ACTIONS):
    ae = []
    for i, act in enumerate(ACTIONS):
        roi_size = np.load(MODEL_PATH + act + "/roi_dims.npy")
        ae.append(model_template(roi_size))
        ae[i].load_weights(MODEL_PATH + act + "/weights.h5")
    return ae

'''
def get_delta(MODEL_PATH, ACTIONS):
    deltas = []
    for i, act in enumerate(ACTIONS):
        d = cv2.imread(MODEL_PATH + act + "/delta.jpg", cv2.IMREAD_GRAYSCALE)
        d = np.divide(d,255.0, dtype=np.float32)
        d = np.expand_dims(d, axis=-1)
        deltas.append(d)
    return deltas
'''
def get_delta(MODEL_PATH, ACTIONS):
    deltas = []
    for i, act in enumerate(ACTIONS):
        d = np.load(MODEL_PATH + act + "/delta.npy")
        deltas.append(d)
    return deltas

def normalize_array (input, min, max):
    input += -(np.min(input))
    input /= np.max(input) / (max - min)
    input += min
    return input