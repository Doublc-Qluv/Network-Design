# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 14:19:44 2018

@author: happen
"""
from tkinter import messagebox as tk_msg
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
import os

class Login_reginster_Page(object):
    def __init__(self,master=None):
        self.root=master   #内部变量
        self.root.geometry('%dx%d'%(300,220))
        self.username=tk.StringVar()
        self.password=tk.StringVar()
        self.service_socket=None
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
        #滚动标题的动态效果
        def foo():
            self.remove=self.remove+10
            if self.remove>300:
                self.remove=0
            title.place(x=self.remove,y=8)
            title['fg']=self.colour[self.remove%(len(self.colour))]
            self.page1.after(500,foo)
        self.page1.after(500,foo)
        #登陆框界面设计
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
        self.dict=require_data_type().registr_type(self.username.get(),self.password.get())
        if self.dict['username'] and self.dict['password']:
            try:
                #self.state=send.send_register_login(self.dict)    这种类的函数引用错去
                #a=send(self.dict)
                #self.state=a.send_register_login()
                #self.state=a.return_message
                self.state=send_register_login(self.dict).register_updata()
                print(self.state)
            except:
                tk_msg.showwarning(title='注册失败',message="网络连接不好")
            else:
                if self.state['Flag']:
                    self.LoginChange()
                    if self.state['content']:
                        tk_msg.showinfo(title="注册成功",message=self.state['content'])
                else:
                    #注册失败后，清空消息框，和已经发送消息内容
                    del self.dict
                    self.pw.delete(0,tk.END)
                    self.user.delete(0,tk.END)
                    if self.state['content']:
                        tk_msg.showerror(title="注册失败！",message=self.state['content'])
        else:
            tk_msg.showerror(message='你没有输入用户名或密码！')
    
    #登陆命令
    def loginCheck(self):
        self.dict=require_data_type().login_type(self.username.get(),self.password.get())
        if self.dict['username'] and self.dict['password']:
            try:
                #self.state=send(self.dict)    这种也错误，类本身没有返回值
                #self.state=send(self.dict).send_register_login()                
                self.state,self.service_socket=send_register_login(self.dict).login_updata()
                #类的函数两种不同的引用方式
            except:
                tk_msg.showwarning(title='登陆失败',message="网络连接不好")
            else:
                if self.state['Flag']:
                    self.page1.destroy()
                    self.page2.destroy()
                    #time.sleep(2)
                    MainPage(self.root,self.service_socket,self.username)
                else:
                    #登陆失败后，清空消息框，和已经发送消息的内容
                    del self.dict
                    self.pw.delete(0,tk.END)
                    self.user.delete(0,tk.END)
                    if self.state['content']:
                        tk_msg.showerror(title="登陆失败！",message=self.state['content'])
        else:
            tk_msg.showerror(title='登陆失败',message='你没有输入用户名或密码！')

#与服务器通信进行注册和登陆
class send_register_login(object):
    def __init__(self,master=None):
        self.message=str(master)
        self.host='127.0.0.1'
        self.port=28956
        self.addr=(self.host,self.port)
        self.service_socket=None
        #self.send_register_login()
    
    #登陆消息发送
    def login_updata(self):
        self.s=sk.socket(sk.AF_INET,sk.SOCK_STREAM)
        self.s.connect(self.addr)
        self.s.send(self.message.encode('utf-8'))
        self.return_message=eval(self.s.recv(1024).decode('utf-8'))
        self.service_socket=self.s
        return self.return_message,self.service_socket

    #注册消息发送
    def register_updata(self):
        self.s=sk.socket(sk.AF_INET,sk.SOCK_STREAM)
        self.s.connect(self.addr)
        self.s.send(self.message.encode('utf-8'))
        self.return_message=eval(self.s.recv(1024).decode('utf-8'))
        self.s.close()
        self.service_socket=None
        return self.return_message

#登陆后的界面
class MainPage(object):
    def __init__(self,master=None,service_socket=None,myself=None):
        self.service_socket=service_socket
        self.root=master
        self.myself_name=myself
        self.root.geometry("%dx%d"%(800,600))
        self.root.title("聊天程序实例")
        self.Main_user_Page()
    
    #登陆后的界面设计——————菜单
    def Main_user_Page(self):
        #self.active_user_Page=active_user_frame(self.root)    #创建frame类
        #self.whole_user_Page=whole_user_frame(self.root)
        #self.AboutMe_Page=about_frame(self.root)
        #self.active_user_Page.place(x=0,y=0)
        self.user_page=user_frame(self.root,self.service_socket,self.myself_name)
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
    def __init__(self,master=None,service_socket=None,myself=None):
        tk.Frame.__init__(self,master,width=800,height=600)
        self.root=master
        self.myself_name=myself
        self.user__list_frame=tk.Frame(self)
        self.user__list_frame.pack(side=tk.LEFT,fill='y',expand=1)
        self.var=tk.StringVar()
        self.message_page=[]
        self.active_user=[]
        self.whole_user=[]
        #与服务器联系的socket
        self.service_socket=service_socket
        self.Main_active_Page()
               
    
    #联系人框
    def Main_active_Page(self):
        #self.ft=font.Font(size=20,weight='bold')
        self.user_list=tk.Listbox(self.user__list_frame,height=21,selectmode=tk.BROWSE,listvariable=self.var,font=('Fixdsys',20))
        self.user_list.pack(side=tk.LEFT,fill='y',expand=1) 
        self.user_list.bind("<ButtonRelease-1>",self.change_send_message_user)
        self.user_bar=tk.Scrollbar(self.user__list_frame)
        self.user_bar.pack(side=tk.RIGHT,fill=tk.Y)
        self.user_list.configure(yscrollcommand=self.user_bar.set)
        self.user_bar['command']=self.user_list.yview
        self.updata()

    #运行更新
    def updata(self):
        #运行线程---联系人在线情况更新
        self.updata_message_thread=threading.Thread(target=self.message_update)
        self.updata_message_thread.start()
        time.sleep(1)
        self.update_user_thread=threading.Thread(target=self.require_user_data)
        self.update_user_thread.start()


         
    #联系人的框更新
    def user_name_list_updata(self):
        print('0',self.active_add,self.active_delete)
        print('1',self.whole_add,self.whole_delete)
        for user in self.whole_add:
            #新的用户注册
            #print('11',user)
            self.user_list.insert(tk.END,user+"  <Noactive>")
            self.message_page.append(message_frame(self,user,self.myself_name))
        for user in self.whole_delete:
            #当用户从注销该账号
            for i in range(len(eval(self.var.get()))):
                if eval(self.var.get())[i].split(' ')[0]==user:
                    self.user_list.delete(i)
                    del self.message_page[i]
                    break
        for user in self.active_add:
            #用户又非在线状态变为在线状态
            #print(self.var.get())
            #print('size:',len(self.var.get()))
            #print('type:',type(eval(self.var.get())))
            for i in range(len(eval(self.var.get()))):
                #print(i)
                #print(self.var.get())
                #print(self.var.get()[i])
                #print(self.var.get()[i].split(' ')[0])
                if eval(self.var.get())[i].split(' ')[0]==user:
                    #print('00',self.var.get()[i])
                    self.user_list.delete(i)
                    del self.message_page[i]
                    self.user_list.insert(0,user+"  <active>")
                    self.message_page.insert(0,message_frame(self,user,self.myself_name))
                    break
        for user in self.active_delete:
            #用户有在线状态变为非在线状态
            for i in range(len(eval(self.var.get()))):
                if eval(self.var.get())[i].split(' ')[0]==user:
                    self.user_list.delete(i)
                    del self.message_page[i]
                    self.user_list.insert(tk.END,user+"  <Noactive>")
                    self.message_page.append(message_frame(self,user,self.myself_name))
                    break

                        
                
    #向服务器请求更新用户信息
    def require_user_data(self):
        #print(require_data_type().user_name_updata_type())
        network_send_message(self.service_socket,require_data_type().user_name_updata_type()).user_name_updata()
        #print(require_data_type().user_name_updata_type())
        self.user__list_frame.after(5000,self.require_user_data)
    
    #点击切换联系人（或用户）
    def change_send_message_user(self,event):    #event的作用
        for i in self.user_list.curselection():
            print("1")
            #print(self.user_list.get(i))
            #page=message_frame(self,self.user_list.get(i).split()[0])
            self.message_page[i].pack(side=tk.RIGHT)
            for j in range(len(self.whole_user)):
                if j!=i:
                    self.message_page[j].pack_forget()
    
    #向服务器发送更新消息
    def message_update(self):
        while True:
            try:
                self.message=network_reciver_meaasge(self.service_socket).return_message
            except:
                tk_msg.showinfo(title='网络连接不好',message='请检查你的网络，或服务器是否正常使用')
            else:
                #print(self.message)
                if self.message['Head']=='message':
                    #更新消息
                    for i in self.whole_user:
                        if i==self.message['Src_name']:
                            self.message_page[i].message_list.insert(tk.END,ctime())
                elif self.message['Head']=='UserNameList':
                    #更新联系人
                    self.active_add,self.active_delete=set(eval(self.message['ActiveUserList']))-set(self.active_user),set(self.active_user)-set(eval(self.message['ActiveUserList']))
                    self.active_user=eval(self.message['ActiveUserList'])  
                    #print(self.active_user)
                    self.whole_add,self.whole_delete=set(eval(self.message['WholeUserList']))-set(self.whole_user),set(self.whole_user)-set(eval(self.message['WholeUserList']))
                    self.whole_user=eval(self.message['WholeUserList'])
                    self.user_name_list_updata()
                elif self.message['Head']=='file':
                    pass
        #self.message_page[i].show_message_frame.after(500,self.message_update)



#消息框与文本框界面设计
class message_frame(tk.Frame):
    def __init__(self,master=None,name=None,service_socket=None,myself=None,height=100):
        tk.Frame.__init__(self,master)
        self.frame=master
        self.user_name=name
        self.service_socket=service_socket
        self.myself_name=myself
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
        self.filename=filedialog.askopenfilename(title='选择发送的文件',filetypes=[('Python','*.py *.pyw'),('All Files','*')])
        self.size=os.path.getsize(r)
        self.message=require_data_type().file_message_type(self.filename,self.size,self.myself_name,self.user_name)
        p=network_send_message(self.service_socket,self.message).send_file_message()
        self.file_send_thread=threading.Thread(target=p.send_file_message)
        self.file_send_thread.start()
        print(r)
    
            
    #发消息命令
    def send_messsage_command(self):
        self.message=self.text.get(0.0,tk.END)
        self.dict=require_data_type().message_type(self.user_name,self.myself_name,self.message)
        try:
            network_send_message(self.service_socket,self.dict).send_message()
        except:
            tk_msg.showerror(title='发送失败',message='发送失败')
        else:
            self.message_list.insert(tk.END,"%s"%ctime().rjust(35))
            self.message_list.insert(tk.END,self.user_name+":"+self.message)
            self.text.delete(0.0,tk.END)
####当发送与其他如联系人更新时冲突是，会发生什么     不会冲突，因为发送和接受是不同的线程     
        
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



#登陆后与服务器进行发送消息
#class network_message(object):
class network_send_message(object):    
    def __init__(self,master=None,message=None):
        self.service_socket=master
        self.message=message
    
    def user_name_updata(self):
        self.service_socket.send(str(self.message).encode('utf-8'))
        #self.return_message=eval(self.service_socket.recv(1024).decode('utf-8'))
        #return self.return_message

    def send_message(self):
        self.service_socket.send(str(self.message).encode('utf-8'))

    
    def send_file_message(self):
        self.service_socket.send(str(self.message).encode('utf-8'))

#登陆后服务器接受消息
class network_reciver_meaasge(object):
    def __init__(self,master=None):
        self.service_socket=master
        self.message=self.reciver_message()
        
    def reciver_message(self):
        self.return_message=eval(self.service_socket.recv(1024).decode('utf-8'))
        return self.return_message

#向服务器请求的数据类型
class require_data_type(object):
    def __init__(self):
        self.dict={}

    #请求联系人消息
    def user_name_updata_type(self):
        self.dict['Head']='UserNameList'
        self.dict['type']='POST'
        return self.dict

    #通信信息信息
    def message_type(self,Src_name,Dst_name,msg):
        self.dict['Head']='message'
        self.dict['type']='POSt'
        self.dict['Src_name']=Src_name
        self.dict['Dst_name']=Dst_name
        self.dict['msg']=msg
        self.dict['Size']=sys.getsizeof(str(self.dict).encode('utf-8'))   #一个对象的字节大小
        return self.dict
    
    #登陆消息
    def login_type(self,username,password):
        self.dict['Head']='login'
        self.dict['username']=username    #注册或登陆的用户名
        self.dict['password']=password    #注册或登陆的密码
        self.dict['time']=ctime()     #注册或登陆时的时间
        self.dict['type']='POST'      #消息类型        
        return self.dict

    #注册消息
    def registr_type(self,username,password):
        self.dict['Head']='register'
        self.dict['username']=username    #注册或登陆的用户名
        self.dict['password']=password    #注册或登陆的密码
        self.dict['time']=ctime()     #注册或登陆时的时间
        self.dict['type']='POST'      #消息类型 
        return self.dict
    
    def file_message_type(self,file,size,Src_name_Dstname):
        self.dict['Head']='file'
        self.dict['type']='POST'
        self.dict['Src_name']=Src_name
        self.dict['Dst_name']=Dst_name
        self.dict['file']=file
        self.dict['size']=size
        return self.dict


"""
        self.dict['Head']='file'
        self.dict['type']='POST'
        self.dict['Flag']=1/0/2
        self.dict['file']=file
        self.dict['offset']=offset
