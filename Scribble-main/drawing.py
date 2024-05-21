from tkinter import *
from PIL import Image, ImageDraw
from tkinter.colorchooser import askcolor
import socket
import threading
import resources
import time
from HighScoreScreen import screen

WIDTH,  HEIGHT = 500, 500
CENTER = WIDTH // 2
WHITE = (255,255,255)
host = '127.0.0.1'


skt = [None] * 10
server_thread = [None] * 10
client_thread = [None] * 10
skt_index = 0
resources.is_artist = False
count = 0
def init(root):
    round_setup()

    resources.brush_width = 12
    resources.current_color = "#000000"

    resources.cnv = Canvas(root, width=WIDTH-10, height= HEIGHT-10,bg="white")

    resources.cnv.pack()
    resources.cnv.bind("<B1-Motion>", paint)

    #skipped image and draw

    resources.btn_frame = Frame(root)
    resources.btn_frame.pack(fill=X)

    resources.btn_frame.columnconfigure(0, weight=1)
    resources.btn_frame.columnconfigure(1, weight=1)
    resources.btn_frame.columnconfigure(2, weight=1)

    clear_btn = Button(resources.btn_frame, text="Clear", command=clear)
    clear_btn.grid(row=1, column=1, sticky=W+E)

    bplus_btn = Button(resources.btn_frame, text="B+", command=brush_plus)
    bplus_btn.grid(row=0, column=0, sticky=W+E)

    bminus_btn = Button(resources.btn_frame, text="B-", command=brush_minus)
    bminus_btn.grid(row=1, column=0, sticky=W+E)

    color_btn = Button(resources.btn_frame, text="Change Color", command=change_color)
    color_btn.grid(row=0, column=1, sticky=W+E)
    
    server_btn = Button(resources.btn_frame, text="Send", command=send_to_server)
    server_btn.grid(row=0, column=2, sticky=W+E)
    
    client_btn = Button(resources.btn_frame, text="Receive", command=handle_thread)
    client_btn.grid(row=1, column=2, sticky=W+E)

    global answer
    answer = StringVar()
    answer_entry = Entry(resources.btn_frame, textvariable=answer)
    answer_entry.grid(row=2, column=0)
    submit_button = Button(resources.btn_frame, text="Submit", command=handle_answer)
    submit_button.grid(row=2, column=2)

    #on close not handled

    root.mainloop()

def init2(root):
    while True:
         ret=round_setup()
         if ret: break

    resources.brush_width = 12
    resources.current_color = "#000000"

    resources.cnv = Canvas(root, width=WIDTH-10, height= HEIGHT-10,bg="white")

    resources.cnv.pack()
    resources.cnv.bind("<B1-Motion>", paint)

    #skipped image and draw

    resources.btn_frame = Frame(root)
    resources.btn_frame.pack(fill=X)

    resources.btn_frame.columnconfigure(0, weight=1)
    resources.btn_frame.columnconfigure(1, weight=1)
    resources.btn_frame.columnconfigure(2, weight=1)

    clear_btn = Button(resources.btn_frame, text="Clear", command=clear)
    clear_btn.grid(row=1, column=1, sticky=W+E)

    bplus_btn = Button(resources.btn_frame, text="B+", command=brush_plus)
    bplus_btn.grid(row=0, column=0, sticky=W+E)

    bminus_btn = Button(resources.btn_frame, text="B-", command=brush_minus)
    bminus_btn.grid(row=1, column=0, sticky=W+E)

    color_btn = Button(resources.btn_frame, text="Change Color", command=change_color)
    color_btn.grid(row=0, column=1, sticky=W+E)
    
    server_btn = Button(resources.btn_frame, text="Send", command=send_to_server)
    server_btn.grid(row=0, column=2, sticky=W+E)
    
    client_btn = Button(resources.btn_frame, text="Receive", command=handle_thread)
    client_btn.grid(row=1, column=2, sticky=W+E)

    global answer
    answer = StringVar()
    answer_entry = Entry(resources.btn_frame, textvariable=answer)
    answer_entry.grid(row=2, column=0)
    submit_button = Button(resources.btn_frame, text="Submit", command=handle_answer)
    submit_button.grid(row=2, column=2)

