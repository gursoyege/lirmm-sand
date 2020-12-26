from common.imports import *
from module import get_data, create_model, model_train, model_test, tree_generator

##Clean
#model_train.clean()
#model_test.clean()
tree_generator.clean()

##Run
tree_generator.run()
img_w, img_h, train_set, test_set, train_cla_n, test_cla_n, train_img_n, r_all, r_max = get_data.run()

##Sum
beg_train = train_set[0:1,:,0:1,:,:,:]
end_train = train_set[1:2,:,0:1,:,:,:]
beg_test = test_set[0:1,:,0:1,:,:,:]
end_test = test_set[1:2,:,0:1,:,:,:]

r_aug = np.expand_dims(r_all[None,:], axis=2)

beg_all = np.concatenate((beg_train, beg_test), axis=1)
end_all = np.concatenate((end_train, end_test), axis=1)

beg_rall = beg_all * r_aug
end_rall = end_all * r_aug

beg_rsum = np.sum(beg_rall, axis=1, keepdims=True)
end_rsum = np.sum(end_rall, axis=1, keepdims=True)

beg_avg = beg_rsum/(beg_rall).shape[1]
end_avg = end_rsum/(end_rall).shape[1]

delta = beg_avg - end_avg
a = delta[0,0,0,:,:,:].shape
np.save(OUTPUT_PATH + "delta.npy", delta[0,0,0,:,:,:])

cv2.imwrite(OUTPUT_PATH + "beg_avg.jpg", (255 * (beg_avg[0,0,0,:,:,:]/r_max)).astype(np.uint8))
cv2.imwrite(OUTPUT_PATH + "end_avg.jpg", (255 * (end_avg[0,0,0,:,:,:]/r_max)).astype(np.uint8))
cv2.imwrite(OUTPUT_PATH + "delta.jpg", (255 * (delta[0,0,0,:,:,:]/r_max)).astype(np.uint8))

train_set[0] = train_set[0:1,:,0:1,:,:,:]
train_set[1] = train_set[1:2,:,0:1,:,:,:]
train_set = train_set[0:2,:,0:1,:,:,:]

test_set[0] = test_set[0:1,:,0:1,:,:,:]
test_set[1] = test_set[1:2,:,0:1,:,:,:]
##

autoencoder, r, r_max = create_model.run(img_w, img_h, r_max, delta)
model_train.run(autoencoder, train_set, train_cla_n, train_img_n, r, r_all)
model_test.run(autoencoder, train_set, test_set, train_cla_n, test_cla_n,r_all, r_max)