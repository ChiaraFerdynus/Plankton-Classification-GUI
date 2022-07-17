import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from datetime import date
import ImageExtraction as ie
import LoadPredictStore as lps
from PIL import ImageTk, Image
import predict_Chiara as pred_v2

main_root = Tk()
main_root.title('Nauplii Classifier')
main_root.config(bg='skyblue')
main_root.iconbitmap('octopus.ico')
main_root.geometry("865x600")

# colors
header_bg = '#457B9D'

# create a main frame
main_frame = Frame(main_root)
main_frame.pack(fill=BOTH, expand=TRUE)

# create a canvas
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

# add scroll bar to the canvas
my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

# configure the canvas to have scrollbar
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
#my_canvas.bind_all("<MouseWheel>", lambda e: my_canvas.yview_scroll(-1*(e.delta/120), "units"))

# create another frame inside the canvas
root = Frame(my_canvas)

# add new frame to a window in the canvas
# my_canvas.create_window((0, 0), window=root, anchor="nw")
canvas_frame = my_canvas.create_window((0, 0), window=root, anchor="nw")
"""
# configure root frame and canvas to expand
#root.bind("<Configure>", OnFrameConfigure())
#my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))


def FrameWidth(self, event):    # my_canvas.bind(<configure>, self.FrameWidth)
    canvas_width = event.width
    self.canvas.itemconfig(self.canvas_frame, width=canvas_width)
    
def OnFrameConfigure(self, event):   # root.bind(<configure>, self.OnFrameConfigure)
    self.canvas.configure(scrollregion=my_canvas.bbox("all"))

def _on_mousewheel(self, event):
    self.canvas.yview_scroll(-1*(event.delta/120), "units")
"""

header = Frame(master=root, height=150, width=800, bg=header_bg, bd=10)
header.pack(fill=BOTH, expand=True)
ex_lps_f = Frame(master=root, height=150, width=800, bg='white')
ex_lps_f.pack(fill=BOTH, expand=True)
ex_lps = Frame(ex_lps_f, bg='#CCE5FF', height=110, width=700, bd=10)
ex_lps.pack(fill=BOTH, expand=True, pady=10, padx=10)
ex_lps.grid_columnconfigure(1, weight=1, minsize=110)
ex_lps.grid_rowconfigure((1, 2), weight=1)
im_extractionF_f = Frame(master=root, height=150, width=800, bg='white')
# im_extractionF.grid(row=1, column=0, columnspan=2, sticky=N+E+S+W)
im_extractionF_f.pack(fill=BOTH, expand=True)
im_extractionF = Frame(im_extractionF_f, bg='#CCE5FF', bd=10)
im_extractionF.pack(fill=BOTH, expand=True, padx=10)
im_extractionF.grid_columnconfigure(1, weight=1, minsize=110)    # this makes it expand
im_extractionF.grid_rowconfigure((1, 2, 3), weight=1)
lps_folder_f = Frame(master=root, height=150, width=800, bg='white')   #E5CCFF
# lps_folder.grid(row=2, column=0, columnspan=2, sticky=N+E+S+W)
lps_folder_f.pack(fill=BOTH, expand=True)
lps_folder = Frame(lps_folder_f, bg='#CCE5FF', bd=10)
lps_folder.pack(fill=BOTH, expand=True, pady=10, padx=10)
lps_folder.grid_columnconfigure(1, weight=1, minsize=110)
lps_folder.grid_rowconfigure((1, 2), weight=1)
im_extractionS = Frame(master=root, height=150, width=800, bg='#CCFFCC', bd=5)
# additional box for different model
pred2_f = Frame(master=root, height=150, width=800, bg='white')
pred2_f.pack(fill=BOTH, expand=True)
pred2 = Frame(pred2_f, bg='#CCE5FF', height=110, width=700, bd=10)
pred2.pack(fill=BOTH, expand=True, pady=(0, 10), padx=10)
pred2.grid_columnconfigure(1, weight=1, minsize=110)
pred2.grid_rowconfigure((1, 2), weight=1)

# colours
extr_bg = '#CCE5FF'  # some light blue
bg2 = '#CCE5FF'    # light green, #CCE5FF '#c2ffd9'
browse_bg = '#5c84fa'
submit_fg = '#b30421'
image_format_list = ["tif", "bmp", "jpg", "png"]



""" Functions """
def get_im_name(name_entry, ext_entry, path_entry):
    file_name = filedialog.askopenfilename(title='Select a Single Frame')
    print(file_name)
    extension = str(file_name).split('.')[1]
    part1 = str(file_name).split('.')[0]
    name = part1.split('/')[-1]
    path = '/'.join(part1.split('/')[:-1])
    print(extension)
    print(name)
    print(path)
    name_entry.insert(0, name)
    ext_entry.insert(0, extension)
    path_entry.insert(0, path)


