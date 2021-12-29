from PIL import Image
import json
import os
import numpy as np
import cv2

ocrNet = cv2.dnn.readNetFromCaffe('models/ocr.prototxt', 'models/ocr.caffemodel')

def read_characters():
    p = 'models/ocr.json'
    if os.path.exists(p):
        with open(p,encoding='utf-8')  as f:
            characters = json.loads(f.read())
        return characters
    else:
        return ''


charactersPred = ' '+read_characters()+'｜ '


def softmax(res):
    resMax = res.max(axis=1).reshape((-1,1))
    res    = res-resMax
    res    = np.exp(res)
    expSum = res.sum(axis=1).reshape((-1,1))
    return res/expSum

def decode(pred):
        t = pred.argmax(axis=1)
        prob  = [ pred[ind,pb] for ind,pb in enumerate(t)]
        length = len(t)
        charList = []
        probList = []
        n = len(charactersPred)
        for i in range(length):
           if t[i] not in [n-1,n-1] and (not (i > 0 and t[i - 1] == t[i])):
                        charList.append(charactersPred[t[i]])
                        probList.append(prob[i])
        res = {'text':''.join(charList),
               "prob":round(float(min(probList)),2) if len(probList)>0 else 0,
               "chars":[{'char':char,'prob':round(float(p),2)}for char ,p in zip(charList,probList)]}
        return res


def predict_caffe(image):
    """
    use converted caffe model
    """

    scale = image.size[1]*1.0 / 32
    w = image.size[0] / scale
    w = int(w)
    if w<8:
        return {'chars':[],'text':'','prob':0}
    image   = image.resize((w,32),Image.BILINEAR)
    image = (np.array(image.convert('L'))/255.0-0.5)/0.5
    image = np.array([[image]])
    ocrNet.setInput(image)
    y_pred = ocrNet.forward()
    out = y_pred[0][:,0,:]
    
    out = out.transpose((1,0))
    out = softmax(out)
    out = decode(out)##

    return out

if __name__=='__main__':
    import time
    t =time.time()
    img=Image.open('test.jpg')
    res = predict_caffe(img)
    print(time.time()-t,res)


