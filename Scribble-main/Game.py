from tkinter import *
from PIL import Image, ImageDraw
from tkinter.colorchooser import askcolor
import socket
import threading
from resources import *
import time


class Game:
    total_players = 0
    player_scores = [None] * 10
    skt = [None] * 10
    current_artist = 0
    total_rounds = 3

    def create_game_thread(self):
        thread = threading.Thread(target=self.handle_game_thread, args = ())
        thread.start()

    def handle_game_thread(self):
        print("Handle Game Thread")
        ssocket = socket.socket()
        ssocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ssocket.bind((host, game_port))
        ssocket.listen()
        conn, addr = ssocket.accept()
        self.skt[self.total_players] = conn
        self.total_players += 1

        self.start_game()


        #handle stuffs after connection
        # while True:
        #     print("Stuck in here")
        #     message = conn.recv(1024).decode()

    def start_game(self):
            print("Game Started")
            for player_number in range(0, self.total_players):
                if(player_number != self.current_artist):
                    self.skt[player_number].send(str(12).encode())           #you are a observer

                elif player_number == self.current_artist:
                    self.skt[player_number].send(str(11).encode())           #you are the artist

                time.sleep(10)

    def __init__(self):
        pass

    pass