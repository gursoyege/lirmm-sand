from common.imports import *

def clean():
    folders = glob.glob(AUGMENT_PATH + "/train/beg" + "/*/")
    for f in folders:
        shutil.rmtree(f)
    folders = glob.glob(AUGMENT_PATH + "/train/end" + "/*/")
    for f in folders:
        shutil.rmtree(f)
    folders = glob.glob(AUGMENT_PATH + "/test/beg" + "/*/")
    for f in folders:
        shutil.rmtree(f)
    folders = glob.glob(AUGMENT_PATH + "/test/end" + "/*/")
    for f in folders:
        shutil.rmtree(f)

def run():
    
    folders_beg = sorted(glob.glob(DATA_PATH + "/beg" + "/*"))
    folders_end = sorted(glob.glob(DATA_PATH + "/end" + "/*"))
    data = [[ None for y in range(len(folders_beg))] for x in range(2)]
    
    cla_e = 0
    for folder_e, folder_path_beg in enumerate(folders_beg):
        data[0][folder_e] = (sorted(glob.glob(folder_path_beg + "/*.png")))   
        
        i_slash = folder_path_beg.rfind('/')
        foldername = folder_path_beg[i_slash+1:i_slash+8]
        
        if cla_e < train_test_ratio:
            if not os.path.exists(AUGMENT_PATH + "/train/beg/"+ foldername):
                os.makedirs(AUGMENT_PATH + "/train/beg/"+ foldername, 0o777)
        else:
            if not os.path.exists(AUGMENT_PATH + "/test/beg/"+ foldername):
                os.makedirs(AUGMENT_PATH + "/test/beg/"+ foldername, 0o777)         
        cla_e += 1
    cla_e = 0
    for folder_e, folder_path_end in enumerate(folders_end):
        data[1][folder_e] = (sorted(glob.glob(folder_path_end + "/*.png")))
        
        i_slash = folder_path_end.rfind('/')
        foldername = folder_path_end[i_slash+1:i_slash+8]
        
        if cla_e < train_test_ratio:
            if not os.path.exists(AUGMENT_PATH + "/train/end/"+ foldername):
                os.makedirs(AUGMENT_PATH + "/train/end/"+ foldername, 0o777)
        else:   
            if not os.path.exists(AUGMENT_PATH + "/test/end/"+ foldername):
                os.makedirs(AUGMENT_PATH + "/test/end/"+ foldername, 0o777) 
        cla_e +=1


    cla_e = 0
    img_ebeg = 0
    img_eend = 0
    total_inclass = 0
    sample_nbeg = 1
    sample_nend = 1
    while cla_e < train_test_ratio:
        while total_inclass < nSample: 
            if img_ebeg == len(data[0][cla_e]):
                img_ebeg = 0
                sample_nbeg += 1
            if img_eend == len(data[1][cla_e]):
                img_eend = 0
                sample_nend += 1

            img_beg = data[0][cla_e][img_ebeg]
            img_end = data[1][cla_e][img_eend]

            aug_apply, aug_param = randomizer(rotate = False, 
                                              flip_h = False, 
                                              flip_v = False, 
                                              zoom = False, 
                                              translate = False, 
                                              brightness = False, 
                                              contrast = False, 
                                              gaussian = False, 
                                              salt_pepper = False, 
                                              poisson = False, 
                                              speckle = False,
                                              max_rotate = 150,
                                              max_zoom = 0.5,
                                              max_translate = 0.1,
                                              max_brightness = 50/2,
                                              max_contrast = 1/2,
                                              max_gauss_mean = 3/2,
                                              max_gauss_var = 1/2,
                                              max_salt_pepper_ratio = 1,
                                              max_salt_pepper = 0.05/2,
                                              max_poisson_var = 50/2,
                                              max_speckle_mean = 2/2,
                                              max_speckle_var = 1/2)
            aug_beg = pipeline(img_beg, aug_apply, aug_param)
            aug_end = pipeline(img_end, aug_apply, aug_param)


            i_slash = img_beg.rfind('/')
            i_under = img_beg.rfind('_')
            cv2.imwrite(AUGMENT_PATH + "/train/beg/" + img_beg[i_slash+1:i_under] + "/" + img_beg[i_slash+1:i_under+1] + str(total_inclass) + ".png",aug_beg)

            i_slash = img_end.rfind('/')
            i_under = img_end.rfind('_')
            cv2.imwrite(AUGMENT_PATH + "/train/end/" + img_end[i_slash+1:i_under] + "/" + img_end[i_slash+1:i_under+1] + str(total_inclass) + ".png",aug_end)
        
            img_ebeg += 1
            img_eend += 1
            total_inclass +=1
        else :
            aug_apply, aug_param = randomizer(rotate = False, 
                                              flip_h = False, 
                                              flip_v = False, 
                                              zoom = False, 
                                              translate = False, 
                                              brightness = False, 
                                              contrast = False, 
                                              gaussian = False, 
                                              salt_pepper = False, 
                                              poisson = False, 
                                              speckle = False,
                                              max_rotate = 150,
                                              max_zoom = 0.5,
                                              max_translate = 0.1,
                                              max_brightness = 50/2,
                                              max_contrast = 1/2,
                                              max_gauss_mean = 3/2,
                                              max_gauss_var = 1/2,
                                              max_salt_pepper_ratio = 1,
                                              max_salt_pepper = 0.05/2,
                                              max_poisson_var = 50/2,
                                              max_speckle_mean = 2/2,
                                              max_speckle_var = 1/2)
            aug_beg = pipeline(img_beg, aug_apply, aug_param)
            aug_end = pipeline(img_end, aug_apply, aug_param)

            i_slash = img_beg.rfind('/')
            i_under = img_beg.rfind('_')
            cv2.imwrite(AUGMENT_PATH + "/train/beg/" + img_beg[i_slash+1:i_under] + "/" + img_beg[i_slash+1:i_under+1] + "0.png",aug_beg)

            i_slash = img_end.rfind('/')
            i_under = img_end.rfind('_')
            cv2.imwrite(AUGMENT_PATH + "/train/end/" + img_end[i_slash+1:i_under] + "/" + img_end[i_slash+1:i_under+1] + "0.png",aug_end)
        
        sample_nbeg = 1
        sample_nend = 1
        img_ebeg = 0
        img_eend = 0
        total_inclass = 0
        cla_e += 1

    for cla_e in range(train_test_ratio, len(data[0])):
        img_beg = data[0][cla_e][0]
        img_end = data[1][cla_e][0]
        read_beg = cv2.imread(img_beg, cv2.IMREAD_GRAYSCALE)
        read_end = cv2.imread(img_end, cv2.IMREAD_GRAYSCALE)

        i_slash = img_beg.rfind('/')
        i_under = img_beg.rfind('_')
        cv2.imwrite(AUGMENT_PATH + "/test/beg/" + img_beg[i_slash+1:i_under] + "/" + img_beg[i_slash+1:i_under+1] + "0.png",read_beg)
        
        i_slash = img_end.rfind('/')
        i_under = img_end.rfind('_')
        cv2.imwrite(AUGMENT_PATH + "/test/end/" + img_end[i_slash+1:i_under] + "/" + img_end[i_slash+1:i_under+1] + "0.png",read_end)


