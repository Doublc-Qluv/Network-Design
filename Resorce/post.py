# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 16:13:30 2018

@author: 亓官上
"""

import socket

sk = socket.socket()

ip_port = ('127.0.0.1', 2222)

sk.connect(ip_port)

with open('Tclt.py')