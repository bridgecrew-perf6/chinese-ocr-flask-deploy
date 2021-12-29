# Flask
from flask import Flask, request, render_template, jsonify

# Some utilites
import numpy as np
import cv2
from helper.util import base64_to_pil, draw, np_to_base64, read_url_img

# Declare a flask app
app = Flask(__name__)

# Models
from dnn.main import text_ocr

TEXT_LINE_SCORE=0.7## min prob thres for text line detection
scale = 900##no care text.cfg height,width
maxScale = 1800

@app.route('/', methods=['GET'])
def index():
    # Main page

    return render_template('index.html')
    
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the image/image_url from post request
        try:
            img = base64_to_pil(request.json)
        except:
            img = read_url_img(request.json)

        image = np.array(img)
        image =  cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        data,boxes = text_ocr(image,scale,maxScale,TEXT_LINE_SCORE)
        res_image = draw(boxes,img)       
        return jsonify(result=data, image=np_to_base64(np.array(res_image)))
    return None

if __name__ == '__main__':
    # FOR LOCAL RUN DEPLOY
    # app.run(port=3000, debug=True)
    
    # FOR LOCAL RUN DOCKER
    app.run(host='0.0.0.0',port=5002, debug=False)
    
    # FOR DEPLOYMENT DOCKER
    # import os
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host = '0.0.0.0', port = port)

