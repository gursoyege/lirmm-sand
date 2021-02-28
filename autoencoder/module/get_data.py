from common.imports import *

def run():
    img_w, img_h, train_cla_n, test_cla_n, train_img_n, train_set, test_set = get_data(DATA_PATH)
    r_train, r_test = get_r_val(R_PATH, train_cla_n, test_cla_n)
    r_max = np.sqrt(1 + (U0/FX)**2 + (V0/FY)**2)
    np.save(OUTPUT_PATH + "roi_dims.npy", np.array([img_w, img_h]))
    delta = np.zeros((1,1,1,img_w,img_h,1))
    return(img_w, img_h, train_set, test_set, train_cla_n, test_cla_n, train_img_n, r_train, r_test, r_max, delta)

