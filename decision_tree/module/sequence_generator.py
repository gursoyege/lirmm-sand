from common.imports import *

def clean():
    shutil.rmtree(SEQUENCE_PATH)
    shutil.rmtree(TREE_PATH)

def run():
    if not os.path.exists(SEQUENCE_PATH):
        os.makedirs(SEQUENCE_PATH)
    if not os.path.exists(TREE_PATH):
        os.makedirs(TREE_PATH) 

    r_matrix = r_generator(IM_SIZE, U0, V0, FX, FY)

    fI = glob.glob(INIT_PATH + "*")
    fD = glob.glob(DESIR_PATH + "*")

    initImg = cv2.imread(fI[0], cv2.IMREAD_GRAYSCALE)
    initImg = np.expand_dims(initImg, axis=-1)
    initImg = np.divide(initImg,255.0, dtype=np.float32)

    desImg = cv2.imread(fD[0], cv2.IMREAD_GRAYSCALE)
    desImg = np.expand_dims(desImg, axis=-1)
    desImg = np.divide(desImg,255.0, dtype=np.float32)

    rInitImg = img2rimg(initImg, r_matrix)
    rDesImg = img2rimg(desImg, r_matrix)
    
    posX = list(range(1, GRID_SIZE[0]+1))
    posY = list(range(1, GRID_SIZE[1]+1))

    #ae_tap = create_model('tap', MODEL_PATH)
    ae_poke = create_model('poke', MODEL_PATH)

    l = 0
    k = 0
    prev_act = ""
    while l<l_max:
        ds = []
        names = []
        if l == 0:
            images = [fI[0]]
            path = TREE_PATH
        else:
            path = path + "*/"
            images = glob.glob(path + "*.png")

        for enum,img in enumerate(images):
            print(enum)
            split = img.split('/')
            img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
            img = np.expand_dims(img, axis=-1)
            img = img2rimg(img, r_matrix)
            img = np.divide(img,255.0, dtype=np.float32)

            for act in actions:
                for i in posX:
                    for j in posY:
                        loc, roi = img2roi(i, j, act, img, IM_SIZE, GRID_SIZE)
                        
                        roi = np.expand_dims(roi, axis=0)
                        #if act == "tap":
                            #pred = ae_tap.predict(roi)
                        if act == "poke":
                            pred = ae_poke.predict(roi)
                        
                        pred = pred[0,:,:,:]

                        res = roi2img(loc, pred, img)
                        
                        d = dist(res, rDesImg, IM_SIZE)
                        ds.append(d)
                        prev_act = act

                        save_path = TREE_PATH
                        for ind in range(l):
                            s = split[ind+2]
                            save_path = save_path + s + "/"

                        if not os.path.exists(save_path + act + "_" + str(i) + "_" + str(j) + "/"):
                            os.makedirs(save_path + act + "_" + str(i) + "_" + str(j) + "/")
                        
                        res = res*255.0/r_matrix
                        cv2.imwrite(save_path + act + "_" + str(i) + "_" + str(j) + "/" + "img.png" ,res)
                        names.append(save_path + act + "_" + str(i) + "_" + str(j))
                if ds != []:
                    ind = np.argmin(ds)
                    p = names[ind]
                    out_split = p.split('/')[2:]
                    out = ' + '.join(out_split)
                    with open(SEQUENCE_PATH +"sequence.txt", "w") as text:
                        text.write(out)
                    print(out)
            if np.min(ds) < 0:
                ind = np.argmin(ds)
                s = names[ind]

            k += 1
            '''
            if (k % 5) == 0:
                ind = np.argmin(ds)
                p = names[ind]
                tmp_imgloc = glob.glob(p + "/*.png")
                tmp_img = cv2.imread(tmp_imgloc[0], cv2.IMREAD_GRAYSCALE)

                files = glob.glob("root/*/")
                for fs in files:
                    shutil.rmtree(fs)
                
                os.makedirs(tmp_imgloc[0][0:-8])
                cv2.imwrite(tmp_imgloc[0], tmp_img)
                l -= 1 
                break
            '''
        l = l+1