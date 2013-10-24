from flask import Flask
from flask import render_template
import cv2.cv as cv  
import tesseract

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html',random_text='1234')


@app.route('/ocr')
def ocr():
    filename = 'ocr.png'
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
    app.run()
