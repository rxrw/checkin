# -*- coding: utf-8 -*-
"""
cron: 0 6 * * *
new Env('Tool工具');
"""

import os
import requests, re, sys, traceback
from io import StringIO

from notify import send

class ToolLu:
    def __init__(self, cookie):
        self.sio = StringIO()
        self.Cookies = cookie
        self.cookie = ''

    def sign(self):
        url = 'https://id.tool.lu/sign/'
        headers = {
            "cookie": self.cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        res = requests.get(url=url, headers=headers)
        day = re.findall('你已经连续签到(.*)，再接再厉！', res.text)
        if len(day) == 0:
            self.sio.write('Cookie失效\n')
            print('Cookie失效')
        else:
            day = day[0].replace(' ', '')
            self.sio.write(f'连续签到 {day}\n')
            print(f'连续签到 {day}')

    def SignIn(self):
        print("【Tool工具 日志】")
        self.sio.write("【Tool工具】\n")
        for cookie in self.Cookies:
            cookie = cookie.get("user")
            print(f"{cookie.get('name')} 开始签到...")
            self.sio.write(f"{cookie.get('name')}: ")
            self.cookie = cookie.get('cookie')
            try:
                self.sign()
            except:
                print(f"{cookie.get('name')}: 异常 {traceback.format_exc()}")
                if '签到存在异常, 请自行查看签到日志' not in self.sio.getvalue():
                    self.sio.write('签到存在异常, 请自行查看签到日志\n')
        return self.sio

if __name__ == '__main__':
  Cookies = os.environ.get("TOOLLU_COOKIE")
  if Cookies != None:
    Cookies = json.loads(Cookies)
    toollu = ToolLu(Cookies)
    sio = toollu.SignIn()
    print(f'\n{sio.getvalue()}')
    send('Tool工具', sio.getvalue())
  else:
      print('配置文件没有 Tool工具')