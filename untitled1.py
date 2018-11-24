# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 14:19:44 2018

@author: happen
"""


from tkinter.messagebox import *
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import font
import tkinter as tk
import time
from time import ctime
import socket as sk
import sys
import threading

class Login_reginster_Page(object):
    def __init__(self,master=None):
        self.root=master   #内部变量
        self.root.geometry('%dx%d'%(300,220))
        self.username=tk.StringVar()
        self.password=tk.StringVar()
        self.LoginPage()
    
    #登陆界面
    def LoginPage(self):
        self.root.title("登陆界面")
        self.page1=tk.Frame(self.root,height=120,width=300)   ##frame框架的大小必须写
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
        self.user=tk.Entry(self.page1,width=18,textvariable=self.username)
        self.user.place(x=70,y=50)
        tk.Label(self.page1,width=6,text='密码').place(x=20,y=100)
        self.pw=tk.Entry(self.page1,width=18,show='*',textvariable=self.password)
        self.pw.place(x=70,y=100)
        tk.Button(self.page2,text='注册',fg='blue',command=self.RegisterChange).place(x=70,y=50)
        tk.Button(self.page2,text='登陆',fg='red',command=self.loginCheck).place(x=180,y=50)
        tk.Label(self.page2,text='请登录',fg='green').place(x=100,y=15)
    
    #注册界面
    def RegisterPage(self):
        self.root.title("注册界面")
        self.page3=tk.Frame(self.root,height=100,width=300)
        self.page3.place(x=0,y=120)
        tk.Button(self.page3,text='登陆',fg='red',command=self.LoginChange).place(x=70,y=50)
        tk.Button(self.page3,text='注册',fg='blue',command=self.RegisterCheck).place(x=180,y=50)
        tk.Label(self.page3,text="*密码至少要有一个小写字母和一个数字，且长度大于4",fg='purple').place(x=2,y=10)
        tk.Label(self.page3,text='请注册',fg='green').place(x=100,y=30)
        
    def LoginChange(self):
        self.page3.destroy()
        self.pw.delete(0,tk.END)
        self.user.delete(0,tk.END)
        self.LoginPage()        
    
    def RegisterChange(self):
        self.page2.destroy()
        self.pw.delete(0,tk.END)
        self.user.delete(0,tk.END)
        self.RegisterPage()
                
    def RegisterCheck(self):
        self.message_content()
        self.dict['Head']='register'
        if self.dict['username'] and self.dict['password']:
            try:
                self.state=send.send_register_login(self.dict)
            except:
                showwarning(title='注册失败',message="网络连接不好")
            else:
                if self.state['Flag']:
                    self.LoginChange()
                    if self.state['content']:
                        showinfo(title="注册成功",message=self.state['content'])
                else:
                    del self.dict
                    if self.state['content']:
                        showerror(title="注册失败！",message=self.state['content'])
        else:
            showerror(message='你没有输入用户名或密码！')
    
    #登陆命令
    def loginCheck(self):
        self.message_content()
        self.dict['Head']='login'     #标识消息类型为：登陆验证消息
        if self.dict['username'] and self.dict['password']:
            try:
                self.state=send.send_register_login(self.dict)
            except:
                showwarning(title='登陆失败',message="网络连接不好")
            else:
                if self.state['Flag']:
                    self.page1.destroy()
                    self.page2.destroy()
                    #time.sleep(1)
                    MainPage(self.root)
                else:
                    del self.dict
                    if self.state['content']:
                        showerror(title="登陆失败！",message=self.state['content'])
        else:
            showerror(title='登陆失败',message='你没有输入用户名或密码！')
            
    #注册登陆消息
    def message_content(self):
        self.dict={}
        self.dict['username']=self.username.get()    #注册或登陆的用户名
        self.dict['password']=self.password.get()    #注册或登陆的密码
        self.dict['time']=ctime()     #注册或登陆时的时间
        self.dict['type']='POST'      #消息类型




#消息发送
class send(object):
    def __init__(self,master=None):
        self.message=master
        self.host='127.0.0.1'
        self.port=28956
        self.addr=(self.host,self.port)
    
    #注册登陆消息发送
    def send_register_login(self):
        self.s=sk.socket(sk.AF_INET,sk.SOCK_STREAM)
        self.s.connect(self.addr)
        self.s.send(self.message.encode('utf-8'))
        self.return_message=self.s.recv(1024)
        return eval(self.return_message.decode('utf-8'))
        
        


#登陆后的界面
class MainPage(object):
    def __init__(self,master=None):
        self.root=master
        self.root.geometry("%dx%d"%(800,600))
        self.root.title("聊天程序实例")
        self.Main_user_Page()
    
    #登陆后的界面设计——————菜单
    def Main_user_Page(self):
        #self.active_user_Page=active_user_frame(self.root)    #创建frame类
        #self.whole_user_Page=whole_user_frame(self.root)
        #self.AboutMe_Page=about_frame(self.root)
        #self.active_user_Page.place(x=0,y=0)
        self.user_page=user_frame(self.root)
        self.AboutMe_Page=About_me(self.root)
        self.user_page.place(x=0,y=0)
        menubar=tk.Menu(self.root)
        menubar.add_command(label='User',command=self.user_data)
        menubar.add_command(label='AboutMe',command=self.about_data)
        self.root['menu']=menubar
    
    #联系人界面    
    def user_data(self):
        self.user_page.place(x=0,y=0)
        self.AboutMe_Page.place_forget()   
        
    #关于该软件 
    def about_data(self):
        self.user_page.place_forget()
        self.AboutMe_Page.place(x=0,y=0)

#联系人界面----消息界面 
class user_frame(tk.Frame):   #继承frame类
    def __init__(self,master=None):
        tk.Frame.__init__(self,master,width=800,height=600)
        self.root=master
        self.user__list_frame=tk.Frame(self)
        self.user__list_frame.pack(side=tk.LEFT,fill='y',expand=1)
        self.var=tk.StringVar()
        self.message_page=[]
        self.active_user=['aaaa','bbb','ccc']
        self.whole_user=['1111','2222','3333','aaaa','bbb','ccc','4444','5555','6666','777','888','999','wwwww','wdwwd','ef','as','cd','dcd','ddcd','cd1','wwwwwhh']
        self.Main_active_Page()
        #self.after(5000,self.send_user_data)
        #self.after(5000,self.user_name_updata)        
    
    #联系人框
    def Main_active_Page(self):
        #self.ft=font.Font(size=20,weight='bold')
        self.user_list=tk.Listbox(self.user__list_frame,height=21,selectmode=tk.BROWSE,listvariable=self.var,font=('Fixdsys',20))
        self.user_list.pack(side=tk.LEFT,fill='y',expand=1) 
        self.user_name_updata()
        self.user_list.bind("<ButtonRelease-1>",self.change_send_message_user)
        self.user_bar=tk.Scrollbar(self.user__list_frame)
        self.user_bar.pack(side=tk.RIGHT,fill=tk.Y)
        self.user_list.configure(yscrollcommand=self.user_bar.set)
        self.user_bar['command']=self.user_list.yview
        self.message_update()
    
    #联系人的框更新
    def user_name_updata(self):
        for user in self.whole_user:
            if user not in self.var.get():
                self.message_page.append(message_frame(self,user))
                if user in self.active_user:
                    self.user_list.insert(0,user+"  <active>")
                else:
                    self.user_list.insert(tk.END,user+"  <Noactive>")
        self.after(5000,self.user_name_updata)
    
    #点击切换联系人（或用户）
    def change_send_message_user(self,event):    #event的作用
        for i in self.user_list.curselection():
            print(self.user_list.get(i))
            #page=message_frame(self,self.user_list.get(i).split()[0])
            self.message_page[i].pack(side=tk.RIGHT)
            for j in range(len(self.whole_user)):
                if j!=i:
                    self.message_page[j].pack_forget()
    
    #向服务器请求更新用户信息
    def require_user_data(self):
        self.active_user=['aaaa','bbb','ccc']
        self.whole_user=['1111','2222','3333','aaaa','bbb','ccc']
        self.after(5000,self.require_user_data)
    
    #向服务器更新消息
    def message_update(self):
        #self.message_page[1].sh
        #time.sleep(10)
        self.message_page[1].message_list.insert(tk.END,ctime())
        self.message_page[1].show_message_frame.after(10000,self.message_update)

#消息框与文本框界面设计
class message_frame(tk.Frame):
    def __init__(self,master=None,name=None,height=100):
        tk.Frame.__init__(self,master)
        self.frame=master
        self.user_name=name
        self.Main_message_page()
    
    #消息框与文本框界面    
    def Main_message_page(self):
        self.show_message_frame=tk.LabelFrame(self,text=self.user_name,width=200,height=600)
        self.message_bar=tk.Scrollbar(self.show_message_frame)
        self.message_bar.pack(side=tk.RIGHT,fill=tk.Y,expand=1)
        self.message_list=tk.Listbox(self.show_message_frame,width=47,height=17,selectmode=tk.BROWSE,font=('Fixdsys',15))
        self.message_list.configure(yscrollcommand=self.message_bar.set)
        self.message_list.pack(anchor=tk.W,fill=tk.Y,expand=1)
        self.message_bar['command']=self.message_list.yview()
        self.show_message_frame.pack(anchor=tk.W,side=tk.TOP)       #顺序
        self.button_send=tk.Button(self,text='send',fg='blue',command=self.send_messsage_command)
        self.button_send.pack(side=tk.BOTTOM,anchor=tk.E)
        self.text=scrolledtext.ScrolledText(self,width=68,height=11,wrap=tk.WORD)
        self.text.pack(side=tk.BOTTOM)
        self.file_button=tk.Button(self,text='file',fg='blue',height=1,width=4,command=self.openfile)   #dia
        self.file_button.pack(side=tk.BOTTOM,anchor=tk.W)
    
    #发文件命令
    def openfile(self):
        #显示打开文件对话框，返回文件名以及路径
        r=filedialog.askopenfilename(title='选择文件',filetypes=[('Python','*.py *.pyw'),('All Files','*')])
        print(r)
    
    #发消息命令
    def send_messsage_command(self):
        self.message=self.text.get(0.0,tk.END)
        self.message_list.insert(tk.END,"%s"%ctime().rjust(40))
        self.message_list.insert(tk.END,self.user_name+":"+self.message)
        self.text.delete(0.0,tk.END)
        
class About_me(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.Main_AboutMe_page()
        
    def Main_AboutMe_page(self):
        tk.Label(self,text='正在更新！'.rjust(30),font=('Fixdsys',20),fg='red').pack(side=tk.TOP,anchor=tk.N)
        tk.Button(self,text='qiut',command=self.page_close).pack()
        
    def page_close(self):
        #sys.exit()
        pass


if __name__=="__main__":
    root=tk.Tk()
    Login_reginster_Page(root)
    #MainPage(root)
    root.mainloop()
        
