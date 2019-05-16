# -*- coding: utf-8 -*-
import sys
sys.path.insert(0,'./src')

import tensorflow as tf
import keras
from keras.models import load_model
from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from model import DeepModel
from detection import TagDetector
from code_creator import CodeCreator
import os
import glob
import zipfile
import shutil
import time

import numpy as np

app = Flask(__name__)
dropzone = Dropzone(app)
# Dropzone settings
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
#app.config['DROPZONE_REDIRECT_VIEW'] = "results"
app.config["CACHE_TYPE"] = "null"
app.config["DROPZONE_DEFAULT_MESSAGE"] = "Koda cevirmek istediginiz fotograflari surukleyin"
# Uploads settings
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/static/uploads'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

def load_keras_model():
    global model
    model = load_model("my_model.h5")

    global graph
    graph = tf.get_default_graph()

def predict(data, locations):
    labels = ['Button' , 'Image' , 'Text' , 'TextInput']
    result = []
    with graph.as_default():
        output = model.predict(np.array(data))
    indis = 0
    idx = 0
    for o in output:
        largest_value = max(o)
        indis = list(o).index(largest_value)
        if(largest_value > 0.6):
            result.append([idx, labels[indis]])
        idx += 1
    result = np.array(result)
    return result, locations

load_keras_model()

@app.route('/', methods=['GET', 'POST'])
def index():
    # list to hold our uploaded image urls
    file_urls = []
    if request.method == 'POST':
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)
            # save the file with to our photos folder
            filename = photos.save(
                file,
                name= file.filename
            )
            # append image urls
            file_urls.append("./static/uploads/" + str(file.filename))
            detector = TagDetector("./static/uploads/" + str(file.filename))
            data, locations = detector.detect_tags()
            result, locations = predict(data,locations)
            code_creator = CodeCreator(locations, result, file.filename.split('.')[0])
            code_creator.create_code()
    else:
        shutil.rmtree("./outputs", ignore_errors=True)
        shutil.rmtree("./static/uploads/", ignore_errors=True)
        os.mkdir("./outputs")
        os.mkdir("./static/uploads/")
    return render_template('index.html')
    
@app.route('/results')
def results():
    html_outputs = glob.glob("./outputs/*.html")
    if len(html_outputs) != 0:
        filename = str(time.strftime("%d%m%Y-%H%M%S")) + ".zip"
        zipf = zipfile.ZipFile(filename,'w', zipfile.ZIP_DEFLATED)

        for o in html_outputs:
            zipf.write(o)

        zipf.close()

        shutil.rmtree("./outputs", ignore_errors=True)
        shutil.rmtree("./static/uploads/", ignore_errors=True)
        os.mkdir("./outputs")
        os.mkdir("./static/uploads/")
        return send_file(filename,
                mimetype = 'zip',
                attachment_filename= filename,
                as_attachment = True, cache_timeout=0)
    
    return ('', 204)