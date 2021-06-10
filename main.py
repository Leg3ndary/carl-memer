import os
from flask import Flask, send_file, jsonify
from threading import Thread
import time
import urllib
import asyncio
import image_gen as ig
import pymongo

# return send_file('errors/invalid_id.png')

# Because repl sucks we need to make sure packages are installed
os.system("pip install pymongo[srv]")

# Mongo DB stuff, env-ing pass and user so people can't access the db :p 
pymongo_client = pymongo.MongoClient(f"mongodb+srv://{os.environ['MongoUser']}:{os.environ['MongoPass']}@dankmemer.ntbr7.mongodb.net/database?retryWrites=true&w=majority")
database = pymongo_client["users_db"]
users = database["users"]

# User Template, can be altered
user_template = {
    "_id": "0",
    "patron": False,
    "proper": None,
    "wallet": 1000,
    "bank": 0,
    "bankmax": 5000, 
    "items": {
        "Rare Carl": 0,
        "Carl Coin": 0,
        "Carl Medal": 0,
        "Carl Trophy": 0,
        "Carl Crown": 0,
        "Subway": 5,
        "Subway Coupon": 0,
        "Normie Shell": 1,
        "God Shell": 0,
        "Carl Shell": 0,
        "Pandas Chocolate": 0,
        "Astys Baguette": 0,
        "Oriels Neko": 0,
        "LPBs Brick": 0,
        "Mooshs Moosh": 0        
    },
    "streaks": {
        "hourly": {
            "streak": None,
            "unix": 0
        },
        "daily": {
            "streak": None,
            "unix": 0
        }
    }
}

# Literally just a dict, dunno what else to say
shop = {
    "Rare Carl": 7500, # trade item
    "Carl Coin": 62500, # trade item
    "Carl Medal": 1000000, # trade item
    "Carl Trophy": 5000000, # trade item
    "Carl Crown": 25000000, # raises gambling
    "Subway": 10000, # gives u 5000-10000 bank space
    "Subway Coupon": 1000, # Trade in 5 for a Subway or sell...
    "Normie Shell": 10000, # box
    "God Shell": 100000, # box
    "Carl Shell": 1000000, # above three are boxes, what did ya expect
    "Pandas Chocolate": 1000, # collection item
    "Astys Baguette": 1000, # collection item
    "Oriels Neko": 1000, # collection item
    "LPBs Brick": 1000, # collection item
    "Mooshs Moosh": 1000 # collection item
}

# Search replies... What else 
search_replies = {
    "Docs": [
        [ # Successes if that's a word
            "You searched docs and found your answer!",
            "You read docs and understood something.",
            "You scrolled docs and avoided being social while finding your answer...",
            "You did something productive with your life",
            "You made an attempt to learn something and it worked out!"
        ],
        [ # Fails
            "You procrastinated reading and decided to yell at some mods.",
            "You got muted after being too lazy to read",
            "You refused to read because everyone is ur servant and you can't do something so hard."
        ]
    ],
    "Old Folder": [
        [ # Success
            "You found a dank meme",
            "You found an old tik tok",
            "You found a macroscript you made a while ago",
            "You found an old file"
        ],
        [ # Fail
            "You opened a troll virus that shut down your computer.",
            "You found Free_Nitro_2017_[100% LEGIT].mp4",
            "Your computer froze.",
            "Your computer crashed."
        ]
    ],
    "Carl": [
        
    ],
    "Discord": [],
    "Bank": []
}

# We need to build a cache, this helps make sure we don't get delayed on responses if we get a surge of requests
users_inv = {}
users_bal = {}
users_data = {}

# Here we have all the cooldown dictionaries...
command_cooldowns = {}
streak_cooldowns = {}

