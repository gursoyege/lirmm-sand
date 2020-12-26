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

    deltas = get_delta(MODEL_PATH, ACTIONS)

    rInitImg = img2rimg(initImg, r_matrix)
    rDesImg = img2rimg(desImg, r_matrix)

    ae = create_model(MODEL_PATH, ACTIONS)

    l = 0
    k = 0
    min_dist = 0
    prev_act = ""
    ds = [[] for i in range(l_max)]
    ds_mins = []
    names = [[] for i in range(l_max)]
    while l<l_max:
        if l == 0:
            images = [fI[0]]
            path = TREE_PATH
        else:
            path = path + "*/"
            images = glob.glob(path + "*.png")

        for enum,img in enumerate(images):
            if k%20 == 0:
                print("k = " + str(k)+"/552")
            split = img.split('/')
            img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
            img = np.expand_dims(img, axis=-1)
            img = img2rimg(img, r_matrix)
            img = np.divide(img,255.0, dtype=np.float32)

            for act_e, act in enumerate(ACTIONS):
                center = [0,0]
                centers = []
                annotations = glob.glob(ANNOTATION_PATH + act + "/*.xml")
                for ann in annotations:
                    action, name, loc_curr = getXml(ann)
                    center[0] = int(loc_curr[0] + (loc_curr[2] - loc_curr[0])/2)
                    center[1] = int(loc_curr[1] + (loc_curr[3] - loc_curr[1])/2)
                    centers.append(center.copy())
                
                for cnt in centers:
                    roi_size = np.load(MODEL_PATH + act + "/roi_dims.npy")

                    loc, roi = img2roi(act, img, IM_SIZE, cnt, roi_size)
                    delta = deltas[act_e]

                    m_pre = np.mean(roi)
                    m_delta = np.mean(delta)
                    
                    roi = roi - delta                  
                    roi = np.expand_dims(roi, axis=0)

                    pred = ae[act_e].predict(roi)  
                    pred = pred[0,:,:,:]

                    m_post = np.mean(pred)

                    pred = pred + m_pre - m_post - m_delta

                    res = roi2img(loc, pred, img,BLEND_RATE)

                    d = dist(res, rDesImg, IM_SIZE)
                    ds[l].append(d)
                    prev_act = act
                    

                    save_path = TREE_PATH
                    for ind in range(l):
                        s = split[ind+2]
                        save_path = save_path + s + "/"

                    if not os.path.exists(save_path + act + "_" + str(cnt[0]) + "_" + str(cnt[1]) + "/"):
                        os.makedirs(save_path + act + "_" + str(cnt[0]) + "_" + str(cnt[1]) + "/")
                    
                    res = res*255.0/r_matrix
                    cv2.imwrite(save_path + act + "_" + str(cnt[0]) + "_" + str(cnt[1]) + "/" + "img.png" ,res)
                    names[l].append(save_path + act + "_" + str(cnt[0]) + "_" + str(cnt[1]))
                if ds[l] != [] :
                    ds_mins = []
                    for line in range(l_max):                  
                        if ds[line] != []:
                            ds_mins.append(np.min(ds[line]))
                    min_line = np.argmin(ds_mins)

                    ind = np.argmin(ds[min_line])              
                    
                    p = (names[min_line])[ind]
                    out_split = p.split('/')[2:]
                    out = ' + '.join(out_split)
                    with open(SEQUENCE_PATH +"sequence.txt", "w") as text:
                        text.write(out)
                    if np.min(ds[min_line]) != min_dist :
                        print(out, " : d = ", np.min(ds[min_line]))
                    min_dist = np.min(ds[min_line])

            if np.min(ds[min_line]) < 0:
                ind = np.argmin(ds[min_line])
                s = (names[min_line])[ind]
            k += 1
            '''
            if (k % 10) == 0:
                ind = np.argmin(ds[min_line])
                p = (names[min_line])[ind]
                tmp_imgloc = glob.glob(p + "/*.png")
                tmp_img = cv2.imread(tmp_imgloc[0], cv2.IMREAD_GRAYSCALE)

                files = glob.glob(TREE_PATH)
                for fs in files:
                    shutil.rmtree(fs)
                
                os.makedirs(tmp_imgloc[0][0:-8])
                cv2.imwrite(tmp_imgloc[0], tmp_img)
                l -= 1 
                break
            '''
        if np.argmin(ds_mins) < l:
            min_line = np.argmin(ds_mins)

            ind = np.argmin(ds[min_line])              
            
            p = (names[min_line])[ind]
            out_split = p.split('/')[2:]
            out = ' + '.join(out_split)
            with open(SEQUENCE_PATH +"sequence.txt", "w") as text:
                text.write(out)
            if np.min(ds[min_line]) != min_dist :
                print(out, " : d = ", np.min(ds[min_line]))
            min_dist = np.min(ds[min_line])
        l = l+1