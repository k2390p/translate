#!flask/bin/python

# Author: Ngo Duy Khanh
# Email: ngokhanhit@gmail.com
# Git repository: https://github.com/ngoduykhanh/flask-file-uploader
# This work based on jQuery-File-Upload which can be found at https://github.com/blueimp/jQuery-File-Upload/

import os
# import PIL
# from PIL import Image
import simplejson
import traceback

from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from flask_bootstrap import Bootstrap
from werkzeug import secure_filename

from lib.upload_file import uploadfile

from threading import Thread
from extraction_util import extract_pdf
import config
from pdf2html import pdf2html

import requests
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
DATA_DIR_OUT = os.path.curdir
HTML_DIR_OUT  = os.path.join(DATA_DIR_OUT, 'OUTPUT_FOLDER')
app.config['UPLOAD_FOLDER'] = HTML_DIR_OUT
app.config['THUMBNAIL_FOLDER'] = 'data/thumbnail/'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc', 'docx'])
IGNORED_FILES = set(['.gitignore'])

bootstrap = Bootstrap(app)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def gen_file_name(filename):
    """
    If file was exist already, rename it and return a new name
    """

    i = 1
    while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i += 1

    return filename

#
# def create_thumbnail(image):
#     try:
#         base_width = 80
#         img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], image))
#         w_percent = (base_width / float(img.size[0]))
#         h_size = int((float(img.size[1]) * float(w_percent)))
#         img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)
#         img.save(os.path.join(app.config['THUMBNAIL_FOLDER'], image))
#
#         return True
#
#     except:
#         print(traceback.format_exc())
#         return False


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files['file']
        language = request.form.get('language_select')
        vendor = request.form.get('vendor_select')
        print(language + " #### KSHITIJ #####" + vendor)
        if files:
            filename = secure_filename(files.filename)
            filename = gen_file_name(filename)
            mime_type = files.content_type

            if not allowed_file(files.filename):
                result = uploadfile(name=filename, type=mime_type, size=0, not_allowed_msg="File type not allowed")

            else:
                # save file to disk
                uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                files.save(uploaded_file_path)

                # start translation

                try:
                    Thread(target=pdf2html, args=(language, vendor, uploaded_file_path,app.config['UPLOAD_FOLDER'], filename, 2)).start()
                except Exception as e:
                    print(e)
                # # create thumbnail after saving
                # if mime_type.startswith('image'):
                #     create_thumbnail(filename)
                #
                # get file size after saving
                size = os.path.getsize(uploaded_file_path)

                # return json for js call back
                result = uploadfile(name=filename, type=mime_type, size=size)
            print('done')
            return simplejson.dumps({"files": [result.get_file()]})

    if request.method == 'GET':
        # get all file in ./data directory
        files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'],f)) and f not in IGNORED_FILES ]
        
        file_display = []

        for f in files:
            size = os.path.getsize(os.path.join(app.config['UPLOAD_FOLDER'], f))
            file_saved = uploadfile(name=f, size=size)
            file_display.append(file_saved.get_file())

        return simplejson.dumps({"files": file_display})

    return redirect(url_for('index'))


@app.route("/delete/<string:filename>", methods=['DELETE'])
def delete(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_thumb_path = os.path.join(app.config['THUMBNAIL_FOLDER'], filename)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)

            if os.path.exists(file_thumb_path):
                os.remove(file_thumb_path)
            
            return simplejson.dumps({filename: 'True'})
        except:
            return simplejson.dumps({filename: 'False'})


# serve static files
@app.route("/thumbnail/<string:filename>", methods=['GET'])
def get_thumbnail(filename):
    return send_from_directory(app.config['THUMBNAIL_FOLDER'], filename=filename)


@app.route("/data/<string:filename>", methods=['GET'])
def get_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER']), filename=filename)


@app.route("/compare", methods=['GET'])
def compare():
    url = "http://localhost:8000/api/service/compare"
    text1 = '''1. The board of directors, the board of supervisors
     and the directors, supervisors and senior management of the company
      ensure that the contents of the annual report are true, accurate and complete. 
 There are no false records, misleading statements or major omissions, and
  individual and joint legal responsibilities.'''

    text2 = '''1. The Board of Directors of the Company, the audit committee and the directors,
     senior management and senior management shall ensure that the contents of the
     contents are true, accurate and complete, and there is no indication of any
     false, accurate or substantial representation or material responsibility.'''

    data = {"baseText": text1, "changedText": text2}
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json'}

    response = requests.post(url, data=data_json, headers=headers)



    # if response:
    #     return simplejson.dumps(response)
    return render_template('compare.html', response=response.json())

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
