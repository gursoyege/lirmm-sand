from common.imports import *  # Yes this is a bad habit

def clean():
    folders = glob.glob(DATA_PATH + "/beg" + "/*/")
    for f in folders:
        shutil.rmtree(f)
    folders = glob.glob(DATA_PATH + "/end" + "/*/")
    for f in folders:
        shutil.rmtree(f)

def run():
    posMeanBeg = findPosMean(XML_PATH + "/beg")
    posMeanEnd = findPosMean(XML_PATH + "/end")
    posMean = ((posMeanBeg + posMeanEnd)/2).astype(int)

    center = [0,0]
    for n, xml in enumerate(sorted(glob.glob(XML_PATH + "/beg" + "/*.xml")), 1):
        a, name, pos = getXml(xml)

        center[0] = (pos[2] + pos[0])/2
        center[1] = (pos[3] + pos[1])/2

        pos[0] = center[0] - posMean[0]/2
        pos[2] = center[0] + posMean[0]/2

        pos[1] = center[1] - posMean[1]/2
        pos[3] = center[1] + posMean[1]/2

        while pos[0]<0:
            pos[0] += 1
            pos[2] += 1
        while pos[1]<0:
            pos[1] += 1
            pos[3] += 1
        while pos[2]>IM_SIZE[0]:
            pos[0] -= 1
            pos[2] -= 1
        while pos[3]>IM_SIZE[1]:
            pos[1] -= 1
            pos[3] -= 1

        img = cv2.imread(IMAGE_PATH + "/" + name, cv2.IMREAD_GRAYSCALE)
        if xml[-11] == "/":
            filename = xml[-10:-4]
        elif xml[-12] == "/":
            filename = xml[-11:-4]
        elif xml[-13] == "/":
            filename = xml[-12:-4]
        
        if (xml[-12].isdigit() and xml[-11].isdigit()) or (xml[-11].isdigit() and xml[-10].isdigit()) == True:
            foldername = filename[0:5]
        else:
            foldername = filename[0:4]
        
        if not os.path.exists(DATA_PATH + "/beg/"+ foldername):
            os.makedirs(DATA_PATH + "/beg/"+ foldername, 0o777)
        roi = img[int(pos[1]):int(pos[3]), int(pos[0]):int(pos[2])]
        cv2.imwrite(DATA_PATH + "/beg/"+ foldername + "/" + filename +  ".png", roi)

    center = [0,0]
    for n, xml in enumerate(sorted(glob.glob(XML_PATH + "/end" + "/*.xml")), 1):
        a, name, pos = getXml(xml)

        center[0] = (pos[2] + pos[0])/2
        center[1] = (pos[3] + pos[1])/2

        pos[0] = center[0] - posMean[0]/2
        pos[2] = center[0] + posMean[0]/2

        pos[1] = center[1] - posMean[1]/2
        pos[3] = center[1] + posMean[1]/2

        while pos[0]<0:
            pos[0] += 1
            pos[2] += 1
        while pos[1]<0:
            pos[1] += 1
            pos[3] += 1
        while pos[2]>IM_SIZE[0]:
            pos[0] -= 1
            pos[2] -= 1
        while pos[3]>IM_SIZE[1]:
            pos[1] -= 1
            pos[3] -= 1

        img = cv2.imread(IMAGE_PATH + "/" + name, cv2.IMREAD_GRAYSCALE)
        if xml[-11] == "/":
            filename = xml[-10:-4]
        elif xml[-12] == "/":
            filename = xml[-11:-4]
        elif xml[-13] == "/":
            filename = xml[-12:-4]
        
        if (xml[-12].isdigit() and xml[-11].isdigit()) or (xml[-11].isdigit() and xml[-10].isdigit()) == True:
            foldername = filename[0:5]
        else:
            foldername = filename[0:4]
        
        if not os.path.exists(DATA_PATH + "/end/"+ foldername):
            os.makedirs(DATA_PATH + "/end/"+ foldername, 0o777)
        roi = img[int(pos[1]):int(pos[3]), int(pos[0]):int(pos[2])]
        cv2.imwrite(DATA_PATH + "/end/"+ foldername + "/" + filename +  ".png", roi)
