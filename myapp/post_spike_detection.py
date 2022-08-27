#python3
# -*- coding: utf-8 -*-
import json
import base64
from io import BytesIO
from PIL import Image
import time
import requests
import cv2
from matplotlib import pyplot as plt
import os
from django.conf import settings

raw = {"image_name" :'',
       'image_path':'',
       "p_xd":0.01,
       "ap_xd":0,
        "username":"inference"}
#存放原始图片的目录，检测好的图片会存在同一目录下，文件名后增加_spike_detection字段
# path = 'D:/shoe_photo/'
# path = "../media/documents"

#对图片进行base64编码
def image_to_base64(image):
    output_buffer = BytesIO()
    image.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str
#使用API制定的的POST方式发起请求
def post_req(raw,urls):
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                   "Content-Type": "application/json",
                  "x-client-appcode":"K63tp6fI7eBjxwOlvPwvP5cp5tkV02WE",
                  "charset":"UTF-8"}
    textmod = json.dumps(raw).encode(encoding='utf-8')
    req = requests.post(url=urls,data=textmod,headers=header_dict)
    return req.text


def detection(path, url, fType):
    list = os.listdir(path)
    # 按顺序把文件夹中待检测的图片进行检测，标出鞋钉的位置再保存图片
    for photo in list:
        print('photo:', photo)
        if '_d' not in photo:
            photo_dir = os.path.join(path, photo)
            image = Image.open(photo_dir)
            img = image_to_base64(image)
            name = photo_dir

            if fType == 'ding':
                # name = photo_dir.split('/')[-1]  # winows
                # name = photo_dir.split('\\')[-1]  # linux
                raw['image_name'] = name
                img = str(img, encoding='utf-8')
                raw['image_path'] = img
                result_raw = post_req(raw,url)
                result = json.loads(result_raw)
                print(result)
                # API输出结果显示，'NG', 4, [[144, 136, 20, 40], [213, 413, 17, 34], [213, 413, 17, 34], [213, 413, 17, 34]]表示检测出鞋钉、鞋钉的数量和坐标
                im = cv2.imread(photo_dir)
                img = im.copy()
                # counts = len(result['Response'][2])
                for item in result['Response'][2]:
                    # 标出长方形框
                    cv2.rectangle(img, (item[0], item[1]), (item[0] + item[2], item[1] + item[3]), (0, 255, 0), 5)
                new_name = name.split('.')[0] + '_d.' + name.split('.')[1]
                print("new_name:",new_name)
                cv2.imwrite(new_name, img)
                # return result['Response']

            elif fType == 'mao':
                img = str(img, encoding='utf-8')
                headers = {"appId": "health_check", "token": "123", "requestId": "201803080000098300001", "requestTime": "2018-05-22 21:12:00"}
                body = '{"serviceName":"tj_jgfsjc_app", "image":"%s", "contain": "health_check"}' % img  # 新平台
                result_raw = requests.post(url=url, data=body, headers=headers)
                im = cv2.imread(photo_dir)
                img = im.copy()
                if result_raw.status_code == 200:
                    response_code = json.loads(result_raw.text)["errorcode"]
                    if str(response_code) == '0':
                        # for i in json.loads(response.text)['data']:
                        # {'type': 'YES', 'left_up_x': '667', 'left_up_y': '256', 'right_down_x': '715', 'right_down_y': '314'}
                        # {'type': 'YES', 'left_up_x': '823', 'left_up_y': '251', 'right_down_x': '871', 'right_down_y': '314'}
                        for item in json.loads(result_raw.text)['data']:
                            # print(item)
                            cv2.rectangle(img, (item['left_up_x'], item['left_up_y']), (item['right_down_x'], item['right_down_y']), (0, 255, 0),
                                          3)
                            new_name = name.split('.')[0] + '_d.' + name.split('.')[1]
                            print("new_name:", new_name)
                            cv2.imwrite(new_name, img)
                        else:
                            print("response_code ! = 0")
                else:
                    print("status_code != 200")

            elif fType == 'face':
                pass
            return result_raw


