import socket
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
while 1:
    clientsocket,addr = socketserver.accept()


    recvmsg = clientsocket.recv(1024)
    #把接收到的数据进行解码
    strData = eval(recvmsg.decode("utf-8"))
#判断客户端是否发送q，是就退出此次对话

    print("收到:",strData)
#msg = input("回复:")
#对要发送的数据进行编码
#msg=1
#clientsocket.send(str(msg).encode("utf-8"))

socketserver.close()
