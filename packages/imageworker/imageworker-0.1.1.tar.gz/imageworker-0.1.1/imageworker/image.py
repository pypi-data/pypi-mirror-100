import qiniu
import hashlib
from qiniu.services.cdn.manager import create_timestamp_anti_leech_url
from keras_preprocessing import image as imagetool
import os,io
import numpy as np

from PIL import Image
import requests 

def put_qiniu(np,
        access_key:str, 
        secret_key:str,
        domain:str,
        bucket:str):
    q = qiniu.Auth(access_key, secret_key)
    token = q.upload_token(bucket)
    img = imagetool.array_to_img(np)
    data = img.tobytes()
    key = f"{hashlib.md5(data).hexdigest()}.png"
    img.save(key)
    ret, info = qiniu.put_file(token,key,key) 
    os.remove(key)
    key = ret['key']
    base_url = f'{domain}/{key}'
    private_url = q.private_download_url(base_url, expires=3600)
    return private_url



def url_to_array(url):
    result = requests.get(url, timeout=3)
    if result.ok:
        img = Image.open(io.BytesIO(result.content))
        img =  img.convert('RGB')
        data =  np.array(img)
        return data
    else:
        print("http get:{}".format(result.status_code))
        return None
