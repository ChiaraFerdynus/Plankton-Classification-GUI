from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense
import numpy as np
from PIL import Image
from skimage import transform
from os import listdir
from os.path import isfile, join
from pathlib import Path
import os
import shutil
from datetime import date

# helper functions
def load_my_model(model_name):
    model = Sequential()
    model.add((Conv2D(32, (3, 3), input_shape=(150, 150, 3))))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))

    model.add((Conv2D(64, (3, 3))))  # doubling the number of filters in each Conv2D layer
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))

    model.add((Conv2D(128, (3, 3))))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))

    model.add((Conv2D(256, (3, 3))))  # , input_shape=(150, 150, 3) ADDED FOR V3
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))

    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='softmax'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    model.load_weights(model_name)
    return model


# load a single image for predictions
def load(filename):
    np_image = Image.open(filename)
    np_image = np.array(np_image).astype('float32')/255
    np_image = transform.resize(np_image, (150, 150, 3))
    np_image = np.expand_dims(np_image, axis=0)
    return np_image


def load_images_from_folder(input_path):    # needs to be input as raw string!
    path = Path(input_path)                 # gets the path to the folder of images
    image_names = [f for f in listdir(path) if isfile(join(path, f))]
    total_images = len(image_names)
    path_names = []                         # list of all paths as path objects --> can use for load(path) function
    for name in image_names:
        con_name = Path(str(path) + '\\' + str(name))
        path_names.append(con_name)
    # now load and store all images
    ready_images = []                       # list of images ready to be "predicted"
    for P in path_names:
        ready_images.append(load(P))
    return image_names, path_names, ready_images


# this will return 1 for nauplii, 0 for non nauplii images (use result from model.predict(np_image))
def predict_binary(prediction):
    prediction = (prediction > 0.04).astype("int32")
    return prediction.sum()


def predict_batch(ready_images, model):      # returns list of predictions according to where in image list
    predictions = []
    for image in ready_images:
        pred = model.predict(image)
        predictions.append(predict_binary(pred))
    return predictions


def store_images(image_names, predictions, path_names, dest_path, dest_folder_name="Sorted Images "+str(date.today())):
    keys = path_names
    values = predictions
    my_dictionary = dict(zip(keys, values))    # returns a dictionary of path names and prediction accordingly
    # default destination folder is created, should NOT be specified explicitly
    if not os.path.exists(dest_path):
        print("The folder could not be found")
        # if dest path is not entered correctly!
    store_folder_name = "Sorted Images " + str(path_names[1]).split("\\")[-2]
    store_folder_name = store_folder_name.replace(" Single Images ", " ")   # changed from "Extracted"
    full_path = dest_path + "\\" + store_folder_name   # default dest folder name in dest path
    raw_path = r'{}'.format(full_path)
    nauplii_path = full_path + "\\" + "Nauplii"
    non_nauplii_path = full_path + "\\" + "Non_Nauplii"
    raw_nauplii = r'{}'.format(nauplii_path)
    raw_non = r'{}'.format(non_nauplii_path)
    if not os.path.exists(raw_path):
        os.makedirs(raw_path)
        os.makedirs(raw_nauplii)
        os.makedirs(raw_non)
    else:
        print("Folders already exist")
    image_number = 0
    for key in my_dictionary:
        if my_dictionary[key] == 1:
            check_path = r'{}'.format(nauplii_path + "\\" + image_names[image_number])
            if not os.path.exists(check_path):
                shutil.copy(key, raw_nauplii)
                print("Image Nauplii copied")
            else:
                print("Image already exists")
            image_number = image_number + 1
        else:
            check_path = r'{}'.format(non_nauplii_path + "\\" + image_names[image_number])
            if not os.path.exists(check_path):
                shutil.copy(key, raw_non)
                print("Image nonNauplii copied")
            else:
                print("Image already exists")
            image_number = image_number + 1






