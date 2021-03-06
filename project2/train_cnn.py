from __future__ import absolute_import

# Keras.
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import sgd

# Peoject files.
from model.cnn_v1 import leNet
from model.alexnet import alexnet_v1
from model.resnet import resnet34, resnet34orig
from project2.exampe_engine import ExampleEngine
from project2.utils.data_utils import RoadImageIterator, DirectoryPatchesIterator
from project2.utils.io_utils import get_road_image_dir


def fitModel_original_data(model, nb_epoch, batch_size, orig_train_img_size, img_width, img_height, stride, title):
    """ Initiate the actual training.

    Parameters
    ----------
    model : keras.model
        Compiled model.

    nb_epoch : int32
        Number of epochs.

    batch_size : in32
        Batch size.

    orig_train_img_size : 2-tuple (int32)
        Size of the original image.

    img_width : int32

    img_height : int32

    stride : 2-tuple

    title : str
    """
    train_generator = ImageDataGenerator(rescale=1.0 / 255)
    valid_generator = ImageDataGenerator(rescale=1.0 / 255)
    
    train_img_iterator = RoadImageIterator(get_road_image_dir('prml2'), train_generator,
                                           data_folder='training',
                                           image_folder='images',
                                           label_folder='groundtruth',
                                           stride=stride,
                                           original_img_size=orig_train_img_size,
                                           target_size=(img_width, img_height),
                                           batch_size=batch_size, # 32
                                           preload=1)
    valid_img_iterator = RoadImageIterator(get_road_image_dir('prml2'), valid_generator,
                                           data_folder='validation',
                                           stride=stride,
                                           original_img_size=orig_train_img_size,
                                           target_size=(img_width, img_height),
                                           batch_size=batch_size,
                                           preload=1)

    engine = ExampleEngine(train_img_iterator, model, validation=valid_img_iterator,
                           load_weight=False, lr_decay=True, title=title,
                           nb_epoch=nb_epoch, samples_per_epoch=200 * batch_size,
                           save_model=True)

    history = engine.fit(batch_size=batch_size, nb_epoch=nb_epoch)

    # engine.plot_result()
    engine.save_history(history, tmp=True)


def run_routine1():
    """
    Routine 1: Baseline training process to obtain a classifier for LeNet structure.
    """

    ### Input parameters.
    img_height = 16
    img_width = 16
    img_channel = 3
    stride = (16, 16)
    original_train_image_size = (400, 400)
    nb_epoch = 200
    batch_size = 32
    # learning_rate = 0.005
    title='LeNet5_50tr50te_bs32_balance'

    ## Train.
    input_shape = (img_channel, img_height, img_width)
    model = leNet(input_shape)
    opt = optimizers.rmsprop()
    # opt = sgd(lr=learning_rate, momentum=0.9, decay=0.0005)
    model.compile(loss='categorical_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])
    fitModel_original_data(model, nb_epoch, batch_size, original_train_image_size, img_width, img_height, stride, title)


def run_routine2():
    """
    Routine 2: Baseline training process to obtain a classifier for AlexNet structure
    """

    ### Input parameters.
    img_height = 16
    img_width = 16
    img_channel = 3
    stride = (16, 16)
    original_train_image_size = (400, 400)
    nb_epoch = 200
    batch_size = 32
    title = 'alex_50tr50va_bs32_noBalance'

    # Train.
    learning_rate = 0.001
    input_shape = (img_channel, img_height, img_width)

    model = alexnet_v1(input_shape)
    # opt = sgd(lr=learning_rate, momentum=0.9, decay=0.0005)
    opt = optimizers.rmsprop()
    model.compile(loss='categorical_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])
    fitModel_original_data(model, nb_epoch, batch_size, original_train_image_size, img_width, img_height, stride, title)

def run_routine3():
    """
    Routine 3: Baseline training process to obtain a classifier for ResNet structure
    """

    ### Input parameters.
    img_height = 16
    img_width = 16
    img_channel = 3
    stride = (16, 16)
    original_train_image_size = (400, 400)
    nb_epoch = 200
    batch_size = 32
    title = 'ResNet34orig_50tr50va_bs32_noBalance'

    # Train.
    learning_rate = 0.005
    input_shape = (img_channel, img_height, img_width)

    model = resnet34orig(input_shape, nb_class=2)
    # opt = sgd(lr=learning_rate, momentum=0.9, decay=0.0005)
    opt = optimizers.rmsprop()
    model.compile(loss='categorical_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])
    fitModel_original_data(model, nb_epoch, batch_size, original_train_image_size, img_width, img_height, stride, title)


if __name__ == '__main__':
    # Only uncomment one:

    # run_routine1()
    # run_routine2()
    run_routine3()