def re_init(root, message):
    re_round_setup(message)

    resources.brush_width = 12
    resources.current_color = "#000000"

    resources.cnv = Canvas(root, width=WIDTH-10, height= HEIGHT-10,bg="white")

    resources.cnv.pack()
    resources.cnv.bind("<B1-Motion>", paint)

    #skipped image and draw

    resources.btn_frame = Frame(root)
    resources.btn_frame.pack(fill=X)

    resources.btn_frame.columnconfigure(0, weight=1)
    resources.btn_frame.columnconfigure(1, weight=1)
    resources.btn_frame.columnconfigure(2, weight=1)

    clear_btn = Button(resources.btn_frame, text="Clear", command=clear)
    clear_btn.grid(row=1, column=1, sticky=W+E)

    bplus_btn = Button(resources.btn_frame, text="B+", command=brush_plus)
    bplus_btn.grid(row=0, column=0, sticky=W+E)

    bminus_btn = Button(resources.btn_frame, text="B-", command=brush_minus)
    bminus_btn.grid(row=1, column=0, sticky=W+E)

    color_btn = Button(resources.btn_frame, text="Change Color", command=change_color)
    color_btn.grid(row=0, column=1, sticky=W+E)
    
    server_btn = Button(resources.btn_frame, text="Send", command=send_to_server)
    server_btn.grid(row=0, column=2, sticky=W+E)
    
    client_btn = Button(resources.btn_frame, text="Receive", command=handle_thread)
    client_btn.grid(row=1, column=2, sticky=W+E)

    global answer
    answer = StringVar()
    answer_entry = Entry(resources.btn_frame, textvariable=answer)
    answer_entry.grid(row=2, column=0)
    submit_button = Button(resources.btn_frame, text="Submit", command=handle_answer)
    submit_button.grid(row=2, column=2)

def handle_answer():
    if resources.is_artist == False and resources.cur_round<=resources.ROUND_LIM:
        if(resources.answer == answer.get()):
             if resources.last_round< resources.cur_round:
                print("The answer is correct")
                resources.userscore += 10
                resources.last_round= resources.cur_round

def handle_thread():
    thread = threading.Thread(target=receive, args=())
    thread.start()


def receive():
    resources.cur_time= time.time()
    while True:
        message = resources.player_skt.recv(1024).decode()
        print(message)
        if len(message.split(" "))==3:
             resources.cur_time= time.time()
             if resources.cnv!= None: resources.cnv.destroy()
             if resources.btn_frame!= None: resources.btn_frame.destroy()
             if resources.label!= None:resources.label.destroy()
             if resources.current_player_name != None: resources.current_player_name.destroy()
             if resources.current_player_score != None: resources.current_player_score.destroy()
             resources.current_artist= (resources.current_artist+1)%resources.current_game.total_players
             re_init(resources.app_root,message)
             continue
             

        x1s, y1s, x2s, y2s, c_color = message.split(" ")

        x1 = int(x1s)
        x2 = int(x2s)
        y1 = int(y1s)
        y2 = int(y2s)


        resources.cnv.create_rectangle(x1,y1,x2,y2,outline=c_color, fill=c_color, width=resources.brush_width)

        # print((str(x1) + str(y1) + " " + str(x2) + " " + str(y2) + " " + c_color))

def send_to_server():
    resources.player_skt.send(("sent data").encode())

def paint( event):
    if resources.cur_round>resources.ROUND_LIM and time.time-resources.cur_time> resources.LIMIT+12:
          if resources.cnv!= None: resources.cnv.destroy()
          if resources.btn_frame!= None: resources.btn_frame.destroy()
          if resources.label!= None:resources.label.destroy()
          if resources.current_player_name != None: resources.current_player_name.destroy()
          if resources.current_player_score != None: resources.current_player_score.destroy()
          username = resources.username
          userscore = str(resources.userscore)
          if resources.app_root!= None:
               resources.app_root= Tk()
               screen(resources.app_root)
               return
    if resources.is_artist and resources.cur_round<= resources.ROUND_LIM:
        # if resources.cur_round> resources.ROUND_LIM:
        #      if(time.time()-resources.cur_time>2):
        #           resources.cur_time= time.time()
        #           resources.player_skt.send(("e "+resources.username+" "+resources.userscore).encode())
        #      return
        x1, y1 = (event.x-1), (event.y-1)
        x2, y2 = (event.x+1), (event.y+1)


        resources.cnv.create_rectangle(x1,y1,x2,y2,outline=resources.current_color, fill=resources.current_color, width=resources.brush_width)
        print((str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) + " " + resources.current_color))
        
        print(str(time.time())+" "+str(resources.cur_time)+" "+str(time.time()-resources.cur_time))
        
        # print(str(resources.cur_time)+(" ")+str(time.time())+" "+str(resources.current_game.current_artist))
        if time.time()-resources.cur_time>=resources.LIMIT:
            resources.cur_time= time.time()
            resources.player_skt.send(("t").encode())
            print("Switching")
            resources.cur_time= time.time()
            if resources.cnv!= None: resources.cnv.destroy()
            if resources.btn_frame!= None: resources.btn_frame.destroy()
            if resources.label!= None:resources.label.destroy()
            if resources.current_player_name != None: resources.current_player_name.destroy()
            if resources.current_player_score != None: resources.current_player_score.destroy()
            resources.current_artist= (resources.current_artist+1)%resources.current_game.total_players
            resources.userscore += 5
            init2(resources.app_root)

        elif time.time()-resources.cur_time<resources.LIMIT-2 :resources.player_skt.send((str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) + " " + resources.current_color).encode())
        
        

