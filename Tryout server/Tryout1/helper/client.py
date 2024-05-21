import os
import struct
import socket
import pickle
from time import sleep
# import helper.TCPReno as TCPReno

# TCPReno = TCPReno.TCPReno()
connectConfig = ('127.0.0.1', 5050)

def createPicklePakcet(object) -> bytes:
    data = pickle.dumps(object)
    length = struct.pack('!I', len(data))
    data = length + data
    return data

def saveToFile(username, filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        clientSocket.connect(connectConfig)

        data = createPicklePakcet({
            "username": username,
            "type": "download",
            "filename": filename
        })

        clientSocket.send(data)

        savedir = f'saves/{filename}'
        print(savedir)
        with open(savedir, "wb") as f:
            while True:
                recvData = clientSocket.recv(1024)
                # print(recvData)

                if len(recvData) == 0: break
                if recvData == b'Unable to locate the file': 
                    os.remove(savedir)
                    break
                f.write(recvData)
            print("done")

def getDir(username, filename = None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        clientSocket.connect(connectConfig)

        data = createPicklePakcet({
            "username": username,
            "type": "get_dir",
            "filename": filename
        })

        clientSocket.send(data)

        dir = b''
        while True:
            recvData = clientSocket.recv(1024)
            if len(recvData) == 0: break
            dir = dir + recvData
        dir = pickle.loads(dir)
        # print(dir)
        return dir
    
def uploadFile(username, file):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
        clientSocket.connect(connectConfig)

        data = createPicklePakcet({
            "username": username,
            "type": "upload",
            "filename": file.filename
        })

        clientSocket.send(data)
        sleep(1)

        for byte in file:
            clientSocket.send(byte)
