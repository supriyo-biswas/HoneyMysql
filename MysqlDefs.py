# -*- coding: utf-8 -*-
# Auth:xiaoxiaoleo
# https://github.com/xiaoxiaoleo/
# See LICENSE for details

class MysqlDefs:
    def __init__(self,):
        self.serverVersion = "5.5.15" # + 1 for termination
        self.threadID = "1234"
        self.pluginData  = "mysql_native_password"
        #self.scrambleBuf = [11,22,33,44,55,66,77,88]
        self.scrambleBuf = [0x0B,0x16,0x21,0x2C,0x37,0x42,0x4D,0x58]
        #self.filler = [0,0,0,0,0,0,0,0,0,0]
        self.filler = [0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0]
        self.filler12  = [0x42, 0x42, 0x42, 0x42, 0x42, 0x42, 0x42, 0x42, 0x42, 0x42, 0x42, 0x42]
        self.protocolVersion = 0xa

    def getServerVersion(self,):
        return self.serverVersion

    def getThreadID(self,):
        return self.threadID

    def getPluginData(self,):
        return self.pluginData

    def getScrambleBuf(self,):
        return self.scrambleBuf

    def getFiller(self,):
        return self.filler

    def getFiller12(self,):
        return self.filler12

    def getProtocolVersion(self,):
        return self.protocolVersion


