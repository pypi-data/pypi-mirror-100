import qiniu
import hashlib
from qiniu.services.cdn.manager import create_timestamp_anti_leech_url
from keras_preprocessing import image as imagetool
import os


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

