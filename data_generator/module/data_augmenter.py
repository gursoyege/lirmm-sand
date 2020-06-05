from common.imports import *

def clean():
    folders = glob.glob(AUGMENT_PATH + "/beg" + "/*/")
    for f in folders:
        shutil.rmtree(f)
    folders = glob.glob(AUGMENT_PATH + "/end" + "/*/")
    for f in folders:
        shutil.rmtree(f)

def run():
    folders = glob.glob(DATA_PATH + "/beg" + "/*/")
    for folderPath in folders:
        data = glob.glob(folderPath + "/*.png")
        if not os.path.exists(AUGMENT_PATH + "/beg/"+ folderPath[-5:-1]):
            os.makedirs(AUGMENT_PATH + "/beg/"+ folderPath[-5:-1], 0o777)
        for image in data:
            for n in range(nSample):
                aug = pipeline(image)
                if image[-6] == "_":
                    cv2.imwrite(AUGMENT_PATH + "/beg/" + folderPath[-5:-1] + image[-11:-4] + "_" + str(n+1) + ".png",aug)
                else:
                    cv2.imwrite(AUGMENT_PATH + "/beg/" + folderPath[-5:-1] +image[-12:-4] + "_" + str(n+1) + ".png",aug)

    folders = glob.glob(DATA_PATH + "/end" + "/*/")
    for folderPath in folders:
        data = glob.glob(folderPath + "/*.png")
        if not os.path.exists(AUGMENT_PATH + "/end/"+ folderPath[-5:-1]):
            os.makedirs(AUGMENT_PATH + "/end/"+ folderPath[-5:-1], 0o777)
        for image in data:
            for n in range(nSample):
                aug = pipeline(image)
                if image[-6] == "_":
                    cv2.imwrite(AUGMENT_PATH + "/end/" + folderPath[-5:-1] + image[-11:-4] + "_" + str(n+1) + ".png",aug)
                else:
                    cv2.imwrite(AUGMENT_PATH + "/end/" + folderPath[-5:-1] +image[-12:-4] + "_" + str(n+1) + ".png",aug)
