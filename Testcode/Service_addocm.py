import hashlib
import sys,os
# from PIL import Image, ImageFont, ImageDraw, ImageFilter
# import random
import socket, threading
import json
import re
import socketserver

clients = {}    #提供 用户名->socket 映射
chatwith = {}   #提供通信双方映射
def add_onlist(dic,hostport):
    username = dic['username'] #input('输入你的用户名\n')
    # user_file = open('account.txt','r')  # 打开读取用户文件
    user_file = open('Usernow', 'r+')
    # temp_file = open('Usernow','w') # 将在线用户写入一个表
    jsuser = user_file.read()
    dict_userold = json.loads(jsuser) # 导入旧表
    # dict.update(dict2) # 这个函数可以更新字典
    user_file.close()
    dict_add = {
        username:hostport
        }
    dict_userold.update(dict_add)
    jsuser_add = json.dumps(dict_userold)
    user_file2 = open('Usernow', 'r+') 
    user_file2.write(jsuser_add)
    user_file2.close()
def del_onlist(username):
    # user_file = open('account.txt','r')  # 打开读取用户文件
    user_file = open('Usernow', 'r+')
    user_file.close()
    # temp_file = open('Usernow','w') # 将在线用户写入一个表
    jsuser = user_file.read()
    dict_userold = json.loads(jsuser) # 导入旧表
    # dict.update(dict2) # 这个函数可以更新字典
    dict_userold = dict_userold.pop(username)
    dict_userold.update(dict_userold)
    jsuser_add = json.dumps(dict_userold)
    user_file2 = open('Usernow', 'r+') 
    user_file2.write(jsuser_add)
    user_file2.close()
def onlinedict():
    pass
    file = open('Usernow', 'r') 
    js = file.read()
    dicnow = json.loads(js)
    file.close()
    return dicnow

def relist_all():
    # 总表
    file = open('Userform', 'r') 
    js = file.read()
    dic = json.loads(js)
    dicn = {}
    for i in range(len(dic)):
        dicte = {
            dic['user'+ str(i)]['name']:str(i)
        }
        dicn.update(dicte)
    L1 = list(dicn.keys())
    # 在线表
    file = open('Usernow', 'r') 
    js = file.read()
    dicnow = json.loads(js)

    L1 = list(dicn.keys())
    L2 = list(dicnow.keys())
    dict_back = {}
    dict_back['Head'] = 'UserNameList'
    dict_back['type'] = 'GET'
    dict_back['ActiveUserList'] = str(L2)
    dict_back['WholeUserList'] = str(L1)
    # return L1,L2
    return dict_back

def verify(db,hostport):
    print(db)    
    name = db['username'] 
    passwd = db['password']
    # user_file = open('account.txt','r')  # 打开读取用户文件
    user_file = open('Userform', 'r')
    # temp_file = open('Usernow','a+') # 将登陆用户写入一个表
    jsuser = user_file.read()
    dict_userold = json.loads(jsuser) # 导入旧表
    dict_passverify = {}
    dict_passverify['Head'] = 'login'
    dict_passverify['type'] = 'GET' 
    print(len(dict_userold))
    flag = len(dict_userold)
    for i in range(len(dict_userold)):
        # print(dict_userold['user'+ str(i)]['name'])
        if name == dict_userold['user'+ str(i)]['name'] and passwd == dict_userold['user'+ str(i)]['password']:                      
            if name in onlinedict():
                flag = 0
                break  
            dict_passverify['Flag'] = 1
            dict_passverify['content'] = 'welcome'
            #send_back(dict_passverify)
            print('welcome')
            add_onlist(db,hostport)
            break
        else:
            flag -= 1
            continue
    if flag == 0:
            dict_passverify['Flag'] = 0
            dict_passverify['content'] = 'user-or-password-error'
            #send_back(dict_passverify)
            print('user-or-password-error')
    return dict_passverify

