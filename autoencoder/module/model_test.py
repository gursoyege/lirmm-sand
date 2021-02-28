from tensorflow.python import framework
from common.imports import *

def clean():
    if os.path.exists(OUTPUT_PATH):
        if os.path.isfile(OUTPUT_PATH + "train.png"):
            os.remove(OUTPUT_PATH + "train.png")
        if os.path.isfile(OUTPUT_PATH + "test.png"):
            os.remove(OUTPUT_PATH + "test.png")

def run(autoencoder, train_set, test_set, train_cla_n, test_cla_n, r_train, r_test, r_max):
    autoencoder.load_weights(OUTPUT_PATH + "weights.h5")
    plt.rcParams['axes.linewidth'] = 0.1
    

    j=0
    plt.rcParams["figure.figsize"] = (3,25)
    for i in range(test_cla_n):
        j += 1
        plt.subplot(test_cla_n,3,j, frame_on=False)
        imgs = test_set[0,i,:,:,:,:] 
        plt.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        plt.imshow(imgs[0,:,:,0], cmap="gray", vmin=0, vmax=1)

        j += 1
        plt.subplot(test_cla_n,3,j)
        gnds = test_set[1,i,:,:,:,:] 
        plt.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        plt.imshow(gnds[0,:,:,0], cmap="gray", vmin=0, vmax=1)
        
        j += 1
        plt.subplot(test_cla_n,3,j)
        decoded_imgs = autoencoder.predict(imgs*r_test[i,:,:,:])
        plt.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        plt.imshow(decoded_imgs[0,:,:,0], cmap="gray", vmin=0, vmax=1)
        
    plt.savefig(OUTPUT_PATH + "test.png", dpi=850)
    plt.clf()
    plt.close()

    j=0
    plt.rcParams["figure.figsize"] = (3,75)
    for i in range(0,train_cla_n):
        j += 1
        plt.subplot(train_cla_n,3,j)
        imgs = train_set[0,i,:,:,:,:]
        plt.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False) 
        plt.imshow(imgs[0,:,:,0], cmap="gray", vmin=0, vmax=1)
        
        j += 1
        plt.subplot(train_cla_n,3,j)
        gnds = train_set[1,i,:,:,:,:] 
        plt.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        plt.imshow(gnds[0,:,:,0], cmap="gray", vmin=0, vmax=1)

        j += 1
        plt.subplot(train_cla_n,3,j)
        decoded_imgs = autoencoder.predict(imgs*r_train[i,:,:,:])
        plt.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        plt.imshow(decoded_imgs[0,:,:,0], cmap="gray", vmin=0, vmax=1)

    plt.savefig(OUTPUT_PATH + "train.png", dpi=850)
    plt.clf()
    plt.close()