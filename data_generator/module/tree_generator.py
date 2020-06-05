from common.imports import *

def run():
    if not os.path.exists(ANNOTATION_PATH):
        os.makedirs(ANNOTATION_PATH)
    if not os.path.exists(IMAGE_PATH):
        os.makedirs(IMAGE_PATH)
    if not os.path.exists(XML_PATH):
        os.makedirs(XML_PATH + "/beg")
        os.makedirs(XML_PATH + "/end")
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH + "/beg")
        os.makedirs(DATA_PATH + "/end")
    if not os.path.exists(AUGMENT_PATH):
        os.makedirs(AUGMENT_PATH + "/beg")
        os.makedirs(AUGMENT_PATH + "/end")
