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

    return (action, name, [xmin, ymin, xmax, ymax])


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

def begWrite(i_move, i_example, i_xml, annNames, nameImg, ann_path, xml_path):
    action, n_, pos = getXml(ann_path + annNames[i_xml])
    filename = nameGen(False, i_move, i_example)
    writeXml(action, nameImg, pos, filename, xml_path + "/beg")

def endWrite(i_move, i_example, i_xml, annNames, nameImg, ann_path, xml_path):
    action, n_, pos = getXml(ann_path + annNames[i_xml-1])
    filename = nameGen(True, i_move, i_example)
    writeXml(action, nameImg, pos, filename, xml_path + "/end")


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

def contrst(image, alpha):

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

def randomizer(rotate = True, 
                flip_h = True, 
                flip_v = True, 
                zoom = True, 
                translate = True, 
                brightness = True, 
                contrast = True, 
                gaussian = True, 
                salt_pepper = True, 
                poisson = True, 
                speckle = True,
                max_rotate = 150,
                max_zoom = 0.5,
                max_translate = 0.1,
                max_brightness = 50,
                max_contrast = 1,
                max_gauss_mean = 3,
                max_gauss_var = 1,
                max_salt_pepper_ratio = 1,
                max_salt_pepper = 0.05,
                max_poisson_var = 50,
                max_speckle_mean = 2,
                max_speckle_var = 1):
    aug_apply = []
    aug_param = []

    aug_apply.append(np.random.randint(2)==1 and rotate)
    aug_apply.append(np.random.randint(2)==1 and flip_h)
    aug_apply.append(np.random.randint(2)==1 and flip_v)
    aug_apply.append(np.random.randint(3)==1 and zoom)
    aug_apply.append(np.random.randint(3)==1 and translate)
    aug_apply.append(np.random.randint(4)==1 and brightness)
    aug_apply.append(np.random.randint(4)==1 and contrast)
    aug_apply.append(np.random.randint(6)==1 and gaussian)
    aug_apply.append(np.random.randint(6)==1 and salt_pepper)
    aug_apply.append(np.random.randint(6)==1 and poisson)
    aug_apply.append(np.random.randint(10)==1 and speckle)

    aug_param.append(-max_rotate +np.random.random_sample()*2*max_rotate)
    aug_param.append(1 +np.random.random_sample()*max_zoom)
    aug_param.append(-max_translate + np.random.random_sample()*2*max_translate)
    aug_param.append(-max_translate + np.random.random_sample()*2*max_translate)
    aug_param.append(-max_brightness + np.random.random_sample()*2*max_brightness)
    aug_param.append(0.1 + np.random.random_sample()*max_contrast)
    aug_param.append(np.random.random_sample()*max_gauss_mean)
    aug_param.append(np.random.random_sample()*max_gauss_var)
    aug_param.append(np.random.random_sample()*max_salt_pepper_ratio)
    aug_param.append(np.random.random_sample()*max_salt_pepper)
    aug_param.append(np.random.random_sample()*max_poisson_var)
    aug_param.append(np.random.random_sample()*max_speckle_mean)
    aug_param.append(np.random.random_sample()*max_speckle_var)

    return aug_apply, aug_param

def pipeline(image, aug_apply, aug_param):

    img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)

    if aug_apply[0]:
        img = rotate(img, aug_param[0])
    if aug_apply[1]:
        img = flipH(img)
    if aug_apply[2]:
        img = flipV(img)
    if aug_apply[3]:
        img = zoom(img,aug_param[1])
    if aug_apply[4]:
        img = translate(img, aug_param[2], aug_param[3])
    if aug_apply[5]:
        img = bright(img, aug_param[4])
    if aug_apply[6]:
        img = contrst(img, aug_param[5])
    if aug_apply[7]:
        img = gauss(img, aug_param[6], aug_param[7])
    if aug_apply[8]:
        img = saltPep(img, aug_param[8], aug_param[9])
    if aug_apply[9]:
        img = poisson(img, aug_param[10])
    if aug_apply[10]:
        img = speckle(img, aug_param[11], aug_param[12])
    return img