def clear():
    resources.cnv.delete("all")
    

def brush_plus():
    resources.brush_width += 1

def brush_minus():
    if resources.brush_width > 1:
        resources.brush_width -= 1

def change_color():
    _, resources.current_color = askcolor(title="Choose a color")

def round_setup():
    if resources.cur_round>resources.ROUND_LIM and time.time-resources.cur_time> resources.LIMIT+12:
          if resources.cnv!= None: resources.cnv.destroy()
          if resources.btn_frame!= None: resources.btn_frame.destroy()
          if resources.label!= None:resources.label.destroy()
          if resources.current_player_name != None: resources.current_player_name.destroy()
          if resources.current_player_score != None: resources.current_player_score.destroy()
          username = resources.username
          userscore = str(resources.userscore)
          if resources.app_root!= None:
               resources.app_root= Tk()
               screen(resources.app_root)
               return
    message = resources.player_skt.recv(1024).decode()
    print(message)
    if len(message.split(" "))!=3:
         return False

    code, omessage, c_round = message.split(" ")

    resources.cur_round = int(c_round)
    resources.answer = omessage

    print(message)

    if resources.cur_round > resources.ROUND_LIM:
            if resources.cnv!= None: resources.cnv.destroy()
            if resources.btn_frame!= None: resources.btn_frame.destroy()
            if resources.label!= None:resources.label.destroy()
            if resources.current_player_name != None: resources.current_player_name.destroy()
            if resources.current_player_score != None: resources.current_player_score.destroy()
            username = resources.username
            userscore = str(resources.userscore)

            frame = Frame(resources.app_root)
            frame.pack(padx=200, pady=200)
            # root.geometry("400x400")

            label1 = Label(frame, text=username)
            label2 = Label(frame, text="Score " + userscore)

            label1.grid(row=2, column=2)
            label2.grid(row=4, column=2)
            # screen(resources.app_root) 
            return

    if(code == '11'):
            resources.is_artist = True
            print("This is the artist")

    elif code == '12':
            resources.is_artist = False
            print("This is an observer")


    resources.current_player_name = Label(text= resources.username)
    resources.current_player_score = Label(text= str(resources.userscore))

    resources.current_player_name.pack()

    if(resources.is_artist == True):
        resources.label = Label(text=("Current word is : " + omessage))
        resources.label.pack()


    else:
        llabel = ""
        for i in range(0, len(omessage)-1):
            llabel += " _ "
        llabel = omessage[0] + llabel[1:]  # Update the first character of llabel
        resources.label = Label(text=("Hint: " + llabel))
        resources.label.pack()
    
    resources.current_player_score.pack()

    return True

def re_round_setup(message):
    code, omessage, c_round = message.split(" ")
    resources.cur_round= int(c_round)
    print(message)

    if resources.cur_round > resources.ROUND_LIM:
            if resources.cnv!= None: resources.cnv.destroy()
            if resources.btn_frame!= None: resources.btn_frame.destroy()
            if resources.label!= None:resources.label.destroy()
            if resources.current_player_name != None: resources.current_player_name.destroy()
            if resources.current_player_score != None: resources.current_player_score.destroy()
            frame = Frame(resources.app_root)
            frame.pack(padx=200, pady=200)
            # root.geometry("400x400")

            label1 = Label(frame, text=resources.username)
            label2 = Label(frame, text="Score " + str(resources.userscore))

            label1.grid(row=2, column=2)
            label2.grid(row=4, column=2)
            return

    resources.answer = omessage

    if(code == '11'):
            resources.is_artist = True
            print("This is the artist")

    elif code == '12':
            resources.is_artist = False
            print("This is an observer")

    resources.current_player_name = Label(text= resources.username)
    resources.current_player_score = Label(text= str(resources.userscore))

    resources.current_player_name.pack()


    if(resources.is_artist == True):
        resources.label = Label(text=("Current word is : " + omessage))
        resources.label.pack()

    else:
        llabel = ""
        for i in range(0, len(omessage)-1):
            llabel += " _ "
        llabel = omessage[0] + llabel[1:]  # Update the first character of llabel
        resources.label = Label(text=("Hint: " + llabel))
        resources.label.pack()

    resources.current_player_score.pack()
