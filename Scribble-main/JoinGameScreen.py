from tkinter import *
# from PIL import Image, ImageDraw
from tkinter.colorchooser import askcolor
import socket
import threading
import resources
from Game import Game
from drawing import *
import time


def join_game(frame, root):
    host = ""
    host = host_value.get()
    
    if(len(host) != 0):
        resources.host = host

    name = ""
    name = name_value.get()

    resources.username = name

    print(resources.username)

    print("Join game button pressed")
    ssocket = socket.socket()
    ssocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ssocket.connect(((resources.host, 5000)))
    print("Joined Successfully")
    resources.current_game.total_players += 1
    resources.player_skt = ssocket
    frame.destroy()
    resources.cur_time= time.time()
    init(root)


def join_game_screen(root):
    join_game_frame = Frame(root)
    resources.frame = join_game_frame
    join_game_frame.pack(padx=200, pady= 200)

    host_label = Label(join_game_frame,text="Enter the game host address:")
    enter_name_label = Label(join_game_frame, text="Enter a user name")

    global host_value
    host_value = StringVar()

    global name_value
    name_value = StringVar()

    host_entry = Entry(join_game_frame, textvariable=host_value)
    name_entry = Entry(join_game_frame, textvariable=name_value)

    join_game_button = Button(join_game_frame, text="Join the game", command=lambda:join_game(join_game_frame, root))

    host_label.grid(row=2, column=2)
    host_entry.grid(row=3, column=2)
    enter_name_label.grid(row=4, column=2)
    name_entry.grid(row=5,column=2)
    join_game_button.grid(row=6, column=2)
    
    root.mainloop()