def get_im_path(the_entry, the_text):
    # Allow user to select a directory and store it in global var
    # called folder_path
    # global folder_path
    path_name = filedialog.askdirectory(title=the_text)
    # folder_path.set(filename)
    print(path_name)
    the_entry.insert(0, path_name)


def info1(my_text):
    messagebox.showinfo('Info', my_text)


def load_entries(im_name, im_format, im_path, store_path, save_format):  # I don't think this is being used anymore
    if (im_name and im_format and im_path and store_path) is not None:  # this does not work yet
        im_name = str(im_name)
        im_format = str(im_format)
        im_path = r'{}'.format(im_path)
        store_path = r'{}'.format(store_path)
        save_format = "." + save_format
        ie.extract_images(im_name, im_format, im_path, store_path, save_format)
        messagebox.showinfo('Finished', 'Images have been extracted successfully')
    else:
        messagebox.showerror('Incomplete!', 'All fields must be filled out')    # does not yet work aye


""" Header """
c = Frame(header, bg='white', height=100, width=700, bd=10)
c.pack(fill=BOTH, expand=True)
c.grid_columnconfigure(1, weight=1, minsize=20)
image = Image.open("new_size_uoa.png")
#image = image.resize((200, 65), Image.ANTIALIAS)
# image.save("new_size_uoa.png")
img = ImageTk.PhotoImage(image)
im_label = Label(c, borderwidth=0, image=img)
im_label.grid(row=0, column=0, sticky=W)
text_label = Label(c, text="Nauplii Classifier", bg='white', font='Times 20 bold', width=25).grid(row=0, column=1, sticky=N+E+S+W)
image2 = Image.open("MSS_resize.png")
img2 = ImageTk.PhotoImage(image2)
im2_label = Label(c, borderwidth=0, image=img2).grid(row=0, column=2, sticky=E)

""" Extract, Sort (predict) and Store #1 """
title = Label(ex_lps, bg=extr_bg, text='Extract & Sort Images from Frames', font='Times 11 bold', width=30, anchor=W).grid(row=0, column=0, sticky=W)
in_label_ex_lps = Label(ex_lps, bg=extr_bg, text='Select / enter format of frames').grid(row=3, column=0, sticky=W)
in_path_ex_lps = Label(ex_lps, bg=extr_bg, text='Path to folder of frames').grid(row=1, column=0, sticky=W)
store_path_ex_lps = Label(ex_lps, bg=extr_bg, text='Path to store sorted images').grid(row=2, column=0, sticky=W)
store_format_ex_lps = Label(ex_lps, bg=extr_bg, text='Select / enter format of single images').grid(row=4, column=0, sticky=W)

entry_21 = Entry(master=ex_lps, width=50)   # path to folder of frames
entry_21.grid(row=1, column=1, padx=1, pady=1, sticky=N+E+S+W)
entry_22 = Entry(master=ex_lps, width=50)   # path to store at
entry_22.grid(row=2, column=1, padx=1, pady=1, sticky=N+E+S+W)
entry_23 = ttk.Combobox(master=ex_lps, state='normal', values=image_format_list, width=50)       # format
entry_23.grid(row=3, column=1, padx=1, pady=1, sticky=N+E+S+W)
entry_24 = ttk.Combobox(master=ex_lps, state='normal', values=image_format_list, width=50)    # format
entry_24.grid(row=4, column=1, padx=1, pady=1, sticky=N+E+S+W)

path_folder_button2 = Button(master=ex_lps, text='Browse Folder', width=15, activebackground=browse_bg,
                             command=lambda: get_im_path(entry_21, 'Select Path to folder of frames'))
path_folder_button2.grid(row=1, column=2, padx=3, pady=1, sticky=W)

path_store_button2 = Button(master=ex_lps, text='Browse Folder', width=15, activebackground=browse_bg,
                            command=lambda: get_im_path(entry_22, 'Select Path to store single & sorted images at'))
path_store_button2.grid(row=2, column=2, padx=3, pady=1, sticky=W)


def all_in_one(folder_path, store_path, frame_format, save_format):
    folder_load_entries(folder_path, store_path, frame_format, save_format, False)
    from_folder_name = folder_path.split('/')[-1]
    extraction_folder = '\\' + 'Single Images ' + from_folder_name  # extracted -> single
    ext_path = r'{}'.format(store_path + extraction_folder)     # path where the extracted images will be stored
    print(ext_path)
    load_predict_store_folder(ext_path, store_path, False)
    messagebox.showinfo('Finished', 'Images have been extracted, sorted and stored successfully')
    # need to find way to store and then get folder of that stored thingyy, continute here


