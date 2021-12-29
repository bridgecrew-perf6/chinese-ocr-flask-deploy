import numpy as np
from helper.image import resize_img,get_origin_box,soft_max,reshape
from helper.detectors import TextDetector
import cv2

anchors = '16,11, 16,16, 16,23, 16,33, 16,48, 16,68, 16,97, 16,139, 16,198, 16,283'

textNet = cv2.dnn.readNetFromCaffe('models/text.prototxt', 'models/text.caffemodel')
print('loaded caffemodel')

def detect_box(image,scale=600,maxScale=900):
        image,rate = resize_img(image,scale,maxScale=maxScale)
        h,w = image.shape[:2]

        inputBlob = cv2.dnn.blobFromImage(image, scalefactor=1.0, size=(w,h),swapRB=False ,crop=False);
        outputName = textNet.getUnconnectedOutLayersNames()
        textNet.setInput(inputBlob)
        out  = textNet.forward(outputName)[0]
               
        clsOut  = reshape(out[:,:20,...])
        boxOut  = reshape(out[:,20:,...])
        boxes  = get_origin_box((w,h),anchors,boxOut[0])        
        scores = soft_max(clsOut[0])
        boxes[:, 0:4][boxes[:, 0:4]<0] = 0
        boxes[:, 0][boxes[:, 0]>=w] = w-1
        boxes[:, 1][boxes[:, 1]>=h] = h-1
        boxes[:, 2][boxes[:, 2]>=w] = w-1
        boxes[:, 3][boxes[:, 3]>=h] = h-1
        
        return scores,boxes,rate,w,h

def detect_lines(image,
                 scale=600,
                 maxScale=900,
                 MAX_HORIZONTAL_GAP=30,
                 MIN_V_OVERLAPS=0.6,
                 MIN_SIZE_SIM=0.6,
                 TEXT_PROPOSALS_MIN_SCORE=0.7,
                 TEXT_PROPOSALS_NMS_THRESH=0.3,
                 TEXT_LINE_NMS_THRESH = 0.9,
                 TEXT_LINE_SCORE=0.9
                ):
    MAX_HORIZONTAL_GAP = max(16,MAX_HORIZONTAL_GAP)
    scores,boxes,rate,w,h = detect_box(image,scale,maxScale)
    size = (h,w)
    detectors = TextDetector(MAX_HORIZONTAL_GAP,MIN_V_OVERLAPS,MIN_SIZE_SIM)
    text_lines, scores =detectors.detect( boxes,scores,size,\
           TEXT_PROPOSALS_MIN_SCORE,TEXT_PROPOSALS_NMS_THRESH,TEXT_LINE_NMS_THRESH,TEXT_LINE_SCORE)
    if len(text_lines)>0:
        text_lines = text_lines/rate
    return text_lines, scores