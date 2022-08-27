# -*- coding: utf-8 -*-
import os
import requests
import base64
import sys
import json

host = sys.argv[1]
port = sys.argv[2]

path = os.path.dirname(os.path.abspath(__file__))
URL = 'http://{}:{}/service'.format(host, port)
headers = {"appId": "health_check", "token": "123", "requestId": "201803080000098300001",
           "requestTime": "2018-05-22 21:12:00"}

with open("test.jpg", "rb") as f1:
    image1_base64_data = base64.b64encode(f1.read()).decode('utf-8')

body = '{"serviceName":"tj_jgfsjc_app", "image":"%s", "contain": "health_check"}' % image1_base64_data  # 新平台

def check_health():
    try:
        response = requests.post(url=URL, data=body, headers=headers)
        exception = 0
        print(json.dumps(response.content))
        if response.status_code == 200:
            response_code = json.loads(response.text)["errorcode"]
            if str(response_code) != '0':
                exception = 1
            pass
        else:
            exception = 1
    except Exception as e:
        exception = 1
    return exception

if __name__ == '__main__':
    print(check_health())