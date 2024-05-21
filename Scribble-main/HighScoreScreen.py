from tkinter import *
# from PIL import Image, ImageDraw
from tkinter.colorchooser import askcolor
import socket
import threading
import resources
from Game import Game
from drawing import *
import time

def screen(root):
    username = resources.username
    userscore = str(resources.userscore)

    frame = Frame(root)
    frame.pack(padx=200, pady=200)
    # root.geometry("400x400")

    label1 = Label(frame, text=username)
    label2 = Label(frame, text="Score " + userscore)

    label1.grid(row=2, column=2)
    label2.grid(row=4, column=2)