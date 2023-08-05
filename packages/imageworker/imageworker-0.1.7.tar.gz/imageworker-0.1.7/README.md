## Usage


### file to ndarray

```pycon
>>> from imageworker import file_to_array
>>> data = file_to_array("test.jpg")
```

### url to ndarray

```pycon
>>> from imageworker import url_to_array
>>> data = url_to_array("https://n.sinaimg.cn/spider2021326/106/w1024h682/20210326/5927-kmvwsvy1040641.jpg")
```

### upload ndarray to qiniu cdn

```pycon
>>> key = QINIU_KEY
>>> secret = QINIU_SECRET
>>> domain = HOST
>>> bucket = QINIU_BUCKET
>>> url = put_qiniu(data,key,secret,domain,bucket) 
```



