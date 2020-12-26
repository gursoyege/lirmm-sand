from common.imports import *

def run(img_w, img_h, r_max, delta):
    r = K.variable(np.zeros([1,img_w,img_h,1]))
    delta_K = K.constant(delta[0,0,:,:,:,:])
    r_max = K.constant(r_max)
    #K.print_tensor(r, message='r = ')
    input_img = Input(shape=(img_w, img_h, 1),name='input')
    r_input_img = keras.layers.Lambda(lambda x: r * x - delta_K, name='r_input')(input_img)
    x = Conv2D(32, (5, 5), padding='same', name='conv1')(r_input_img)
    x = LeakyReLU(alpha=0.2, name='leaky1')(x)
    x = MaxPooling2D((2, 2), padding='same', name='pool1')(x)
    x = Conv2D(64, (3, 3), padding='same', name='conv2')(x)
    x = LeakyReLU(alpha=0.2, name='leaky2')(x)
    x = MaxPooling2D((2, 2), padding='same', name='pool2')(x)
    x = Conv2D(64, (3, 3), padding='same', name='conv3')(x)
    x = LeakyReLU(alpha=0.2, name='leaky3')(x)
    x = MaxPooling2D((2, 2), padding='same', name='pool3')(x)

    shape = x.shape
    x = Flatten(name='flatten_conv2fc')(x)

    x = Dense(2048, name='fc_encoder')(x)
    x = LeakyReLU(alpha=0.2, name='leaky4')(x)
    #x = Dense(1024, activation='relu', name='fc_latent')(x)
    #x = Dense(4096, activation='relu', name='fc_decoder')(x)

    x = Dense(shape[1]*shape[2]*shape[3], name='map_fc2deconv')(x)
    x = LeakyReLU(alpha=0.2, name='leaky5')(x)
    x = Reshape((shape[1],shape[2],shape[3]), name='reshape_fc2deconv')(x)

    x = UpSampling2D((2, 2), name='unpool1')(x)
    x = Conv2DTranspose(64, (3, 3), padding='same', name='deconv1')(x)
    x = LeakyReLU(alpha=0.2, name='leaky6')(x)
    x = UpSampling2D((2, 2), name='unpool2')(x)
    x = Conv2DTranspose(32, (3, 3), padding='same', name='deconv2')(x)
    x = LeakyReLU(alpha=0.2, name='leaky7')(x)
    x = UpSampling2D((2, 2), name='unpool3')(x)
    x = Conv2DTranspose(1, (5, 5), padding='same', name='deconv3')(x)
    x = LeakyReLU(alpha=0.2, name='leaky8')(x)

    unpad_h = np.array([np.ceil((x.shape[1]-img_w)/2), x.shape[1] - np.floor((x.shape[1]-img_w)/2)])
    unpad_v = np.array([np.ceil((x.shape[2]-img_h)/2), x.shape[2] - np.floor((x.shape[2]-img_h)/2)])

    decoded = keras.layers.Lambda(lambda x: x[:,int(unpad_h[0]):int(unpad_h[1]),int(unpad_v[0]):int(unpad_v[1]),:], name='reshape_out')(x)
    
    #decoded = keras.layers.Lambda(lambda x: x[:,0:img_w,0:img_h,:], name='reshape_out')(x)

    autoencoder = Model(input_img, decoded, name='autoencoder')
    autoencoder.compile(optimizer=Adam(lr=0.0002, beta_1=0.5), loss=custom_loss(r,img_w,img_h,r_max))
    autoencoder.summary()
    return(autoencoder, r, r_max)