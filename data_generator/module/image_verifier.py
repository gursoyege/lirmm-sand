from common.imports import *

def run():
    xmlBeg = getXmlNames(XML_PATH + "/beg")
    xmlEnd = getXmlNames(XML_PATH + "/end")

    posMeanBeg = findPosMean(XML_PATH + "/beg")
    posMeanEnd = findPosMean(XML_PATH + "/end")

    posMean = ((posMeanBeg + posMeanEnd)/2).astype(int)

    i = 0
    n = 0
    center = [0,0]
    draw = [0,0,0,0]
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

                center[0] = (pos_e[2] + pos_e[0])/2
                center[1] = (pos_e[3] + pos_e[1])/2

                draw[0] = center[0] - posMean[0]/2
                draw[2] = center[0] + posMean[0]/2

                draw[1] = center[1] - posMean[1]/2
                draw[3] = center[1] + posMean[1]/2

                cv2.rectangle(img_e, (int(draw[0]),int(draw[1])), (int(draw[2]),int(draw[3])),255)
                cv2.imshow("img_end", img_e)
                cv2.waitKey()
                posPrev_e = pos_e
                n += 1
        img_b = cv2.imread(IMAGE_PATH + "/" + name_b, cv2.IMREAD_GRAYSCALE)

        center[0] = (pos_b[2] + pos_b[0])/2
        center[1] = (pos_b[3] + pos_b[1])/2

        draw[0] = center[0] - posMean[0]/2
        draw[2] = center[0] + posMean[0]/2

        draw[1] = center[1] - posMean[1]/2
        draw[3] = center[1] + posMean[1]/2

        cv2.rectangle(img_b, (int(draw[0]),int(draw[1])), (int(draw[2]),int(draw[3])),255)
        cv2.imshow("img_begin", img_b)
        cv2.waitKey()
        posPrev_b = pos_b
        i += 1
    else: # lazy but at least works
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

            center[0] = (pos_e[2] + pos_e[0])/2
            center[1] = (pos_e[3] + pos_e[1])/2

            draw[0] = center[0] - posMean[0]/2
            draw[2] = center[0] + posMean[0]/2

            draw[1] = center[1] - posMean[1]/2
            draw[3] = center[1] + posMean[1]/2

            cv2.rectangle(img_e, (int(draw[0]),int(draw[1])), (int(draw[2]),int(draw[3])),255)
            cv2.imshow("img_end", img_e)
            cv2.waitKey()
            posPrev_e = pos_e
            n += 1
