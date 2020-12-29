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
    nameImg = ""
    state = ''
    i_xml = -1
    i_move = 0
    i_example = 1
    nextShould = -1
    switch = 0
    for i_img, img in enumerate(sorted(glob.glob(IMAGE_PATH+"/*.png"))):
        nameImg = img[-13:-4] + ".png"
        numImg = int(nameImg[5:9])

        if (numImg != nextShould):
            switch += 1
            if state != 'newRecord' or switch == 3:
                i_move += 1
                i_xml += 1
                switch = 1
            i_example = 1
            state = 'switch'

        if state == 'switch':
            if i_img == 0:
                nextShould = numImg
                switch = 0
                state = 'onlyBeg'
            elif i_move % sampleBatch == 1:
                state = 'newRecord'
            elif i_xml == len(annNames):
                state = 'onlyEnd'
            else :
                switch = 0
                state = 'regular'

        if state == 'onlyBeg':
            begWrite(i_move, i_example, i_xml, annNames, nameImg, ANNOTATION_PATH, XML_PATH)
            i_example += 1
        if state == 'onlyEnd':
            endWrite(i_move, i_example, i_xml, annNames, nameImg, ANNOTATION_PATH, XML_PATH)
            i_example += 1
        if state == 'newRecord':
            if switch == 1:
                endWrite(i_move, i_example, i_xml, annNames, nameImg, ANNOTATION_PATH, XML_PATH)
            elif switch == 2 :
                begWrite(i_move, i_example, i_xml, annNames, nameImg, ANNOTATION_PATH, XML_PATH)
            i_example += 1
        if state == 'regular':
            begWrite(i_move, i_example, i_xml, annNames, nameImg, ANNOTATION_PATH, XML_PATH)
            endWrite(i_move, i_example, i_xml, annNames, nameImg, ANNOTATION_PATH, XML_PATH)
            i_example += 1
        nextShould = numImg+1
