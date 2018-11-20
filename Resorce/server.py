import socket
import sys, os
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
    if strData['head']==0:
        print(strData)  

        # 判断用户
        i=0
        while True:                                                        #只要用户登录异常不超过3次就不断循环
            name = strData['username']
            passwd = strData['password']
            lock_file = open('account_lock.txt','r+')                       #当用户输入用户名后，打开LOCK 文件 以检查是否此用户已经LOCK了
            lock_list = lock_file.readlines()

            for lock_line in lock_list:                                     #循环LOCK文件 
                lock_line = lock_line.strip('\n')                           #去掉换行符
                if name == lock_line:                                       #如果LOCK了就直接退出
                    sys.exit('用户 %s 已经被锁定，退出' % name)  

            user_file = open('account.txt','r')                             #打开帐号文件 
            user_list = user_file.readlines()                               
            for user_line in user_list:                                     #对帐号文件进行遍历
                (user,passwords) = user_line.strip('\n').split()             #分别获取帐号和密码信息
                
                
                if name == user: 
                    j=0
                    
                    if passwd == passwords:                                       #如用户名正常匹配
                        print(" %s 登陆成功" % name)
                        print
                else:
                    print('用户 %s 不存在，退出' % name)                           #用户输入三次错误后，异常退出
            i += 1
            if i>3:
                break        
        lock_file.close()                                                   #关闭LOCK文件
        user_file.close()
        #msg = input("回复:")
        #对要发送的数据进行编码
        #msg=1
        #clientsocket.send(str(name).encode("utf-8"))
    else:
        break
socketserver.close()
