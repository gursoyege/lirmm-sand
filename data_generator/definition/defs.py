import lxml.etree as ET
import glob
import numpy as np
import cv2

''' XML related '''
def getXml(filepath):
    tree = ET.parse(filepath)

    action = tree.findall('./action')[0].text

    name = tree.findall('./name')[0].text

    xmin = int(tree.findall('./bbox/xmin')[0].text)
    ymin = int(tree.findall('./bbox/ymin')[0].text)
    xmax = int(tree.findall('./bbox/xmax')[0].text)
    ymax = int(tree.findall('./bbox/ymax')[0].text)

    return (action,name,[xmin,ymin,xmax,ymax])

def writeXml(action, photo, pos, filename, folderpath):
    xmin, ymin, xmax, ymax = pos
    root = ET.Element("root")

    ET.SubElement(root, "action").text = action
    ET.SubElement(root, "name").text = photo

    bbox = ET.SubElement(root, "bbox")
    ET.SubElement(bbox, "xmin").text = str(xmin)
    ET.SubElement(bbox, "ymin").text = str(ymin)
    ET.SubElement(bbox, "xmax").text = str(xmax)
    ET.SubElement(bbox, "ymax").text = str(ymax)

    tree = ET.ElementTree(root)
    tree.write(folderpath + "/" + filename + ".xml", pretty_print=True)

def getAnnNames(filepath):
    xmlNum = []
    for xml in sorted(glob.glob(filepath+"/*.xml")):
        xmlNum.append("/" + xml[-13:-4] + ".xml")
    return xmlNum

def getXmlNames(filepath):
    xmlNum = []
    for xml in sorted(glob.glob(filepath+"/*.xml")):
        xmlNum.append(xml)
    return xmlNum

def findPosMean(folderpath):
    posMean = np.zeros(2)
    for n, xml in enumerate(sorted(glob.glob(folderpath + "/*.xml")), 1):
        a, name, pos = getXml(xml)
        posMean[0] = posMean[0] + pos[2] - pos[0]
        posMean[1] = posMean[1] + pos[3] - pos[1]
    else:
        return (posMean/n).astype(int)

''' File names '''
def nameGen(end, i_move, i_example):
    if end:
        state = "end_"
        i_move -= 1
    else:
        state = "beg_"
    return str(i_move) + state + str(i_example)

''' Augmentation methods '''
def rotate(image, angle):
  center = tuple(np.array(image.shape[1::-1]) / 2)
  mat = cv2.getRotationMatrix2D(center, angle, 1.0)
  rotated = cv2.warpAffine(image, mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return rotated

def flipH(image):
    flippedH = cv2.flip(image, 1)
    return flippedH

def flipV(image):
    flippedV = cv2.flip(image, 0)
    return flippedV

def zoom(image, scale):
    zoomed = cv2.resize(image,None,fx=scale, fy=scale, interpolation = cv2.INTER_CUBIC)
    row_org,col_org = image.shape
    row_zoom,col_zoom = zoomed.shape
    cropped = zoomed[int(np.floor(row_zoom/2-row_org/2)) : int(np.floor(row_zoom/2+row_org/2)),
                        int(np.floor(col_zoom/2-col_org/2)) : int(np.floor(col_zoom/2+col_org/2))]
    return cropped

def translate(image, scaleH, scaleV):
    row,col = image.shape
    M = np.float32([[1,0,row*scaleH],[0,1,col*scaleV]])
    translated = cv2.warpAffine(image,M,(col,row))
    return translated

def bright(image, beta):
    bright = np.zeros(image.shape, image.dtype)
    bright = cv2.convertScaleAbs(image, beta=beta)
    return bright

def contrast(image, alpha):

    contrast = cv2.convertScaleAbs(image, alpha=alpha)
    return contrast

def gauss(image, mean, var):
    var = var*var
    gauss = np.random.normal(mean,var,image.size)
    gauss = gauss.reshape(image.shape[0],image.shape[1]).astype('uint8')
    gauss = cv2.add(image,gauss)
    return gauss

def saltPep(image, s_vs_p, amount):
  row,col = image.shape
  out = np.copy(image)
  # Salt
  num_salt = np.ceil(amount * image.size * s_vs_p)
  coords = [np.random.randint(0, i - 1, int(num_salt))
          for i in image.shape]
  out[tuple(coords)] = 1
  # Pepper
  num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
  coords = [np.random.randint(0, i - 1, int(num_pepper))
          for i in image.shape]
  out[tuple(coords)] = 0
  return out

def poisson(image, var):
    poisson = np.random.poisson(var,image.size)
    poisson = poisson.reshape(image.shape[0],image.shape[1]).astype('uint8')
    poisson = cv2.add(image,poisson)
    return poisson

def speckle(image, mean, var):
  row,col = image.shape
  gauss = np.random.normal(mean,var,image.size)
  gauss = gauss.reshape(image.shape[0],image.shape[1]).astype('uint8')
  noisy = image + image * gauss
  return noisy

def pipeline(img_path):
    image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    if np.random.randint(2)==1:
        image = rotate(image, -150 + np.random.ranf()*300)
    if np.random.randint(2)==1:
        image = flipH(image)
    if np.random.randint(2)==1:
        image = flipV(image)
    if np.random.randint(3)==1:
        image = zoom(image, 1 + np.random.ranf()*0.5)
    if np.random.randint(3)==1:
        image = translate(image, -0.1 + np.random.ranf()*0.2, -0.1 + np.random.ranf()*0.2)
    if np.random.randint(4)==1:
        image = bright(image, -50 + np.random.ranf()*100)
    if np.random.randint(4)==1:
        image = contrast(image, 0.1 + np.random.ranf()*1)
    if np.random.randint(6)==1:
        image = gauss(image, np.random.ranf()*3, np.random.ranf()*1)
    if np.random.randint(6)==1:
        image = saltPep(image, np.random.ranf()*1, np.random.ranf()*0.05)
    if np.random.randint(6)==1:
        image = poisson(image, np.random.ranf()*50)
    if np.random.randint(10)==1:
        image = speckle(image, np.random.ranf()*2, np.random.ranf()*1)
    return image
