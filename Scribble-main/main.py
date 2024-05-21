from tkinter import *
import resources
from StartScreen import start_screen
from Game import Game


resources.app_root.geometry("600x720")
resources.app_root.title("Scribble")
resources.current_game = Game()
start_screen(resources.app_root)


