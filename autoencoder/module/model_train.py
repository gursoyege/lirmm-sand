from common.imports import *

def clean():
    os.remove(OUTPUT_PATH + "weights.h5")
    os.remove(OUTPUT_PATH + "loss.npy")
    os.remove(OUTPUT_PATH + "loss.jpg")

def run(autoencoder, train_set, train_cla_n, train_img_n, r, r_all):
    """Training parameters"""

    batch_size = CLA_PASS * train_cla_n
    step_per_epoch = int(np.ceil(train_img_n*train_cla_n/batch_size))

    """Train loop"""

    loss_epoch = 0
    loss_table = np.zeros(EPOCHS)
    for epoch in range(1,EPOCHS+1):
        cla_iter, img_iter , cla_rang, img_rang = make_epoch(train_set)

        for step in range(step_per_epoch):
            input_batch, ground_batch, r_batch = make_batch(train_set, cla_iter, img_iter, batch_size, r_all)
            input_iter = iter(input_batch)
            ground_iter = iter(ground_batch)
            r_iter = iter(r_batch)

            for i in range(batch_size):
                inputs = next(input_iter)
                grounds = next(ground_iter)
                r_values = next(r_iter)

                if not np.any(inputs): # if input = all zeros
                    break
                
                inputs = np.expand_dims(inputs, axis=0)
                grounds = np.expand_dims(grounds, axis=0)
                r_values = np.expand_dims(r_values, axis=0)

                r.assign(r_values)
                loss_out = autoencoder.train_on_batch(inputs, grounds)
                loss_epoch = loss_epoch + loss_out

        if epoch%1 == 0:
            loss_epoch = loss_epoch/(batch_size*step_per_epoch)
            loss_table[epoch-1] = loss_epoch
            print('Epoch: ', epoch, ' loss: ', loss_epoch)
            loss_epoch = 0
            autoencoder.save_weights(OUTPUT_PATH + "weights.h5")

    np.save(OUTPUT_PATH + "loss.npy", loss_table)

    plt.xlabel("epoch")
    plt.ylabel("loss")
    plt.plot(loss_table)
    plt.savefig(OUTPUT_PATH + "loss.jpg")