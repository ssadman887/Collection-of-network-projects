import random as rng
from _thread import *
import time
import socket
import math

class TCPReno:


    serverConn = ('127.0.0.1', 5000)

    PACKET_SIZE = 1460
    MAX_SEQ_NO = (1<<16)

    seqNo = rng.randint(0, MAX_SEQ_NO-1)
    rtt = 0
    cwnd = 1
    ss_threshhold = 8
    sentSize = int(0)
    prevSeqNo =-1
    duplicateAckRcv = 0
    timeout = .7

    def __init__(self):

        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(self.serverConn)

        fileStored = {}
        file_transmission_start = time.time()

        cwndChangeCnt = 0
        cwndTouple = []

        start_new_thread(self.receiveAck, (s,))



    def calculateEWMA(self, prevEWMA, rtt):
        return 0.125 * rtt + (1-.125) * prevEWMA

    def makeTCPPacket(self, packet, seqNo, checksum, lstFlag):
        flag = 0
        flag |= (lstFlag<<0)
        checksum %= (1<<16)
        seqNo %= (1<<16)
        # print("seqNo: ", seqNo, " checksum: ", checksum)
        return seqNo.to_bytes(2, "little") + checksum.to_bytes(2, "little") + flag.to_bytes(1, "little") + packet

    def calculateChecksum(self, packet):
        sum = 0
        packetLen = len(packet)
        if (packetLen %2 != 0): packet = packet + '\0'
        for i in range(packetLen):
            twobytes = packet[i:i+1]
            i += 2
            sum += int.from_bytes(twobytes, "little")
        return sum

    def parseAck(self, ack):
        seqNo = int.from_bytes(ack[:2], "little")
        rwnd = int.from_bytes(ack[2:4], "little")
        return seqNo, rwnd

    def receiveAck(self, s):
        while True:

            global seqNo
            global rtt
            global cwnd
            global ss_threshhold
            global sentSize
            global prevSeqNo
            global duplicateAckRcv
            global timeout
            global cwndTouple
            global cwndChangeCnt

            ack = s.recv(4)

            sentSize = 0
            expectedSeqNo, rwnd = self.parseAck(ack)

            print("ACK RECEIVED")
            print("Expected Seq NO: ", expectedSeqNo, " return window: ", rwnd, " prevAck: ", prevSeqNo)
            print("To be sent seq no: ", seqNo)
            
            if(rwnd < self.PACKET_SIZE): time.sleep(1)
            if (cwnd < ss_threshhold):
                cwnd = min(ss_threshhold, cwnd<<1)
            else:
                cwnd+=1
            if expectedSeqNo != seqNo:
                if expectedSeqNo == prevSeqNo: 
                    duplicateAckRcv+=1
                else:
                    prevSeqNo = expectedSeqNo
                    duplicateAckRcv = 1


            if duplicateAckRcv >= 3:
                duplicateAckRcv = 0
                seqNo = expectedSeqNo
                packet = self.fileStored[expectedSeqNo] if expectedSeqNo in self.fileStored.keys() else self.chunk
                packet = self.makeTCPPacket(packet, seqNo, self.calculateChecksum(packet), sentSize==cwnd)
                self.s.sendall(packet)
                ss_threshhold = math.floor(cwnd / 2)
                cwnd = 1
                print("cwnd changef for triple dupicate ack")

            print("cwnd changed to: ", cwnd)
            cwndTouple.append((cwndChangeCnt, cwnd))
            cwndChangeCnt+=1
            # print((cwndChangeCnt, cwnd))


    

    # with open('tahoe_out', 'w') as log:
    #     log.write("TAHOE")
    #     log.write(cwndChangeCnt)