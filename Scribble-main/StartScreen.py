from tkinter import *
from PIL import Image, ImageDraw
from tkinter.colorchooser import askcolor
from CreateGameScreen import create_game_screen
from JoinGameScreen import join_game_screen
import resources
import Game

def go_to_create_game_screen(start_screen_frame,root):
    start_screen_frame.destroy()   
    create_game_screen(root)

def go_to_join_game_screen(start_screen_frame,root):
    start_screen_frame.destroy()
    join_game_screen(root)

def exit_game(root):
    root.destroy()

def start_screen(root):
    start_screen_frame = Frame(root)
    start_screen_frame.pack(padx=200, pady= 200)
    
    create_game_button = Button(start_screen_frame, text="Create a game", command=lambda: go_to_create_game_screen(start_screen_frame, root))
    join_game_button = Button(start_screen_frame, text="Join a game", command=lambda: go_to_join_game_screen(start_screen_frame, root))
    exit_game_button = Button(start_screen_frame, text="Exit game", command=lambda: exit_game(root))

    create_game_button.grid(row=2, column=2)
    join_game_button.grid(row=6, column=2)
    exit_game_button.grid(row=10, column=2)
    
    root.mainloop()