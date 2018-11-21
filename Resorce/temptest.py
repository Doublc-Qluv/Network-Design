# temptest
import hashlib
import sys,os
# from PIL import Image, ImageFont, ImageDraw, ImageFilter
# import random
import socket, threading

def send_back(dict):
    host = '127.0.0.1'
    port = 28956
    addr = (host, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    s.send(str(dict).encode('utf-8'))

def register(db):
    while True:
        username = name #input('输入你的用户名\n')

        user_file = open('account.txt','r')  # 打开读取用户文件                           #打开帐号文件 
        user_list = user_file.readlines()   
        for user_line in user_list:                                     #对帐号文件进行遍历
            (user,passwords) = user_line.strip('\n').split()             #分别获取帐号和密码信息
            if name == user:
                # existence = '用户已存在'
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
    socketserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port =28956
    socketserver.bind((host, port))
    socketserver.listen(5)
    clientsocket,addr = socketserver.accept()

    while True:
        #接收客户端的请求
        recvmsg = clientsocket.recv(1024)
        #把接收到的数据进行解码
        strData = eval(recvmsg.decode("utf-8"))
        
        head = strData['head']
        # strData = {'sam': '67ae79674e56657bb652bd02f7251474'}
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