for user in users.find():
    users_inv.update({
        user["_id"]: {
            "Rare Carl": user["items"]["Rare Carl"], 
            "Carl Coin": user["items"]["Carl Coin"],
            "Carl Medal": user["items"]["Carl Medal"],
            "Carl Trophy": user["items"]["Carl Trophy"],
            "Carl Crown": user["items"]["Carl Crown"],
            "Subway": user["items"]["Subway"],
            "Subway Coupon": user["items"]["Subway Coupon"],
            "Normie triehipp": user["items"]["Normie triehifp"],
            "God triehiup": user["items"]["God triehpfp"],
            "carltriehpup": user["items"]["carltriehfup"],
            "Pandas Chocolate": user["items"]["Pandas Chocolate"],
            "Astys Baguette": user["items"]["Astys Baguette"],
            "Oriels Neko": user["items"]["Oriels Neko"],
            "LPBs Brick": user["items"]["LPBs Brick"],
            "Mooshs Moosh": user["items"]["LPBs Brick"]
        }
    })
    users_bal.update({
        user["_id"]: {
            "wallet": user["wallet"],
            "bank": user["bank"],
            "bankmax": user["bankmax"]
        }
    })
    users_data.update({
        user["_id"]: {
            "patron": user["patron"],
            "proper": user["proper"],
            "streaks": {
                "hourly": {
                    "streak": None,
                    "unix": 0
                },
                "daily": {
                    "streak": None,
                    "unix": 0
                }
            }
        }
    })

font_dict = {
    "bold": "fonts/bold.otf",
    "medium": "fonts/medium.otf"
}

# Functions
def uib_check(_id_, utime): # Unix Id Ban Check :P UIB
    """Comparing the current unix to the time given, helps deter people who aren't using everything properly
    Rounds unix and checks if its off by 4 or negative, if it doesn't match returns false, else returns true
    We also check the id, all valid discord user snowflakes are 17 or 18 digits.
    
    Finally we also have to check if the user's been banned for being a bad boy >:L"""
    time_diff = round(time.time())-utime
    if time_diff > 4 or time_diff < 0:
        # Time difference was too short
        return False

    elif len(str(_id_)) not in [17, 18]:
        # Length of id was too short
        return False

    elif str(_id_) not in dict:
        # Id wasn't found in dict just make sure we add it and display a welcome message
        return False

    elif users_data.get("banned"):
        # user was banned for being stupid
        return False

    return True

def cooldown_check(_id_, type):
    """Basic cooldown checker, checks a cooldown against a given user + type will update data accordingly if needed
    Types are for every endpoint, if the type is daily or hourly we do a special func with it"""

    if type == "daily":
        pass
    elif type == "hourly":
        pass

app = Flask('')

@app.route('/')	
def home():
	return {
        "status": "API Alive"
        }

# Basic Beg Command, we request the id and the users proper without the # finally we take the unix to try and defer bots
@app.route('/beg/<int:id>/<int:unix>', methods=['GET']) # Technically we don't need to use a list for this but it looks cool so :p
def beg(id, unix):
    if uib_check(id, unix) is False: # Yes I know I can use not
        return "Tag has been altered. Will not work"
    else:
        return send_file("finished/beg_image")

@app.route('/search/<int:id>/<int:unix>', methods=['GET'])
def search(id, unix):
    if uib_check(id, unix) is False:
        return "Tag has been altered. Will not work"
    else:
        return "Approved, do stuff"

@app.route('/bet/<int:id>/<int:unix>/<string:code>/<int:amount>', methods=['GET'])
def bet(id, unix, code, amount):
    if uib_check(id, unix) is False:
        return "Tag has been altered. Will not work"
    else:
        return "Approved, do stuff"

@app.route('/shop/<int:unix>/<int:page_number>', methods=['GET'])
def shop(unix, page_number):
    if uib_check(id, unix) is False:
        return "Tag has been altered. Will not work"
    else:
        return "Approved, do stuff"

@app.route('/buy/<int:id>/<int:unix>/<string:item>/<int:amount>', methods=['GET'])
def buy(id, unix, item, amount):
    if uib_check(id, unix) is False:
        return "Tag has been altered. Will not work"
    else:
        return "Approved, do stuff"

@app.route('/sell/<int:id>/<int:unix>/<string:item>/<int:amount>', methods=['GET'])
def sell(id, unix, item, amount):
    if uib_check(id, unix) is False:
        return "Tag has been altered. Will not work"
    else:
        return "Approved, do stuff"

def run():
    app.run(host="0.0.0.0", port=8080)

server = Thread(target=run)
server.start()

async def keep_alive():
    """A coroutine to keep the api alive, hopefully...
    Doesn't always work, not even sure if this is correct syntax but it works :p"""
    while 1:
        urllib.request.urlopen("https://carlmemer.tagscript1.repl.co")
        await asyncio.sleep(150) # 150 Seconds or 2:30 min, sec

keep_alive()