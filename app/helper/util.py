"""Utilities
"""
import re
import base64
import requests
from PIL import Image, ImageDraw
from io import BytesIO

def read_url_img(url):
    """
    scraping url image
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'}
    try:
        req = requests.get(url,headers=headers,timeout=5)##访问时间超过5s，则超时
        if req.status_code==200:
            imgString = req.content
            img = Image.open(BytesIO(imgString))
            return img
        else:
            return None
    except:
        #traceback.print_exc()
        return None

def base64_to_pil(img_base64):
    """
    Convert base64 image data to PIL image
    """
    image_data = re.sub('^data:image/.+;base64,', '', img_base64)
    pil_image = Image.open(BytesIO(base64.b64decode(image_data)))
    return pil_image


def np_to_base64(img_np):
    """
    Convert numpy image (RGB) to base64 string
    """
    img = Image.fromarray(img_np.astype('uint8'), 'RGB')
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return u"data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode("ascii")

def draw(boxes,img):
    """
    Draw text line boxes on image
    """

    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)
    for box in boxes:
        x1,y1,x2,y2,x3,y3,x4,y4 = box[:8]
        draw.line([(x1, y1),(x2, y2)], fill=(0, 0, 255),width=2)
        draw.line([(x2, y2),(x3, y3)], fill=(255, 0, 0),width=2)
        draw.line([(x3, y3),(x4, y4)],fill= (0,0,255),width=2)
        draw.line([(x1, y1), (x4, y4)],fill=(255,0,0),width=2)

    return img