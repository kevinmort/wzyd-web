#python3
# -*- coding: utf-8 -*-
import json
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import time
import requests
import numpy as np
import cv2
from matplotlib import pyplot as plt
import os

raw = {"image_name" :'',
       'image_path':'',
       "p_xd":0.01,
       "ap_xd":0,
        "username":"inference"}
#存放原始图片的目录，检测好的图片会存在同一目录下，文件名后增加_spike_detection字段
path = '../media/documents/'
#API调用的公网接口
urls = 'http://117.149.212.37:30080/xdjc'

#对图片进行base64编码
def image_to_base64(image):
    output_buffer = BytesIO()
    image.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str
#使用API制定的的POST方式发起请求
def post_req(raw):
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                   "Content-Type": "application/json",
                  "x-client-appcode":"K63tp6fI7eBjxwOlvPwvP5cp5tkV02WE",
                  "charset":"UTF-8"}
    textmod = json.dumps(raw).encode(encoding='utf-8')
    req = requests.post(url=urls,data=textmod,headers=header_dict)
    return req.text


list = os.listdir(path)
#按顺序把文件夹中待检测的图片进行检测，标出鞋钉的位置再保存图片
for photo in list:
    if '_spike_detection' not in photo:
        photo_dir = path + photo
        image = Image.open(photo_dir)
        img = image_to_base64(image)
        name = photo_dir.split('/')[-1]        
        raw['image_name'] = name
        img = str(img,encoding='utf-8')
        raw['image_path'] = img
        result = post_req(raw)
        result = json.loads(result)
        #API输出结果显示，'NG', 4, [[144, 136, 20, 40], [213, 413, 17, 34], [213, 413, 17, 34], [213, 413, 17, 34]]表示检测出鞋钉、鞋钉的数量和坐标
        print(result) #
        im = cv2.imread(photo_dir)
        img = im.copy()
        for item in result['Response'][2]:
            print(item)
            cv2.rectangle(img, (item[0], item[1]), (item[0]+item[2], item[1]+item[3]), (0, 255, 0),5)
            cv2.putText()
            new_name = name.split('.')[0]+'_spike_detection.'+name.split('.')[1]
            new_photo_dir = os.path.join(path, new_name)
            print("new_name:", new_name)
            print("new_photo_dir:",new_photo_dir)
            cv2.imwrite(new_photo_dir,img)