"""

class file_send(object):
    def __init__(self,file=None,service_socket=None,offset=None):
        self.file=file
        self.service_socket=service_socket
        self.offset=offset
    
    #发送文件
    def send(self):
        with open(self.file) as fd:
            read_lenght=0
            while True:
                send_data=fd.read(1024)
                if send_data and read_lenght>int(self.offset):
                    ack_msg='SEND SIZE|%s'%len(send_data)
                    self.service_socket.send(ack_msg.encode('utf-8'))
                    self.client_ack=self.service_socket.recv(1024).decode('utf-8')
                    if self.client_ack=='ready':
                        try:
                            self.service_socket.send(send_data)
                        except:
                            pass
                        else:
                            read_lenght=+len(send_data)                                
                elif read_lenght<=int(self.offset):
                    continue
                else:
                    send_data='END'
                    self.service_socket.send(send_data.encode('utf-8'))
                    self.ack=self.service_socket.recv(1024).decode('utf-8')
                    if self.ack=='ok':
                        break
                    else:
                        pass
"""
    def reciver_message(self):
        while True:
            self.return_message=eval(self.service_socket.recv(1024).decode('utf-8'))
            if self.return_message['Head']=='':
                pass
            elif self.return_message['Head']=='':
                pass
            else:
                pass
        return self.return_message
        
        

        self.service_socket.send('%s:%d'%(self.filename,self.size).encode('utf-8'))  #发送文件名和文件大小
        self.if_has=self.service_socket.recv(1024).decode('utf-8')
        if self.if=='no':
            
        sys_msg=1     #接受偏移量
 """       
filepath='' 
class file_revicer(object):
    def __init__(self,filename=None):
        self.filename=filename
        
        self.service_socket=service_socket
        #得到文件名和文件路径
        #self.filepath=os.path.dirname(self.file)
        #self.filename=os.path.basename(self.file)
        self.filepath,self.filename=os.path.split(self.file)
        self.size=os.path.getsize(self.file)
       
        
        

if __name__=="__main__":
    root=tk.Tk()
    Login_reginster_Page(root)
    #MainPage(root)
    root.mainloop()
        

