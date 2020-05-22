import lxml.etree as ET
import glob

## Defs
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

def nameGen(end, i_move, i_example):
    if end:
        state = "end_"
        i_move -= 1
    else:
        state = "beg_"
    return str(i_move) + state + str(i_example)