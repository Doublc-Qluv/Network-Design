# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 15:33:40 2018

@author: happen
"""


import tkinter as tk
import socket as sk
from time import ctime

register=tk.Tk()
register.title('注册页面')
register.geometry('400x300')
label1=tk.Label(register,text='欢迎注册我们的应用！').pack()
#用户名框
tk.Label(register,text='请输入你的用户名').place(x=1,y=30)
tk.Label(register,width=6,text='用户名').place(x=1,y=50)
username=tk.Entry(register,width=30,fg='blue')
username.place(x=50,y=50)
#密码框
tk.Label(register,text='请输入你的密码！').place(x=1,y=80)
tk.Label(register,width=6,text='密码').place(x=1,y=100)
password=tk.Entry(register,width=30,show='*',fg='green')
password.place(x=50,y=100)

def send_register(dict):
    host='127.0.0.1'
    port=28956
    addr=(host,port)
    s=sk.socket(sk.AF_INET,sk.SOCK_STREAM)
    s.connect(addr)
    s.send(str(dict).encode('utf-8'))



def register_command():
    user=username.get()
    pw=password.get()
    if user and pw:
        dict={}
        dict['head']=0
        dict['username']=user
        dict['password']=pw
        dict['time']=ctime()
        state=send_register(dict)
        #if int(state.decode)==1:
         #   print('ok')
    else:
        warn=tk.Label(register,text='你没有输入用户名和密码，请输入用户名和密码！').place(x=40,y=130)
        


#按钮

tk.Button(register,text='注册',width=8,command=register_command).place(x=100,y=200)
tk.Button(register,text='取消',width=9).place(x=180,y=200)

register.mainloop()