# -*- coding: utf-8 -*-
"""
https://github.com/KD-happy/KDCheckin/blob/main/Music163.py
cron: 10 6 * * *
new Env('网易云音乐');
"""

import requests, time, re, json, sys, traceback, os
from io import StringIO

from notify import send

class Music163:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.cookie = ''

    def Sign_in(self):
        url0 = "http://music.163.com/api/point/dailyTask?type=0"
        url1 = "http://music.163.com/api/point/dailyTask?type=1"
        s0 = requests.get(url0, headers={'Cookie': self.cookie})
        print(s0.text)
        if "重复" in str(s0.json()):
            s0 = "手机端: 重复签到"
        else:
            if "point" in str(s0.json()):
                s0 = "手机端: 获得" + str(s0.json()["point"]) + "云贝"
            else:
                s0 = "手机端: Cookie失效"
        s1 = requests.get(url1, headers={'Cookie': self.cookie})
        print(s1.text)
        if "重复" in str(s1.text):
            s1 = "桌面端: 重复签到"
        else:
            if "point" in str(s1.json()):
                s1 = "桌面端: 获得" + str(s1.json()["point"]) + "云贝"
            else:
                s1 = "桌面端: Cookie失效"
        self.sio.write(s0 +"\n"+ s1 + '\n')

    def SignIn(self):
        print("【网易云音乐 日志】")
        self.sio.write("【网易云音乐】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            print(f"{cookie.get('name')} 开始签到...")
            self.sio.write(f"{cookie.get('name')}: \n")
            self.cookie = cookie.get('cookie')
            try:
                self.Sign_in()
            except:
                print(f"{cookie.get('name')}: 异常 {traceback.format_exc()}")
                if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                    self.sio.write('签到存在异常, 请自行查看签到日志\n')
        return self.sio

if __name__ == '__main__':
    Cookies = os.getenv('MUSIC163_COOKIE')
    if Cookies != None:
        Cookies = json.loads(Cookies)
        music163 = Music163(Cookies)
        sio = music163.SignIn()
        print(f'\n{sio.getvalue()}')
        send('网易云音乐', sio.getvalue())
    else:
        print('配置文件没有 网易云音乐')
