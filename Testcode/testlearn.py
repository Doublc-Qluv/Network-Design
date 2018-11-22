# testlearn

# temptest
import hashlib
import sys,os
# from PIL import Image, ImageFont, ImageDraw, ImageFilter
# import random
import socket, threading
import json
'''
def register(db):
    while True:
        username = name #input('输入你的用户名\n')

        user_file = open('account.txt','r')  # 打开读取用户文件                           #打开帐号文件 
        user_list = user_file.readlines()   
        for user_line in user_list:                                     #对帐号文件进行遍历
            (user,passwords) = user_line.strip('\n').split()             #分别获取帐号和密码信息
            if name == user:
                existence = '用户已存在'
                dict = {}
                dict['type'] = 'p'
                dict['msg'] = '用户已存在'
                send_back(dict)
                print('用户名已存在')
                continue

        secret = passwd # input('输入你的密码:\n')
        dicta = {'number': 0, 'lower': 0, 'upper': 0, 'other': 0}
        for item in secret:
            if item.isdigit():
                dicta['number'] += 1
            elif item.islower():
                dicta['lower'] += 1
            elif item.isupper():
                dicta['upper'] += 1
            else:
                dicta['other'] += 1
        if dicta['lower'] < 1: # or dicta['upper'] < 1 or dicta['number'] < 1 or dicta['other'] < 1:
            dict2 = {}
            dict2['type'] = 'p'
            dict2['msg'] = '必须有小写字母'  
            send_back(dict2)
            print('密码必须有大、小写字母，数字，和特殊字符四部分组成,请重新输入')
        else:
            dict3 = {}
            dict3['type'] = 'p'
            dict3['msg'] = '欢迎'
            send_back(dict3) 
            print('验证通过，欢迎光临')
            break
    return username, secret

if __name__ == '__main__':

    while True:

        head = strData['head']
        # stData = {'sam': '67ae79674e56657bb652bd02f7251474'}
        # receive = input()
        if strData['head'] == '0':
            print(strData)    
            name = strData['username'] 
            passwd = strData['password']

            user, password = register(strData)
            # store(user, password, strData)
            print(strData)
        elif head == '1':
            pass#verify(strData)
        else :
            break
    socketserver.close()

'''

'''
list_dict_all = []               #创建一个空列表，全局变量，用来存放字典
def AddtoDict(str_1):            # 定义一个函数，功能：把文件里面的内容添加到字典中

   list_str1 = str_1.split(" ")  # 读取的行内容以字符串的形式显示出来, 使用‘,’分隔字符串

   line_str = []                 # 创建一个空列表，用来接收去掉'\n'的行字符串
   for i in list_str1:
       x = i.strip("\n")
       line_str.append(x)
   print(line_str)

   dict_all = {}                         # 创建一个空字典
   for item in line_str:                 # 遍历列表中的行内容，列表中有3个元素
       if item[0:3] == "url":            # 列表中的元素，前3个字符是否等于“url”
           dict = {item[0:3]: item[4:]}     # dict = {'url':'http://119.23.241.154:8080/futureloan/mvc/api/member/login'}
           dict_all.update(dict)            # 添加dict到空字典dict_all中
           # print(dict_all)
       else:
           dict = {item.split(":")[0]: item.split(":")[1]}  # 除url外，取其他数据key, value到字典中
           dict_all.update(dict)
   list_dict_all.append(dict_all)                     # 将字典添加到list列表中

def list_dict(file_1):
    file = open(file_1, "r+")
    while True:
        line = file.readline()
        if line:
            AddtoDict(line)
        if not line:
            break
    file.close()
    print(list_dict_all)

list_dict("account.txt")        # 传入文件路径及名称即可实现将文件中的内容以[{}, {}....]的形式输出
'''
'''
# 初始化
dic = {  
    'user1':{  
        'name': 'sam',
        'password': '123' 
    },  
    'user0': {  
        'name': 'root',  
        'password': 'root'
    },
    'user2': {
        'name': 'kevin',
        'password': '123'
    }  
}   
js = json.dumps(dic)   
file = open('Userform', 'w')  
file.write(js)
  
file.close()
'''

# json读取
username = 'asdd'
secret = '123'
file = open('Userform', 'r') 
js = file.read()
dic = json.loads(js) 
dic2 = {
    'user'+str(len(dic)):{
                'name': username,
                'password': secret
    }
}
dic.update(dic2)

for i in range(4):
    print(dic['user'+str(i)])


length = len(dic)

file.close()


#while True:
    #username = name # input('输入你的用户名\n')
    #secret = passwd # input('输入你的密码:\n')
for i in range(4):#range(length):
    if username == dic['user'+ str(i)]['name']:
        if secret == dic['user'+ str(i)]['password']:
            print('验证通过，欢迎光临')
            continue                
        else:
            print('密码不正确,请重新输入')
            continue
    else :
        print('yonghuminn不正确,请重新输入')