# button to extract and sort
ex_lps_folder_button = Button(master=ex_lps, text='Extract, Sort & Store', activeforeground=submit_fg,
                              command=lambda: all_in_one(entry_21.get(), entry_22.get(), entry_23.get(), entry_24.get()))
ex_lps_folder_button.grid(row=5, column=0, pady=1, sticky=W)

info_ex_lps = Button(master=ex_lps, text='Info',
                     command=lambda: info1('This feature allows to extract all single images from a number of image '
                                           'frames, sort the images and store them in folders accordingly\n\n'
                                           '- select the path of the folder containing the frame of images (browse or enter manually)\n'
                                           '- select the path to store the single images (browse or enter manually)\n'
                                           '- enter the format of frames manually'))
info_ex_lps.grid(row=0, column=1, pady=1, sticky=W)

""" Folder Image Extraction #2 """
title = Label(im_extractionF, bg=bg2, text='Extract Single Images from Frames', font='Times 11 bold', width=30, anchor=W).grid(row=0, column=0, sticky=W)
in_label1 = Label(im_extractionF, bg=bg2, text='Select / enter format of frames').grid(row=3, column=0, sticky=W)
in_label2 = Label(im_extractionF, bg=bg2, text='Path to folder of frames').grid(row=1, column=0, sticky=W)
in_label3 = Label(im_extractionF, bg=bg2, text='Path to store extracted images').grid(row=2, column=0, sticky=W)
in_label4 = Label(im_extractionF, bg=bg2, text='Select / enter format of single images').grid(row=4, column=0, sticky=W)

entry_1 = Entry(master=im_extractionF, width=50)    # path of folder
entry_1.grid(row=1, column=1, padx=1, pady=1, sticky=N+E+S+W)
entry_2 = Entry(master=im_extractionF, width=50)    # path to store at
entry_2.grid(row=2, column=1, padx=1, pady=1, sticky=N+E+S+W)
entry_3 = ttk.Combobox(master=im_extractionF, state='normal', values=image_format_list, width=50)     # format
entry_3.grid(row=3, column=1, padx=1, pady=1, sticky=N+E+S+W)
entry_4 = ttk.Combobox(master=im_extractionF, state='normal', values=image_format_list, width=50)      # store format
entry_4.grid(row=4, column=1, padx=1, pady=1, sticky=N+E+S+W)

path_folder_button = Button(master=im_extractionF, text='Browse Folder', width=15, activebackground=browse_bg,
                            command=lambda: get_im_path(entry_1, 'Select Path to folder of frames'))
path_folder_button.grid(row=1, column=2, padx=3, pady=1, sticky=W)

path_store_button1 = Button(master=im_extractionF, text='Browse Folder', width=15, activebackground=browse_bg,
                            command=lambda: get_im_path(entry_2, 'Select Folder to store single images at'))
path_store_button1.grid(row=2, column=2, padx=3, pady=1, sticky=W)


def folder_load_entries(folder_path, store_path, frame_format, save_format, single=True):
    if (frame_format and folder_path and store_path) is not None:
        frame_format = str(frame_format)
        folder_path = r'{}'.format(folder_path)
        store_path = r'{}'.format(store_path)
        save_format = "." + save_format
        ie.extract_multiple_frames(frame_format, folder_path, store_path, save_format)
        print('extracted multiple')
        if single:
            messagebox.showinfo('Finished', 'Images have been extracted and stored successfully')


# button to load the values
extract_buttonF = Button(master=im_extractionF, text='Extract', activeforeground=submit_fg,
                         command=lambda: folder_load_entries(entry_1.get(), entry_2.get(), entry_3.get(), entry_4.get()))
extract_buttonF.grid(row=5, column=0, pady=1, sticky=W)

extrF_info = Button(master=im_extractionF, text='Info',
                    command=lambda: info1('This feature allows to extract single images from multiple frames of images\n\n'
                                          '- select the path of the folder containing the frame of images (browse or enter manually)\n'
                                          '- select the Folder to store the single images (browse or enter manually)\n'
                                          '- enter the format of frames manually'))
extrF_info.grid(row=0, column=1, pady=1, sticky=W)


""" Load, Predict & Store from Folder #3 """
title = Label(lps_folder, bg=extr_bg, text='Sort Single Images', font='Times 11 bold', width=30, anchor=W).grid(row=0, column=0, sticky=W)  #
in_label1 = Label(lps_folder, bg=extr_bg, text='Path to folder of images').grid(row=1, column=0, sticky=W)
in_label2 = Label(lps_folder, bg=extr_bg, text='Path to store sorted images').grid(row=2, column=0, sticky=W)

entry_11 = Entry(master=lps_folder, width=50)
entry_11.grid(row=1, column=1, padx=1, pady=1, sticky=N+E+S+W)
entry_12 = Entry(master=lps_folder, width=50)
entry_12.grid(row=2, column=1, padx=1, pady=1, sticky=N+E+S+W)

