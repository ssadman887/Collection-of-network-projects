from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
import threading
import time
import socket
import os
import ipaddress
import struct
from tkinter import ttk


class ListFrame(ttk.Frame):
    def __init__(self, parent, text_data, item_height):
        super().__init__(master=parent)
        self.pack(expand=True, fill='both')

        # widget data
        self.text_data = text_data
        self.item_number = len(text_data)
        self.item_height = item_height
        self.list_height = self.item_number * item_height

        # canvas
        self.canvas = tk.Canvas(self, background='red', scrollregion=(
            0, 0, self.winfo_width(), self.list_height))
        self.canvas.pack(expand=True, fill='both')

        # display frame
        self.frame = ttk.Frame(self)

        for index, item in enumerate(self.text_data):
            self.create_item(index, item).pack(
                expand=True, fill='both', pady=4, padx=10)

        # scrollbar
        self.scrollbar = ttk.Scrollbar(
            self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')

        # events
        self.canvas.bind_all(
            '<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
        self.bind('<Configure>', self.update_size)

    def update_size(self, event):
        if self.list_height >= self.winfo_height():
            height = self.list_height
            self.canvas.bind_all(
                '<MouseWheel>', lambda event: self.canvas.yview_scroll(-int(event.delta / 60), "units"))
            self.scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')
        else:
            height = self.winfo_height()
            self.canvas.unbind_all('<MouseWheel>')
            self.scrollbar.place_forget()

        self.canvas.create_window(
            (0, 0),
            window=self.frame,
            anchor='nw',
            width=self.winfo_width(),
            height=height)

    def create_item(self, index, item):
        frame = ttk.Frame(self.frame)

        # grid layout
        frame.rowconfigure(0, weight=2)
        frame.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform='a')

        # widgets
        print(f'is first page on = {is_first_page_on}')
        if item[0] == 'button':
            ttk.Button(frame, text=f'{item[1]}', command=lambda: Call_Second_Page(
                item[1])).grid(row=0, column=0, columnspan=5, sticky='nsew')
        else:
            ttk.Label(frame, text=f'{item[1]}').grid(
                row=0, column=0, columnspan=5, sticky='nsew')
        return frame

    def update_list(self, text_data):
        # new code for update_list function here
        self.text_data = text_data
        self.item_number = len(text_data)
        self.list_height = self.item_number * self.item_height

        # clear existing items in the frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        # add new items to the frame
        for index, item in enumerate(self.text_data):
            self.create_item(index, item).pack(
                expand=True, fill='both', pady=4, padx=10)

        # update the scroll region and window size
        self.canvas.config(scrollregion=(
            0, 0, self.winfo_width(), self.list_height))
        self.update_size(None)


window_list = {}
online_friends = {}  # online_friends[name]  = (IP , PORT)
messagebox = {}
PORT = 8080
HOST_NAME = socket.gethostname()
IP = socket.gethostbyname(HOST_NAME)
BROADCAST_ADDR = str(ipaddress.ip_network(
    IP + "/24", strict=False).broadcast_address)
print(BROADCAST_ADDR)
ADDR = (IP, PORT)
WINDOW_SIZE = "660x660+500+200"
SIZE = 1024
FORMAT = "utf-8"
global is_first_page_on
is_first_page_on = True
SERVER_DATA_PATH = "received_files"

root = Tk()


def make_file_name(file_name):

    name, extension = file_name.split(".")

    while os.path.exists(name):
        name = f'{name}_{num}'
        num += 1
    return name + "." + extension


def Call_Second_Page(Cur_name):
    print(Cur_name)
    for widget in root.winfo_children():
        widget.destroy()

    host = socket.gethostname()
    root.title(host)
    root.geometry(WINDOW_SIZE)
    root.configure(bg="#f4fdfe")
    root.resizable(False, False)
    text_list = []
    global list_frame_secondpage
    list_frame_secondpage = ListFrame(root, text_list, 50)
    list_frame_secondpage.place(x=0, y=230)

    def Send_Msg(cur_name, msg):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect(online_friends[cur_name])
        server.send(f'msg@{msg}'.encode(FORMAT))
        server.close()
        if (cur_name not in messagebox):
            messagebox[cur_name] = []
        messagebox[cur_name].append(('label', f'You: {msg}'))
        list_frame_secondpage.update_list(messagebox[cur_name])

    def select_file(cur_name):
        # global filename
        filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                              title='Select Image File',
                                              filetype=(('file_type', '*.txt'), ('all files', '*.*')))
        filepath = filename
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect(online_friends[Cur_name])
        name_of_the_file = filename.split("/")[-1]
        server.send(f"file@{name_of_the_file}".encode(FORMAT))

        with open(filepath, "rb") as f:
            while True:
                buff_data = f.read(SIZE)
                if not buff_data:
                    break
                server.send(buff_data)
                gotmsg = server.recv(SIZE).decode(FORMAT)
                print(gotmsg)

        server.close()
        if (cur_name not in messagebox):
            messagebox[cur_name] = []
        messagebox[cur_name].append(
            ('label', f'You: {name_of_the_file} file is sent'))
        list_frame_secondpage.update_list(messagebox[cur_name])
        print("File has been sent successfully")

    # icon
    image_icon1 = PhotoImage(file="images/recieve.png")
    root.iconphoto(False, image_icon1)

    Hbackground = PhotoImage(file="images/sss.png")
    Label(root, image=Hbackground).place(x=-2, y=0)

    host = socket.gethostname()
    Label(root, text=f'ID: {Cur_name}', font='arial 14',
          bg='white', fg='black').place(x=400, y=100)

    Label(root, text="Write a message:", font=(
        'arial', 10, 'bold'), bg="#f4fdfe").place(x=400, y=300)
    incoming_file = Entry(root, width=20, fg="black",
                          border=2, bg='white', font=('arial', 15))
    incoming_file.place(x=400, y=370)

    Button(root, text="+ file", width=8, height=1, font='arial 14 bold', bg="#fff",
           fg="#581845", command=lambda: select_file(Cur_name)).place(x=530, y=440)
    Button(root, text="SEND", width=8, height=1, font='arial 14 bold', bg="#581845",
           fg="#fff", command=lambda: Send_Msg(Cur_name, incoming_file.get())).place(x=400, y=440)
    Button(root, text="Back", width=8, height=1, font='arial 14 bold',
           bg="#fff", fg="#581845", command=call_first_page).place(x=470, y=510)

    root.mainloop()


