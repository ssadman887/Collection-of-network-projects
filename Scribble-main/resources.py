from tkinter import *

game_port = 5001
player_skt = None
host = '127.0.0.1'
app_root = Tk()
frame = None
current_game = None 
current_word= None
current_artist=0
cur_time= None
player_list=[]
LIMIT=30
cnv= None
brush_width= None
current_color= None
is_artist= False
btn_frame= None
label= None
thread= None
answer = None
cur_round=1
ROUND_LIM=3
last_round= 0

username = None
userscore = 0
userlist=[]
scorelist=[]
current_player_name = None
current_player_score = None
dictionary = [
    # Social Media Apps
    'Facebook', 'Instagram', 'Twitter', 'Snapchat', 'TikTok',
    'LinkedIn', 'Pinterest', 'WhatsApp', 'YouTube', 'Reddit',
    
    # Foods
    'Pizza', 'Burger', 'Sushi', 'Pasta', 'Tacos',
    'Ice', 'Chicken', 'Steak', 'Chocolate', 'Salad',
    
    # Countries
    'United', 'China', 'Russia', 'Brazil', 'Germany',
    'France', 'Kingdom', 'India', 'Australia', 'Japan',
    
    # Animals
    'Lion', 'Tiger', 'Elephant', 'Giraffe', 'Dolphin',
    'Penguin', 'Gorilla', 'Cheetah', 'Kangaroo', 'bear',

    'Apple', 'Banana', 'Orange', 'Grapes', 'Watermelon',
    'Pineapple', 'Strawberry', 'Mango', 'Peach', 'Kiwi',
    'Carrot', 'Broccoli', 'Potato', 'Tomato', 'Cucumber',
    'Lemon', 'Avocado', 'Blueberry', 'Raspberry', 'Pear',
    'Chicken', 'Fish', 'Beef', 'Pork', 'Lamb',
    'Shrimp', 'Salmon', 'Turkey', 'Crab', 'Tuna',
    'Cabbage', 'Spinach', 'Eggplant', 'Onion', 'Garlic',
    'Cantaloupe', 'Honeydew', 'Cherry', 'Coconut', 'Plum'
]
