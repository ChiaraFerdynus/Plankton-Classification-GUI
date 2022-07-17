# Plankton-Classification-GUI
Plankton Classification GUI based on two underlying models

Required files:
GUI_remakev1.py
  This file contains the GUI framework and when run on its own (with all additional files, libraries and packages downloaded) can be run and execute the classification

predict_Chiara.py
  This file contains the prediction and classification based on alternative model, developed by (??), code was adapted to be included in GUI
  Model Associated: VGG16; Weights: last1.h5
  
ImageExtraction.py
  This file is required to extract single images from a frame of images
  
LoadPredictStore.py
  This file contains the prediction and classification based on model developed for thesis by Chiara
  Weights: modelProperv4.hdf5
