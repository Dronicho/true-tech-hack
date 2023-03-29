#! python

import argparse
import json
from os import listdir
from os.path import isfile, join, exists, isdir, abspath

import numpy as np
import tensorflow as tf
from tensorflow import keras
import tensorflow_hub as hub


IMAGE_DIM = 224 

def load_model(model_path):
    if model_path is None or not exists(model_path):
    	raise ValueError("no model")
    
    model = tf.keras.models.load_model(model_path, custom_objects={'KerasLayer': hub.KerasLayer},compile=False)
    return model


def classify_nd(model, nd_images, predict_args={}):
    
    model_preds = model.predict(nd_images, verbose=0, **predict_args)
    
    categories = ['drawings', 'hentai', 'neutral', 'porn', 'sexy']

    probs = []
    for i, single_preds in enumerate(model_preds):
        single_probs = {}
        for j, pred in enumerate(single_preds):
            single_probs[categories[j]] = float(pred)
        probs.append(single_probs)
    return probs