def register(db):
    # print(db)    
    name = db['username'] 
    passwd = db['password']
    username = name #input('输入你的用户名\n')
    # user_file = open('account.txt','r')  # 打开读取用户文件
    user_file = open('Userform', 'r')
    # temp_file = open('Usernow','w') # 将在线用户写入一个表
    jsuser = user_file.read()
    dict_userold = json.loads(jsuser) # 导入旧表
    # dict.update(dict2) # 这个函数可以更新字典
    user_file.close()
    dict_register = {}
    dict_register['Head'] = 'register'
    dict_register['type'] = 'GET'
    flag = 0
    for i in range(len(dict_userold)):
        if dict_userold['user'+ str(i)]['name'] == username:            
            dict_register['Flag'] = 0
            dict_register['content'] = '用户已存在'
            #send_back(dict_register)
            print('用户名已存在')
            break
        elif dict_userold['user'+ str(len(dict_userold)-1)]['name'] != username:
            flag = 1
            break
        else:
            continue
    if flag:
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
        if dicta['number'] + dicta['lower'] + dicta['upper'] + dicta['other'] < 4:
            dict_register['Flag'] = 0
            dict_register['content'] = '密码至少大于四位'
            #send_back(dict_register)
            print('密码至少大于四位')
        elif dicta['lower'] < 1 or dicta['number'] < 1 : # or dicta['upper'] < 1 or dicta['other'] < 1: 
            dict_register['Flag'] = 0
            dict_register['content'] = '密码至少要有一个小写字母以及一个数字'
            #send_back(dict_register)
            print('密码至少要有一个小写字母以及一个数字')
        else:
            dict_register['Flag'] = 1
            dict_register['content'] = '注册成功'
            #send_back(dict_register)
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
            user_file2 = open('Userform', 'w') 
            user_file2.write(jsuser_add)
            user_file2.close()
    return dict_register


def run(mysocket,addr):
    ''' 
    recvData = mysocket.recv(1024)
    clients[recvData] = mysocket
    print(clients[recvData])
    '''

    while True:
        recvmsg = mysocket.recv(1024)
        #把接收到的数据进行解码 
        dicData = eval(recvmsg.decode('utf-8'))
        # receive = input()
        print(dicData)

        if dicData['Head'] == 'UserNameList':
            a = relist_all()
            mysocket.send(str(a).encode('utf-8'))
            print(a)
        elif dicData['Head']=='message':
            #community(mysocket)
            recvData = eval(recvmsg.decode('utf-8'))
            sendto = {
                'Head':'message',
                'type':'GET',
                'Src_name':recvData['Src_name'],
                'Dst_name':recvData['Dst_name'],
                'Size':recvData['Size'],
                'msg':recvData['msg']            
            }
            print(sendto)
            clients[recvData['Dst_name']].send(str(sendto).encode("utf-8") )
            print(recvData['Src_name'])
            print(clients[recvData['Src_name']])
        elif dicData['Head']=='file':
            pass
            '''
        def file_message_type(self,file,size,Src_name,Dst_name):
        self.dict['Head']='file'
        self.dict['type']='POST'
        self.dict['Src_name']=Src_name
        self.dict['Dst_name']=Dst_name
        self.dict['file']=file
        self.dict['size']=size
        return self.dict

        needback        
"""
        self.dict['Head']='file'
        self.dict['type']='POST'
        self.dict['Flag']=1/0/2
        self.dict['file']=file
        self.dict['offset']=offset
"""
            '''
        elif dicData['Head']=='quit':
            del_onlist(dicData['Src_name'])
            mysocket.send(str(dicData).encode('utf-8'))
            mysocket.close()
            print('%s logout' % dicData['Src_name'])
            break
        elif recvmsg <= 0:
            del_onlist(dicData['Src_name'])
            mysocket.send(str(dicData).encode('utf-8'))
            mysocket.close()
            print('%s logout' % dicData['Src_name'])
            break            
        else:
            print('error')
        # mysocket.send(str(a).encode('utf-8'))

def start():
    #创建服务端的socket对象socketserver
    socketserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port =28956
    #绑定地址（包括ip地址会端口号）
    socketserver.bind((host, port))
    #设置监听
    socketserver.listen(10)
    #等待客户端的连接
    #注意：accept()函数会返回一个元组
    #元素1为客户端的socket对象，元素2为客户端的地址(ip地址，端口号)
    #mysocket,addr = socketserver.accept()
    while True:# 总父线程
        mysocket,addr = socketserver.accept()
        #接收客户端的请求
        recvmsg = mysocket.recv(1024)
        #把接收到的数据进行解码 
        dicData = eval(recvmsg.decode('utf-8'))

        if dicData['Head'] == 'register':
            print('yes')
            a=register(dicData)
            print(a)
            mysocket.send(str(a).encode('utf-8'))            
        elif dicData['Head'] == 'login':
            a=verify(dicData,addr)
            mysocket.send(str(a).encode('utf-8'))
            print(a)
            if a['Flag'] == 1:
                username = dicData['username']
                clients[username] = mysocket
                t = threading.Thread(target=run, args=(mysocket,addr))
                t.start()
        else:
            pass
    socketserver.close()


def start_S():
    s = threading.Thread(target=start)#启用一个线程开启服务器
    s.start()#开启线程
    #start()    
if __name__ == '__main__':
    start_S()