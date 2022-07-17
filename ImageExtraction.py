from PIL import Image
import numpy as np
from pathlib import Path
import os
from os import listdir
from os.path import isfile, join


#SH010609_nauplii_2of12
#tif
#r'C:\Users\Chiara Ferdynus\Documents\THESIS\TestJune\SampleImages'

#start_x, start_y, end_x, end_y = extract_images('SH010609_nauplii_2of12', 'tif',
#r'C:/Users/Chiara Ferdynus/Documents/THESIS/TestJune/SampleImages',
#r'C:\Users\Chiara Ferdynus\Documents\THESIS\TestJune\SampleImages')



def extract_images(im_name, im_format, im_path, store_path, save_format='.jpg'):
    image_path = Path(im_path)
    full_im_path = Path(str(image_path) + '\\' + str(im_name) + '.' + str(im_format))
    im = Image.open(full_im_path)

    from_folder_name = im_path.split('/')[-1]
    # then do not have to create folder beforehand
    store_folder = r'{}'.format(store_path + '\\' + 'Single Images ' + from_folder_name)
    if not os.path.exists(store_folder):
        os.makedirs(store_folder)

    # size
    (width, height) = im.size
    print("width: " + str(width) + " height: " + str(height))

    # pixel
    pix = list(im.getdata())  # list of tuples of 3
    pix_vals = np.array(pix).reshape(height, width, 3)  # not sure about height or width

    # pixel in upper left corner: pix_vals[0,0] --> returns array of 3 (RGB)

    # print("First checkpoint")
    # FIND NUMBER OF ROWS AND STARTING OF EACH #
    def num_rows():
        rows = 0
        row_start = [0]
        image_found = False
        col_pixel = 0
        while rows == 0:
            for pixel in range(0, height):
                (R, G, B) = pix_vals[pixel, col_pixel]
                if pixel > 1:
                    (Rp, Gp, Bp) = pix_vals[pixel - 1, col_pixel]
                    if (Rp == 0 and Gp == 0 and Bp == 0) and (R != 0 or G != 0 or B != 0):
                        row_start.append(pixel)
                if (R != 0 or G != 0 or B != 0) and not image_found:
                    image_found = True
                    rows = rows + 1
                elif R == 0 and G == 0 and B == 0 and image_found:
                    image_found = False
            col_pixel = col_pixel + 3
        print("Rows: " + str(rows) + " and start: " + str(row_start))
        return rows, row_start

    # print("second checkpoint")
    # FIND COORDINATES OF EACH INDIVIDUAL IMAGE
    def find_x_y(x, y):
        searching_start_x = True
        searching_end_x = True
        for pixel in range(x, width):
            if searching_start_x:  # searching for x start
                (R, G, B) = pix_vals[y, x]
                if x == width - 1:  # when the end is reached, but no new image is found
                    start_x = width
                    end_x = width
                    searching_start_x = False
                    break
                elif R == 0 and G == 0 and B == 0:
                    x = x + 1
                else:
                    start_x = x
                    searching_start_x = False

            if searching_end_x:
                (R, G, B) = pix_vals[y, x]
                if x == width - 1:
                    end_x = width
                    searching_end_x = False
                elif R == 0 and G == 0 and B == 0 and searching_start_x == False:
                    searching_end_x = False
                else:
                    end_x = x
                    x = x + 1

        searching_start_y = True
        searching_end_y = True
        x = start_x
        for pixel in range(y, height):
            if x == width:
                start_y = y
                end_y = 0
                break
            if searching_start_y:  # searching for y start
                (R, G, B) = pix_vals[y, x]  # x - 1 if original x is used
                if y == height - 1:
                    start_y = height
                    end_y = height
                    break
                elif R == 0 and G == 0 and B == 0:
                    y = y + 1
                else:
                    start_y = y
                    searching_start_y = False

            if searching_end_y:
                (R, G, B) = pix_vals[y, x]  # can use x - 1
                if y == height - 1:
                    start_y = height
                    end_y = height
                    break
                elif R == 0 and G == 0 and B == 0:
                    searching_end_y = False
                else:
                    end_y = y
                    y = y + 1

        return (start_x, start_y, end_x, end_y)

    # print("third checkpoint")
    start_x = 0
    start_y = 0

    image_number = 1  # numerate separate images within the frame

    # find number of rows in the frame, as well as their starting coordinates
    rows, row_start = num_rows()
    # this part also new now, considering that the writing will always start with a "P" (cheating I know)
    if row_start[-1] - row_start[-2] < 15:      # this part deletes the last two entries if it is too small (aka letter)
        row_start.pop(rows)
        row_start.pop(rows-1)
        rows = rows - 1
    # print("checkpoint 4")
    if len(row_start) > 1:      # I think for if it is only one image?
        if row_start[1] - row_start[0] < 5:
            rows = rows + 1
    print("Rows now: " + str(rows) + " and start new: " + str(row_start))
    for each in range(0, rows):     # needs to be from 0 if it fills out full screen
        im_in_row_iteration = 0
        start_y = row_start[each]
        start_x = 0
        while start_x < width:
            box = find_x_y(start_x, start_y)
            # new from here
            #if (box[2] - box[0]) < 15:
            #    print("This is a letter and should hence be skipped")
            #    break
            #else:
            if box[2] < width:
                #if (box[2] - box[0]) < 15:
                #    print("This is a letter and should hence be skipped")
                #    break
                start_x = box[2] + 1  # x to the right, go along row at a time, new start_x is old end_x
                start_y = box[1]  # y should always be the top of the row, shouldn't change
                print(box)
                snip = im.crop(box)
                saver = store_folder + '\\' + im_name + '_' + str(image_number) + save_format
                snip.save(saver)
                # snip.show()
            else:
                print("----- Row " + str(each) + " done -----")
                break
            im_in_row_iteration = im_in_row_iteration + 1
            image_number = image_number + 1


def extract_multiple_frames(frames_format, folder_path, store_path, save_format='.jpg'):
    path = Path(folder_path)
    frame_names = [f for f in listdir(path) if isfile(join(path, f))]
    total_frames = len(frame_names)
    cut = len(frames_format) + 1
    frame_names_only = []  # only frame names without extension
    for frame in frame_names:
        frame_names_only.append(frame[:-cut])
    for each in frame_names_only:
        extract_images(each, frames_format, folder_path, store_path, save_format)
        print('Frame ' + each + ' done')


#extract_images('SH010609_nauplii_2of12', 'tif', r'C:/Users/Chiara Ferdynus/Documents/THESIS/TestJune/SampleImages',
#               r'C:\Users\Chiara Ferdynus\Documents\THESIS\TestJune')

