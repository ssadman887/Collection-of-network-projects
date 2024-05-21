import socket
import random as rng
from threading import Timer
import time

serverConn = ('127.0.0.1', 5000)

PACKET_SIZE = 1460
HEADER_SIZE = 5
BUFFER_SIZE = 32 # buffer can hold upto 32 packets
BUFFER_PROCESS_TIME = .1
ERROR_PERCENTAGE = 1
ACK_TIME = .5

packetRecvCnt = 0
packetCorruptCnt = 0

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind(serverConn)
print("Listening to", serverConn)

timerOn = False
buffer = []

def deleteFromBuffer(): 
    buffer.pop(0)

def parseTCPPacket(chunk):
    seq_no = int.from_bytes(chunk[:2], "little")
    checksum = int.from_bytes(chunk[2:4], "little")
    flag = int.from_bytes(chunk[4:5], "little")
    packet = chunk[5:]
    return seq_no, checksum, flag, packet

def verifyChecksum(packet, checksum):
    sum = 0
    packetLen = len(packet)
    if (packetLen %2 != 0): packet = packet + '\0'
    for i in range(packetLen):
        twobytes = packet[i:i+1]
        i += 2
        sum += int.from_bytes(twobytes, "little")
    return checksum == packet

def corruptPacket():
    probability = rng.randrange(0, 10)
    if (probability >= ERROR_PERCENTAGE): return False
    print("+++++++++++++++++++++")
    print("PACKET CORRUPTED")
    print("+++++++++++++++++++++")
    return True

def prepareAck(seqNo):
    print("expected sequence ", seqNo, "Remaining Buffer Cnt: ", abs(BUFFER_SIZE-len(buffer)))
    return seqNo.to_bytes(2, "little") + (PACKET_SIZE * max(0, (BUFFER_SIZE-len(buffer)))).to_bytes(2, "little")