path_folder_button2 = Button(master=lps_folder, text='Browse Folder', width=15, activebackground=browse_bg,
                             command=lambda: get_im_path(entry_11, 'Select Path to folder of frames'))
path_folder_button2.grid(row=1, column=2, padx=3, pady=1, sticky=W)

path_store_button2 = Button(master=lps_folder, text='Browse Folder', width=15, activebackground=browse_bg,
                            command=lambda: get_im_path(entry_12, 'Select Path to store sorted images at'))
path_store_button2.grid(row=2, column=2, padx=3, pady=1, sticky=W)


def load_predict_store_folder(folder_path, store_path, single=True):
    if (folder_path and store_path) is not None:
        model = lps.load_my_model('modelProperv4.hdf5')   # here is the model
        folder_path = r'{}'.format(folder_path)
        store_path = r'{}'.format(store_path)
        im_names, path_names, ready_images = lps.load_images_from_folder(folder_path)
        predictions = lps.predict_batch(ready_images, model)
        lps.store_images(im_names, predictions, path_names, store_path)
        if single:
            messagebox.showinfo('Finished', 'Images have been sorted and stored successfully')
    else:
        messagebox.showerror('Incomplete!', 'All fields must be filled out')


# button to load the values
lps_folder_button = Button(master=lps_folder, text='Sort & Store', activeforeground=submit_fg,
                           command=lambda: load_predict_store_folder(entry_11.get(), entry_12.get()))
lps_folder_button.grid(row=3, column=0, pady=1, sticky=W)

lps_info = Button(master=lps_folder, text='Info',
                  command=lambda: info1('This feature allows to sort & store single images (images that are already extracted)\n\n'
                                        '- select the path of the folder containing the frame of images (browse or enter manually)\n'
                                        '- select the path to store the single images (browse or enter manually)'))
lps_info.grid(row=0, column=1, pady=1, sticky=W)


"""Additional prediction to implement model designed by XXX (?)"""
title = Label(pred2, bg=extr_bg, text='Sort Single Images (NanW Algorithm)', font='Times 11 bold', width=30, anchor=W).grid(row=0, column=0, sticky=W)  #
in_label1 = Label(pred2, bg=extr_bg, text='Path to folder of images').grid(row=1, column=0, sticky=W)
in_label2 = Label(pred2, bg=extr_bg, text='Path to store Nauplii').grid(row=2, column=0, sticky=W)
in_label3 = Label(pred2, bg=extr_bg, text='Path to store Non-Nauplii').grid(row=3, column=0, sticky=W)

entry_31 = Entry(master=pred2, width=50)    # sourcepath
entry_31.grid(row=1, column=1, padx=1, pady=1, sticky=N+E+S+W)
entry_32 = Entry(master=pred2, width=50)    # savepath
entry_32.grid(row=2, column=1, padx=1, pady=1, sticky=N+E+S+W)
entry_33 = Entry(master=pred2, width=50)    # savepath_not
entry_33.grid(row=3, column=1, padx=1, pady=1, sticky=N+E+S+W)

sourcepath_button = Button(master=pred2, text='Browse Folder', width=15, activebackground=browse_bg,
                             command=lambda: get_im_path(entry_31, 'Select Path to folder of images to be sorted'))
sourcepath_button.grid(row=1, column=2, padx=3, pady=1, sticky=W)

savepath_button = Button(master=pred2, text='Browse Folder', width=15, activebackground=browse_bg,
                            command=lambda: get_im_path(entry_32, 'Select Path to store Nauplii'))
savepath_button.grid(row=2, column=2, padx=3, pady=1, sticky=W)

savepath_not_button = Button(master=pred2, text='Browse Folder', width=15, activebackground=browse_bg,
                            command=lambda: get_im_path(entry_33, 'Select Path to store Non-Nauplii'))
savepath_not_button.grid(row=3, column=2, padx=3, pady=1, sticky=W)

pred2_info = Button(master=pred2, text='Info',
                    command=lambda: info1('This feature predicts Nauplii / Non-Nauplii based on alterantive algorithm\n\n'
                                        '- select the path of the folder containing a SUBFOLDER of images to be sorted\n'
                                        '- select the path to store the Nauplii and Non-Nauplii at'))
pred2_info.grid(row=0, column=1, pady=1, sticky=W)

# def predict_v2(savepath, savepath_not, sourcepath):   # or take directly from predict_Chiara file

# button to load the values
pred2_button = Button(master=pred2, text='Sort & Store', activeforeground=submit_fg,
                      command=lambda: pred_v2.predict_test2(entry_32.get(), entry_33.get(), entry_31.get()))
pred2_button.grid(row=4, column=0, pady=1, sticky=W)




main_root.mainloop()