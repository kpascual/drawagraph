from flask import Flask
from flask import render_template
from flask import request
import cv2.cv as cv  
import tesseract
import re
import base64

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html',random_text='1234')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print 'Got post'
        img = request.form['imgBase64']
        dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
        imgb64 = dataUrlPattern.match(img).group(2)
        if imgb64 is not None and len(imgb64) > 0:
            decoded_img = base64.b64decode(imgb64)

        filename = 'file_to_read.png' 
        with open(filename, 'wb') as f1:
            f1.write(decoded_img)

        text = translate(filename)
        #text = translate('ocr.png')
        print text
        return text

    if request.method == 'GET':
        return 'upload called'

@app.route('/ocr')
def ocr():
    filename = 'ocr.png'
    image=cv.LoadImage(filename, cv.CV_LOAD_IMAGE_GRAYSCALE)
    print image

    api = tesseract.TessBaseAPI()
    api.Init(".","eng",tesseract.OEM_DEFAULT)
    #api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)
    api.SetPageSegMode(tesseract.PSM_AUTO)
    tesseract.SetCvImage(image,api)
    text=api.GetUTF8Text()
    conf=api.MeanTextConf()
    return text


def translate(filename):
    image=cv.LoadImage(filename, cv.CV_LOAD_IMAGE_GRAYSCALE)
    api = tesseract.TessBaseAPI()
    api.Init(".","eng",tesseract.OEM_DEFAULT)
    #api.SetPageSegMode(tesseract.PSM_SINGLE_WORD)
    api.SetPageSegMode(tesseract.PSM_AUTO)
    tesseract.SetCvImage(image,api)
    text=api.GetUTF8Text()
    conf=api.MeanTextConf()
    return text


if __name__ == '__main__':
    app.run(host='0.0.0.0')
