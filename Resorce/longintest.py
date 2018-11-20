import hashlib
import sys,os
# from PIL import Image, ImageFont, ImageDraw, ImageFilter
# import random
import socket

'''
def store(user, secret, db):
    md5 = hashlib.md5()
    md5.update(secret.encode('utf-8'))
    result = md5.hexdigest()
    db[user] = result
'''

def verify(db):
    while True:
        username = input('输入你的用户名\n')
        secret = input('输入你的密码:\n')
        md5 = hashlib.md5()
        md5.update(secret.encode('utf-8'))
        result = md5.hexdigest()
        if username not in db:
            print('用户名不存在')
        elif db[username] == result:
            print('验证通过，欢迎光临')
            break
        else:
            print('密码不正确,请重新输入')


def register(db):
    while True:
        username = name #input('输入你的用户名\n')

        user_file = open('account.txt','r')  # 打开读取用户文件                           #打开帐号文件 
        user_list = user_file.readlines()   

        if username in db.keys():
            print('用户名已存在，请重新输入')
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
            print('密码必须有大、小写字母，数字，和特殊字符四部分组成,请重新输入')
        else:
            print('验证通过，欢迎光临')
            break
    return username, secret


if __name__ == '__main__':
    #创建服务端的socket对象socketserver
    socketserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'

    port =28956
    #绑定地址（包括ip地址会端口号）
    socketserver.bind((host, port))
    #设置监听
    socketserver.listen(5)
    #等待客户端的连接
    #注意：accept()函数会返回一个元组
    #元素1为客户端的socket对象，元素2为客户端的地址(ip地址，端口号)
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