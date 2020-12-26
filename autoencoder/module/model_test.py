from common.imports import *

def clean():
    os.remove(OUTPUT_PATH + "train.jpg")
    os.remove(OUTPUT_PATH + "test.jpg")

def run(autoencoder, train_set, test_set, train_cla_n, test_cla_n, r_all, r_max):
    autoencoder.load_weights(OUTPUT_PATH + "weights.h5")
    j=0
    for i in range(test_cla_n):
        j += 1
        plt.subplot(test_cla_n,3,j)
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
        decoded_imgs = autoencoder.predict(imgs*r_all[6+i,:,:,:])
        plt.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        plt.imshow(decoded_imgs[0,:,:,0], cmap="gray", vmin=0, vmax=1)
        
    plt.savefig(OUTPUT_PATH + "test.jpg")
    plt.clf()

    j=0
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
        decoded_imgs = autoencoder.predict(imgs*r_all[i,:,:,:])
        plt.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        plt.imshow(decoded_imgs[0,:,:,0], cmap="gray", vmin=0, vmax=1)

    plt.savefig(OUTPUT_PATH + "train.jpg")
    plt.clf()