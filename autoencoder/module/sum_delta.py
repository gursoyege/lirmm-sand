from common.imports import *

def clean():
    if os.path.exists(OUTPUT_PATH):
        if os.path.isfile(OUTPUT_PATH + "delta.npy"):
            os.remove(OUTPUT_PATH + "delta.npy")
        if os.path.isfile(OUTPUT_PATH + "beg_avg.png"):
            os.remove(OUTPUT_PATH + "beg_avg.png")
        if os.path.isfile(OUTPUT_PATH + "end_avg.png"):
            os.remove(OUTPUT_PATH + "end_avg.png")
        if os.path.isfile(OUTPUT_PATH + "delta.png"):
            os.remove(OUTPUT_PATH + "delta.png")

def run(train_set, test_set, r_train, r_max):
    beg_train = train_set[0:1,:,:,:,:,:]
    end_train = train_set[1:2,:,:,:,:,:]
    
    r_aug = np.expand_dims(r_train[None,:], axis=2)

    beg_rall = beg_train * r_aug
    end_rall = end_train * r_aug

    beg_rsum = np.sum(beg_rall, axis=(1,2), keepdims=True)
    end_rsum = np.sum(end_rall, axis=(1,2), keepdims=True)

    beg_avg = beg_rsum/(beg_rall).shape[1]
    end_avg = end_rsum/(end_rall).shape[1]

    delta = beg_avg - end_avg

    np.save(OUTPUT_PATH + "delta.npy", delta[0,0,0,:,:,:])

    cv2.imwrite(OUTPUT_PATH + "beg_avg.png", (255 * (beg_avg[0,0,0,:,:,:]/r_max)).astype(np.uint8))
    cv2.imwrite(OUTPUT_PATH + "end_avg.png", (255 * (end_avg[0,0,0,:,:,:]/r_max)).astype(np.uint8))
    cv2.imwrite(OUTPUT_PATH + "delta.png", (255 * (delta[0,0,0,:,:,:]/r_max)).astype(np.uint8))

    return delta
