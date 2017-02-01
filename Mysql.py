# -*- coding: UTF-8 -*-
# Auth:xiaoxiaoleo

import struct
from array import array
import time


def log(info):
    try:
        info = str(info)
        time_str = time.strftime('%X', time.localtime(time.time()))
        print "[%s] %s" % (time_str, info)
        f = open('run_log.txt','a')
        f.write("[%s] %s \n" % (time_str, info) )
        f.close()
    except:
        pass



class Mysql:
    def __init__(self,packetNumber,w):
        self.m_packetNumber = packetNumber
        self.m_writer = w
        self.m_mysqlDefs = MysqlDefs()

    #converts an 32 bit value to a 3 byte array
    def convert32To3Byte(self,Int32):
        destPacket = []
        for i in range(0,3):
            destPacket.append(list(struct.pack("<I", Int32))[i])
        return destPacket

    def copyBytes(self,source,dest,offsetDest,nullTerminated):
        runner = 0
        for runner in range(0,len(source)):
            dest[runner + offsetDest] = source[runner]
        #if null termination is requiredm fullfull the need
        if(nullTerminated):
            dest[runner + offsetDest]  = 0x0
        return dest

    #returns the byte array for a given string
    def getBytes(self,inStr):
        #hex_data = inStr.decode("hex")
        #return list(hex_data)
        a = array("B",inStr)
        return map(hex, a)

    #returns 
    def convertListToBytes(self,inList):
        res = []
        for b in inList:
            if type(b) is int:
                b = struct.pack('>I', b)
            res.append(b)
        res = ''.join(res)
        return res


    def getGreetingPacket(self,packetNumber):
        #create packet and fill it with dummy bytes to attack programming mistake
        length = len(self.m_mysqlDefs.getServerVersion()) + 1 + 1 + 4 + 8 + 1+ 2+ 1+ 2 +2 +  1 + 10+ 1 + 12 + 1 + len(self.m_mysqlDefs.getPluginData())

        packet = [0x0 for i in range(length + 4)]
        #log(packet)

        # 3 byte laenge
        # 1 byte packet nummer
        lengthInPacket = self.convert32To3Byte(length)
        #print lengthInPacket
        packet = self.copyBytes(lengthInPacket,packet,0,False)
        packet[3] = hex(packetNumber)
        #log(packet)

        # copy protocol version
        packet[4] = self.m_mysqlDefs.getProtocolVersion()
        packet = self.copyBytes(self.getBytes(self.m_mysqlDefs.getServerVersion()), packet, 5, True)
        #log(packet)

        # calculate offset for thread id including null terminated length of serverversion
        offset = len(self.m_mysqlDefs.getServerVersion()) + 6
        packet = self.copyBytes(self.getBytes(self.m_mysqlDefs.getThreadID()), packet, offset, False)
        offset = offset + 4
        #log(packet)

        # copy scramble buf
        packet = self.copyBytes(self.m_mysqlDefs.getScrambleBuf(), packet, offset, True)
        offset = offset  + 9
        #log(packet)

        # hardcoded server capabilities
        offset = offset  + 1
        packet[offset] = 0xff
        offset = offset  + 1
        packet[offset] = 0xf7
        #log(packet)

        # hardcoded server language
        offset = offset  + 1
        packet[offset] = 0x8

        # hardcoded server status
        offset = offset  + 1
        packet[offset] = 0x02
        offset = offset  + 1
        packet[offset] = 0x00

        # hardcoded server capabilities (upper two bytes)
        offset = offset  + 1
        packet[offset] = 0xf
        offset = offset  + 1
        packet[offset] = 0x80

        # length of the scramble
        offset = offset  + 1
        tmp = len(self.m_mysqlDefs.getPluginData())
        packet[offset] =  struct.pack("<I", tmp)


        # copy filler buf
        packet = self.copyBytes(self.m_mysqlDefs.getFiller(), packet, offset, False)
        offset = offset  + 10

        # copy filler buf
        packet = self.copyBytes(self.m_mysqlDefs.getFiller12(), packet, offset, True)
        offset = offset  + 13

        # copy pluginData buf
        packet = self.copyBytes(self.getBytes(self.m_mysqlDefs.getPluginData()), packet, offset, True)
        offset = offset  + 10

        # fix internal packetnumber
        m_packetNumber = self.m_packetNumber + 1
        
        #log(res)
        return convertListToBytes(packet)

if __name__ == "__main__":
    print 'Lets start'
    t = Mysql(0,'test.log')
    print t.getGreetingPacket(0)
