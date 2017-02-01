# -*- coding: utf-8 -*-
# Auth:xiaoxiaoleo
# https://github.com/xiaoxiaoleo/
# See LICENSE for details


import struct
from array import array
from MysqlDefs import MysqlDefs


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
        #self.m_writer = w
        self.m_writer = log
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

    #returns the byte string for given list 
    def convertListToBytes(self,inList):
        res = []
        for b in inList:
            if type(b) is int:
                b = struct.pack('>I', b)
            res.append(b)
        res = ''.join(res)
        return res

    # returns a Server greeting packet
    #@in: number of the packet
    #@out: packet for the client
    def getGreetingPacket(self,packetNumber):
        packetNumber = self.packetNumber

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
        return packet

    def getPacketError(data,packetNumber,length,errorNumber):
		# 3 byte laenge
        # 3 byte number
        # 0xff fuellbyte
        # 2 byte errocode
        # n String

        dataBack = [0x0 for i in range(len(data)  + 3 + 1 + 1 + 2 )]
        dataBack[0] = hex(data)
	    dataBack[1] = 0x00
		dataBack[2] = 0x00
			
		dataBack[3] = 0x00

		dataBack[4] = 0xff
			
		dataBack[5] = 0x6a
	    dataBack[6] = 0x04

        dataBytes = self.getBytes(data)
        for runner in range(0,len(data)):
            dataBack[7 + runner] = dataBytes[runner]
        return dataBack
			
    def handleLoginPacket(dataIn,clientIP,token,username,host):
		# 3 byte packet laenge
	    # for the moment we ignore the upper two bytes
        length = dataIn[0]
        packetNumber = dataIn[3]
        
        # allocate dummy buffer for the username
        uNameBytes  = [0x0 for i in range(1024)]
        runner = 0x24
        while (runner != len(dataIn) -1 && dataIn[runner] != 0x0):
            uNameBytes[runner-0x24] = dataIn[runner]
            runner = runner + 1
        dataIn[runner - 0x24] = 0x0
        #attack alert 
        outStr = "Login from " + clientIP +  " try with username("+ uNameBytes + ")"
        print outStr

    #generates an OK packet 
    def generateOKPacket(packetNumber,affectedRows):
        log("Info: Starting generation of OK packet with packetnumber " + packetNumber + " and affected rows: " + affectedRows)
        packet  = [0x0 for i in range(11)]
        lengthInPacket = self.convert32To3Byte(7)

        packet = self.copyBytes(lengthInPacket, packet, 0, False)

	    packet[3] = (byte)packetNumber

		packet[4] = 0x0					   # dummy byte	
		packet[5] = (byte)affectedRows	   # affected rows

		packet[6] = 0x2					# server status	
		packet[7] = 0x0					# server status

		packet[8] = 0x0					# warnings
		packet[9] = 0x0					# warnings
		packet[10] = 0x0				# warnings
        
        log("Info: Generated OK packet with packetnumber " + packetNumber + " and affected rows: " + affectedRows)
        return packet
    
    #  retrieve query command
    def handleQueryPacket(dataIn, clientIP,  token,username,  host):
		# 3 byte packet laenge
	    # for the moment we ignore the upper two bytes
        length = dataIn[0]
        packetNumber = dataIn[3]
        
        #allocate dummy buffer for the username
        uNameBytes =  [0x0 for i in range(1024)]
        runner = 0x5
        while (runner != len(dataIn) -1 && dataIn[runner] != 0x0):
            uNameBytes[runner-0x5] = dataIn[runner]
            runner = runner + 1
        dataIn[runner - 0x5] = 0x0
       
        #attack alert 
        log("Query from " + clientIP +  " with command ("  + uNameBytes + ")")
        return uNameBytes

    


