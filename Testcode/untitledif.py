# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 14:19:44 2018

@author: happen
"""

import tkinter as tk
from time import ctime
import socket as sk
from tkinter.messagebox import *


class Login_reginster_Page(object):
    def __init__(self,master=None):
        self.root=master   #内部变量
        self.root.geometry('%dx%d'%(300,220))
        self.username=tk.StringVar()
        self.password=tk.StringVar()
        self.LoginPage()
    
    def LoginPage(self):
        self.root.title("登陆界面")
        self.page1=tk.Frame(self.root,height=120,width=300)
        self.page1.place(x=0,y=0)
        self.page2=tk.Frame(self.root,height=100,width=300)
        self.page2.place(x=0,y=120)
        ##滚动标题
        self.remove=0
        self.colour=['green','blue','red','organe','yellow','purple']
        #self.page1['bg']=colour[x]
        title=tk.Label(self.page1,text='欢迎使用我们的聊天应用！')
        def foo():
            self.remove=self.remove+10
            if self.remove>300:
                self.remove=0
            title.place(x=self.remove,y=8)
            title['fg']=self.colour[self.remove%(len(self.colour))]
            self.page1.after(500,foo)
        self.page1.after(500,foo)
        tk.Label(self.page1,width=6,text='用户名').place(x=20,y=50)
        tk.Entry(self.page1,width=18,textvariable=self.username).place(x=70,y=50)
        tk.Label(self.page1,width=6,text='密码').place(x=20,y=100)
        tk.Entry(self.page1,width=18,show='*',textvariable=self.password).place(x=70,y=100)
        tk.Button(self.page2,text='注册',fg='blue',command=self.RegisterChange).place(x=70,y=50)
        tk.Button(self.page2,text='登陆',fg='red',command=self.loginCheck).place(x=180,y=50)
        tk.Label(self.page2,text='请登录',fg='green').place(x=100,y=15)
        
    def RegisterPage(self):
        self.root.title("注册界面")
        self.page3=tk.Frame(self.root,height=100,width=300)
        self.page3.place(x=0,y=120)
        tk.Button(self.page3,text='登陆',fg='red',command=self.LoginChange).place(x=70,y=50)
        tk.Button(self.page3,text='注册',fg='blue',command=self.RegisterCheck).place(x=180,y=50)
        tk.Label(self.page3,text='请注册',fg='green').place(x=100,y=15)
        
    def LoginChange(self):
        self.page3.destroy()
        self.LoginPage()
    
    def RegisterChange(self):
        self.page2.destroy()
        self.RegisterPage()
        
    def message(self):
        self.dict={}
        self.dict['username']=self.username.get()
        self.dict['password']=self.password.get()
        self.dict['time']=ctime()
        
    def RegisterCheck(self):
        self.message()
        self.dict['Head']='register'
        if self.dict['username'] and self.dict['password']:
            try:
                state=send(self.dict)
            except:
                showwarning(title='注册失败',message="网络连接不好")
            else:
                if state:
                    self.LoginChange()
                    showinfo("注册成功，请登陆！")
                else:
                    del self.dict
                    showerror(title="注册失败！",message="你的用户名和密码不符合我规则！")
        else:
            showerror(message='你没有输入用户名或密码！')
    
    
    def loginCheck(self):
        self.message()
        self.dict['Head']='login'
        if self.dict['username'] and self.dict['password']:
            try:
                state=send(self.dict)
            except:
                showwarning("网络连接不好")
            else:
                if state:
                    self.page1.destroy()
                    self.page2.destroy()
                    MainPage(self.root)
                else:
                    del self.dict
                    showerror(title="登陆失败！",message="你的用户名或密码错误！")
        else:
            showerror(message='你没有输入用户名或密码！')

        
def send(dict):
    host='127.0.0.1'
    port=28956
    addr=(host,port)
    s=sk.socket(sk.AF_INET,sk.SOCK_STREAM)
    s.connect(addr)
    s.send(str(dict).encode('utf-8'))
    return 1
     
root=tk.Tk()
Login_reginster_Page(root)
MainPage(root)
root.mainloop()
        