def broad_cast_your_presence():
    # Broadcast the IP address to all devices on the local network
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        msg = HOST_NAME + " " + IP + " " + str(PORT)
        s.sendto(msg.encode(), (BROADCAST_ADDR, port))
        print("Sent IP address:", msg)


def check_online():

    # check who is online
    start_timer = time.time() + 10
    while True:
        if time.time() - start_timer > 5:
            start_timer = time.time()
            broad_cast_your_presence_thread = threading.Thread(
                target=broad_cast_your_presence)
            broad_cast_your_presence_thread.start()
            # check online


def check_if_any_friend_is_still_online():
    start_time = time.time()
    while is_first_page_on:
        if time.time()-start_time > 5:
            start_time = time.time()
            tmp_problem = []
            for friend in online_friends:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    s.connect(online_friends[friend])
                    msg = "addr"+" " + HOST_NAME + " " + IP + " " + str(PORT)
                    s.send(msg.encode(FORMAT))
                    s.close()
                except:
                    s.close()
                    tmp_problem.append(friend)
            for friend in tmp_problem:
                del online_friends[friend]
            print(online_friends)

            tmp_list = []
            for name in online_friends:
                tmp_list.append(('button', name))
            list_frame.update_list(tmp_list)


def check_broadcast_messages():

    while True:
        ip_address = "0.0.0.0"  # Listen on all available network interfaces
        port = 12345

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((ip_address, port))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

            # Wait for a message and print it
            print("Waiting for message...")
            while True:
                data, addr = s.recvfrom(1024)
                message = data.decode()
                tmp_name, tmp_ip, tmp_port = message.split(" ")
                if tmp_name == HOST_NAME:
                    continue
                online_friends[tmp_name] = (tmp_ip, int(tmp_port))
                print("Received message from {}: {}".format(addr, message))


def call_first_page():

    for widget in root.winfo_children():
        widget.destroy()

    check_if_any_friend_is_still_online_thread = threading.Thread(
        target=check_if_any_friend_is_still_online)
    check_if_any_friend_is_still_online_thread.start()

    root.title("A-Share")
    root.geometry(WINDOW_SIZE)
    root.configure(bg="#f4fdfe")
    root.resizable(False, False)
    # icon
    image_icon = PhotoImage(file="images/icon.png")
    root.iconphoto(False, image_icon)
    Label(root, text="Share Your Heart", font=(
        'Acumin Variable Concept', 20, 'bold'), bg="#f4fdfe").place(x=20, y=50)

    receive_image = PhotoImage(file="images/recieve.png")
    Label(root, image=receive_image, bg="#f4fdfe").place(x=80, y=100)

    background = PhotoImage(file="images/background.png")
    Label(root, image=background).place(x=-2, y=300)
    text_list = []
    global list_frame
    list_frame = ListFrame(root, text_list, 100)
    list_frame.pack(side='right', fill='x', expand=False, anchor='nw')
    root.mainloop()


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the File Server.".encode(FORMAT))

    data = conn.recv(SIZE).decode(FORMAT)
    if len(data) == 0:
        return
    tmp_Data = data
    print(tmp_Data)
    data = data.split("@")
    tmp_Data = tmp_Data.split(" ")

    if (tmp_Data[0] == 'addr'):
        online_friends[tmp_Data[1]] = (tmp_Data[2], int(tmp_Data[3]))
        print(online_friends)

    elif (data[0] == 'msg'):
        for friend in online_friends:
            if (online_friends[friend][0] == addr[0]):
                if friend not in messagebox:
                    messagebox[friend] = []
                messagebox[friend].append(('label', f'{friend} : {data[1]}'))
                list_frame_secondpage.update_list(messagebox[friend])
                break
    else:
        filename = data[1]
        filename = make_file_name(filename)
        filepath = os.path.join(SERVER_DATA_PATH, filename)
        with open(filepath, "wb") as f:
            while True:
                got_data = conn.recv(SIZE)

                if not got_data:
                    break

                f.write(got_data)
                conn.send("Data received.".encode(FORMAT))
        for friend in online_friends:
            if online_friends[friend][0] == addr[0]:
                if friend not in messagebox:
                    messagebox[friend] = []
                messagebox[friend].append(
                    ('label', f'{friend} : {filename} is received'))
                list_frame_secondpage.update_list(messagebox[friend])
                break

    print(f"[DISCONNECTED] {addr} disconnected")

    conn.close()


def server_handler():
    print("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


def main():

    check_online_thread = threading.Thread(target=check_online)
    check_online_thread.start()

    check_broadcast_messages_thread = threading.Thread(
        target=check_broadcast_messages)
    check_broadcast_messages_thread.start()

    server_handler_thread = threading.Thread(target=server_handler)
    server_handler_thread.start()

    call_first_page()


if __name__ == "__main__":
    main()
