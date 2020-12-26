from common.imports import *

def clean():
    files = glob.glob(XML_PATH + "/beg" + "/*.xml")
    for f in files:
        os.remove(f)
    files = glob.glob(XML_PATH + "/end" + "/*.xml")
    for f in files:
        os.remove(f)

def run():
    # Generate
    annNames = getAnnNames(ANNOTATION_PATH)
    for i_img, img in enumerate(sorted(glob.glob(IMAGE_PATH+"/*.png"))):
        nameImg = img[-13:-4] + ".png"
        numImg = int(nameImg[5:9])
        if i_img == 0:
            i_xml = 0
            i_move = 1
            i_example = 1
            nextShould = numImg

        if numImg != nextShould:
            i_move += 1
            i_example = 1
            i_xml += 1

            action, n_, pos = getXml(ANNOTATION_PATH + annNames[i_xml-1])
            filename = nameGen(True, i_move, i_example)
            writeXml(action, nameImg, pos, filename, XML_PATH + "/end")

            if i_xml != len(annNames):
                action, n_, pos = getXml(ANNOTATION_PATH + annNames[i_xml])
                filename = nameGen(False, i_move, i_example)
                writeXml(action, nameImg, pos, filename, XML_PATH + "/beg")
        elif i_move == 1:
            action, n_, pos = getXml(ANNOTATION_PATH + annNames[i_xml])

            filename = nameGen(False, i_move, i_example)
            writeXml(action, nameImg, pos, filename, XML_PATH + "/beg")

            i_example += 1
        elif i_xml == len(annNames):
            action, n_, pos = getXml(ANNOTATION_PATH + annNames[i_xml-1])
            filename = nameGen(True, i_move, i_example)
            writeXml(action, nameImg, pos, filename, XML_PATH + "/end")

            i_example += 1
        else:
            i_example += 1

            action, n_, pos = getXml(ANNOTATION_PATH + annNames[i_xml-1])
            filename = nameGen(True, i_move, i_example)
            writeXml(action, nameImg, pos, filename, XML_PATH + "/end")

            action, n_, pos = getXml(ANNOTATION_PATH + annNames[i_xml])
            filename = nameGen(False, i_move, i_example)
            writeXml(action, nameImg, pos, filename, XML_PATH + "/beg")
        nextShould = numImg+1
