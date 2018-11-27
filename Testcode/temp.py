import hashlib
import sys,os
# from PIL import Image, ImageFont, ImageDraw, ImageFilter
# import random
import socket, threading
import json
import re

# 新线程执行的代码:
'''
def loop():
    print('thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)

print('thread %s is running...' % threading.current_thread().name)
t = threading.Thread(target=loop, name='LoopThread')
t.start()
t.join()
print('thread %s ended.' % threading.current_thread().name)
'''
'''
file = open('Userform', 'r') 
js = file.read()
dic = json.loads(js)
for i in range(len(dic)):
    dicnew = {
        'user'+str(i):dic['user'+str(i)]['name']
    }
    dic.update(dicnew)
print(dic)
'''
#!/usr/bin/env python

    # -*-coding:utf-8 -*-
#Uer="name1"
#password="name1Python"
'''
uer=["name1", "name2", "name3", "name4",  "name5"]
password=["name1Python", "name2Python", "name3Python", "name4Python", "name5Python"]

count=0
flag=0
while count<3:
    Uername = input("请输入用户名：")
    Password = input("请输入密码：")
    for index in range(len(uer)) :
       if uer[index] == Uername and password[index] == Password :
           print("----欢迎登录----")
           flag=1
           break
    if flag ==1:
        break
    count +=1
'''

def add_onlist(dic):
    username = dic['username'] #input('输入你的用户名\n')
    # user_file = open('account.txt','r')  # 打开读取用户文件
    user_file = open('Usernow', 'r+')
    # temp_file = open('Usernow','w') # 将在线用户写入一个表
    jsuser = user_file.read()
    dict_userold = json.loads(jsuser) # 导入旧表
    # dict.update(dict2) # 这个函数可以更新字典
    user_file.close()
    dict_add = {
        'user'+str(len(dict_userold)): username
        }
    dict_userold.update(dict_add)
    jsuser_add = json.dumps(dict_userold)
    user_file2 = open('Usernow', 'r+') 
    user_file2.write(jsuser_add)
    user_file2.close()


dicta = {'username':'sam'}
add_onlist(dicta)