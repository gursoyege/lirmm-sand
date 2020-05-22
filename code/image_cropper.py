from imports import *

def clean():
    files = glob.glob(DATA_PATH + "/beg" + "/*.png")
    for f in files:
        os.remove(f)
    files = glob.glob(DATA_PATH + "/end" + "/*.png")
    for f in files:
        os.remove(f)

def run():
    xmlBeg = getXmlNames(XML_PATH + "/beg")
    xmlEnd = getXmlNames(XML_PATH + "/end")

    i = 0
    n = 0
    while i < len(xmlBeg):
        a_b, name_b, pos_b = getXml(xmlBeg[i])
        if i == 0:
            posPrev_b = pos_b
        if posPrev_b != pos_b:
            adjust_e = True
            while n < len(xmlEnd):
                a_e, name_e, pos_e = getXml(xmlEnd[n])
                if adjust_e:
                    posPrev_e = pos_e
                    adjust_e = False
                if posPrev_e != pos_e:
                    n += 1
                    break
                img_e = cv2.imread(IMAGE_PATH + "/" + name_e, cv2.IMREAD_GRAYSCALE)       
                if xmlEnd[n][-11] == "/":
                    filename_e = xmlEnd[n][-10:-4]
                else:
                    filename_e = xmlEnd[n][-11:-4]
                roi_e = img_e[pos_e[1]:pos_e[3], pos_e[0]:pos_e[2]]
                cv2.imwrite(DATA_PATH + "/end/" + filename_e + ".png", roi_e)     
                posPrev_e = pos_e
                n += 1
        img_b = cv2.imread(IMAGE_PATH + "/" + name_b, cv2.IMREAD_GRAYSCALE)
        if xmlBeg[i][-11] == "/":
            filename_b = xmlBeg[i][-10:-4]
        else:
            filename_b = xmlBeg[i][-11:-4]
        roi_b = img_b[pos_b[1]:pos_b[3], pos_b[0]:pos_b[2]]
        cv2.imwrite(DATA_PATH + "/beg/" + filename_b + ".png", roi_b)
        posPrev_b = pos_b
        i += 1
    else:
        n += 1
        adjust_e = True
        while n < len(xmlEnd):
            a_e, name_e, pos_e = getXml(xmlEnd[n])
            if adjust_e:
                posPrev_e = pos_e
                adjust_e = False
            if posPrev_e != pos_e:
                n += 1
                break
            img_e = cv2.imread(IMAGE_PATH + "/" + name_e, cv2.IMREAD_GRAYSCALE)       
            if xmlEnd[n][-11] == "/":
                filename_e = xmlEnd[n][-10:-4]
            else:
                filename_e = xmlEnd[n][-11:-4]
            roi_e = img_e[pos_e[1]:pos_e[3], pos_e[0]:pos_e[2]]
            cv2.imwrite(DATA_PATH + "/end/" + filename_e + ".png", roi_e)     
            posPrev_e = pos_e
            n += 1