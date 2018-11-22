import hashlib
import sys,os
# from PIL import Image, ImageFont, ImageDraw, ImageFilter
# import random
import socket, threading
import json
'''
def store(user, secret, db):
    md5 = hashlib.md5()
    md5.update(secret.encode('utf-8'))
    result = md5.hexdigest()
    db[user] = result
'''

def verify(db):
    print(db)    
    name = db['username'] 
    passwd = db['password']

    # user_file = open('account.txt','r')  # 打开读取用户文件                           #打开帐号文件 
    
    user_file = open('Userform', 'r')
    # temp_file = open('Usernow','w') # 将在线用户写入一个表
    jsuser = user_file.read()
    dict_userold = json.load(jsuser) # 导入旧表

    for i in range(len(dict_userold)):
        if name not in dict_userold['user'+ str(i)]['name']:
            print('usererror')
            break
        if name in dict_userold['user'+ str(i)]['name']:
            if passwd == dict_userold['user'+ str(i)]['password']:
                print('yes')
                break
            else:
                print('passerror')


def send_back(dict):
    host = '127.0.0.1'
    port = 28956
    addr = (host, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    s.send(str(dict).encode('utf-8'))

def register(db):
    print(db)    
    name = db['username'] 
    passwd = db['password']
    while True:
        username = name #input('输入你的用户名\n')

        # user_file = open('account.txt','r')  # 打开读取用户文件                           #打开帐号文件 
        
        user_file = open('Userform', 'w')
        # temp_file = open('Usernow','w') # 将在线用户写入一个表
        jsuser = user_file.read()
        dict_userold = json.load(jsuser) # 导入旧表
        # dict.update(dict2) # 这个函数可以更新字典

        for i in len(dict_userold):
            if dict_userold['user'+ str(i)][name] == username:
                '''dictt = {}
                dictt['type'] = 'post'
                dictt['msg'] = '用户已存在'
                send_back(dictt)'''
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
            '''dict_post2 = {}
            dict_post2['type'] = 'post'
            dict_post2['msg'] = '必须有小写字母'  
            send_back(dict_post2)'''
            print('密码必须有大、小写字母，数字，和特殊字符四部分组成,请重新输入')
        else:
            dict_post3 = {}
            dict_post3['type'] = 'post'
            dict_post3['msg'] = '注册成功'
            send_back(dict_post3) 
            print('注册成功')
            # 存入表单
            dict_add = {
                'user'+str(len(dict_userold)):{
                            'name': username,
                            'password': secret
                }
            }
            dict_userold.update(dict_add)
            jsuser_add = json.dumps(dict_userold)
            user_file.write(jsuser_add)
            user_file.close()
            break


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
        dicData = eval(recvmsg.decode("utf-8"))
        head = dicData['head']
        # dicData = {'sam': '67ae79674e56657bb652bd02f7251474'}
        # receive = input()
        if dicData['head'] == '0':
            register(dicData)
        elif head == '1':
            verify(dicData)
        else :
            pass
    socketserver.close()