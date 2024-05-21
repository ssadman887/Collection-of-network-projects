from tkinter import *
from PIL import Image, ImageDraw
from tkinter.colorchooser import askcolor
import socket
import threading
import resources
from Game import Game
from drawing import *
import time
import random

def add_player():    
    print("Add player button pressed")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', 5000))
        s.listen(1)
        conn, addr = s.accept()
    resources.current_game.skt[resources.current_game.total_players] = conn
    resources.current_game.total_players += 1
    print("Total players now :" + " " + str(resources.current_game.total_players))  
    

    

def start_game():
    print("Start game button pressed")
    
    artist = resources.current_artist

    word = resources.dictionary[random.randint(0, 79)]
    resources.current_word=word

    for i in range(0, 5):
                    if resources.current_game.skt[i] != None and i == resources.current_artist:
                            resources.current_game.skt[i].send((str(11) + " " + word+" "+ str(resources.cur_round)).encode())
                    elif resources.current_game.skt[i] != None:
                            resources.current_game.skt[i].send((str(12) + " " + word+" "+ str(resources.cur_round)).encode())
    
    while True:
           if resources.current_game.skt[resources.current_artist]== None:
                  continue
        #    print("Current artist is " + str(resources.current_artist))
           message = resources.current_game.skt[resources.current_artist].recv(1024).decode()

        #    done=0
        #    if message[0]=='e':
        #           ig, name, tmp= message.split(" ")
        #           score= int(tmp)
        #           done += 1
        #           resources.userlist.append(name)
        #           resources.scorelist.append(score)
        #           if done>= resources.current_game.total_players:
        #                  break

                  
           if message[0]=='t':
                word = resources.dictionary[random.randint(0, 79)]
                resources.current_word= word
                resources.current_artist= (resources.current_artist+1)%resources.current_game.total_players
                resources.cur_round += 1

                time.sleep(7)

                # if resources.cur_round== resources.ROUND_LIM:
                #     for i in range(0, 5):
                #         if resources.current_game.skt[i] != None:
                #             resources.current_game.skt[i].send(("score").encode())
                    
                #     break


                for i in range(0, 5):
                    if resources.current_game.skt[i] != None and i == resources.current_artist:
                            resources.current_game.skt[i].send((str(11) + " " + word+ " "+ str(resources.cur_round)).encode())
                    elif resources.current_game.skt[i] != None:
                            resources.current_game.skt[i].send((str(12) + " " + word+ " "+ str(resources.cur_round)).encode())
                # init(resources.app_root)

                # time.sleep(2)
                for i in range(0, 5):
                    if resources.current_game.skt[i] != None and i == resources.current_artist:
                            resources.current_game.skt[i].send((str(11) + " " + word+ " "+ str(resources.cur_round)).encode())
                
                # if resources.cur_round>resources.ROUND_LIM:
                #     break
                continue


            
           for i in range(0, 10):
                        if resources.current_game.skt[i] != None and i != resources.current_artist:
                            resources.current_game.skt[i].send((message).encode())
    print(resources.userlist)
    print(resources.scorelist)       
           

def create_game_screen(root):
    create_game_frame = Frame(root)
    create_game_frame.pack(padx=200, pady=200)
    
    add_player_button = Button(create_game_frame, text="Add a player", command= add_player)
    start_game_button = Button(create_game_frame, text="Start Game", command= start_game)
    

    add_player_button.grid(row=2, column=2)
    start_game_button.grid(row=6, column=2)

    root.mainloop()
