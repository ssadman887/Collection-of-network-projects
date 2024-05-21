import socket
import struct
import pickle
import os
from _thread import start_new_thread
from fileext import file_extension_map as file_map
from hurry.filesize import size
from time import sleep
import TCPReno
from datetime import datetime

connectConfig = ('127.0.0.1', 5050)

def send_file(client: socket, data):

    user = data['username']
    filename = data['filename']

    try:
        with open(f'storage\{user}\{filename}', "rb") as f:
            for byte in f:
                client.send(byte)
    except Exception as e:
        print(e)
        client.send(b'Unable to locate the file')

def getAllFileDetail(path, search = None):
    if not os.path.isdir(f'storage/{path}'): return None

    dirlist = os.listdir(f'storage/{path}')

    dir = []

    
    for filename in dirlist:

        if search != None and search != filename: continue

        path_to_file = f'storage/{path}/{filename}'

        dir.append({
            "name": filename,
            "size": size(os.path.getsize(path_to_file)),
            "last_modified": datetime.fromtimestamp(os.path.getmtime(path_to_file)).ctime(),
            "type": file_map[filename.split('.')[-1]],
            "downloadpath": os.path.abspath(path_to_file)
        })
    return dir

def get_dir(client: socket, data):
    # print(data)
    dir = {
        "public": getAllFileDetail('public', data['filename'])
    }

    try:
        user = data['username']
        dir[user] = getAllFileDetail(user, data['filename'])
    except:
        pass
    
    dir = pickle.dumps(dir)
    client.send(dir)

def save_file(client: socket, data):
    # print(data)

    try:
        user = data['username']
        if user == '': user = 'public'
        filename = data['filename']
        path = f'storage/{user}'

        if not os.path.exists(path):
            os.makedirs(path)

        with open(f'{path}/{filename}', 'wb') as f:

            while True:
                filedata = client.recv(1024)
                if len(filedata) == 0: break
                f.write(filedata)
    except Exception as e:
        print(e)
        
    return

def receivePickledData(client: socket.socket) -> bytes:
        buf = b""
        while len(buf) < 4:
            buf += client.recv(4 - len(buf))
        length = struct.unpack('!I', buf)[0]
        
        data = b""
        while len(data) < length:
            data += client.recv(length - len(buf))
        return data

def handle_client(client: socket):
    data = receivePickledData(client)
    data = pickle.loads(data)
    # print(data)
    try:
        
        if not 'username' in data: raise Exception("No Username Provided form the client")
        if not 'type' in data: raise Exception("Unable to infer request type")

        if data["type"] == "download":
            send_file(client, data)
        elif data["type"] == "get_dir":
            get_dir(client, data)
        elif data["type"] == "upload":
            save_file(client, data)
    except Exception as e:
        print(e)


    client.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind(connectConfig)
    serverSocket.listen(64)

    print("Server is listening to", connectConfig)

    while True:
        conn, addr = serverSocket.accept()
        start_new_thread(handle_client, (conn,))