# -*- coding: utf-8 -*-
# Auth:xiaoxiaoleo
# https://github.com/xiaoxiaoleo/
# See LICENSE for details

import socket

State = {   'NOT_CONNECTED': 1,
	    	'GREETING_PACKET_SEND' : 2,
			'LOGIN_OK' : 3,
			'FINISH': 666    }

class MySqlServer:
    def __init__(self,port,  fileName,   ip):
		self.m_socket = null
		self.m_state = State['NOT_CONNECTED']
		self.m_writer = null
		self.readBytes = 0
		self.data = new byte[1024]
		self.m_port = 3306
		self.m_fileName = ""
		self.m_ip = null
		
        self.m_ip = ip
        self.m_port = port 
        self.m_fileName = fileName
        self.m_writer = open(filename,'a')

    # calculate own IP address
    def getMyIP():
        if (m_ip != null):
				return m_ip                
        else:
            return socket.gethostbyname(socket.gethostname())
