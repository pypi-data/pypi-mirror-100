import qiniu
import hashlib
from qiniu.services.cdn.manager import create_timestamp_anti_leech_url
from keras_preprocessing import image as imagetool
import os,io
import numpy as np

from PIL import Image
import requests 
from urllib import parse


def put_file_to_qiniu(filepath,
                      access_key:str, 
                      secret_key:str,
                      domain:str,
                      bucket:str):
    q = qiniu.Auth(access_key, secret_key)
    token = q.upload_token(bucket)
    with open(filepath, "rb") as f:
        subfix = filepath.split(".")[-1]
        upname = f"{hashlib.md5(f.read()).hexdigest()}.{subfix}"
        ret, info = qiniu.put_file(token,upname,filepath)
        key = ret['key']
        base_url = f'{domain}/{key}'
        private_url = q.private_download_url(base_url, expires=3600)
        return private_url
    return None

def put_qiniu(np,
        access_key:str, 
        secret_key:str,
        domain:str,
        bucket:str):
    q = qiniu.Auth(access_key, secret_key)
    img = imagetool.array_to_img(np)
    data = img.tobytes()
    key = f"{hashlib.md5(data).hexdigest()}.png"
    img.save(key)
    url = put_file_to_qiniu(key,access_key,secret_key,domain,bucket)
    os.remove(key)
    return url



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

def file_to_array(path):
    f = Image.open(path)
    data = imagetool.img_to_array(f)
    return data

def url_to_file(url,filepath = None):
    d = url_to_array(url)
    if filepath is None:
        p = parse.urlparse(url)
        filepath = p.path[1:]
    i = Image.fromarray(d,"RGB")
    i.save(filepath)

def file_to_file(filepath, newpath):
    d = file_to_array(filepath)
    i = imagetool.array_to_img(d)
    i.save(newpath)