import os
from flask import Flask, send_file, jsonify
from threading import Thread
import time
import urllib
import asyncio
from PIL import Image, ImageFont, ImageDraw
import pymongo

# return send_file('errors/invalid_id.png')

# Because repl sucks we need to make sure packages are installed
os.system("pip install pymongo[srv]")

""" Everything you need to know...
This project is not affiliated with either Dank Memer or Carl-bot neither is it supported by either, this is just for a tag and my curiosity.

API Endpoints... 
https://carlmemer.tagscript1.repl.co
The above shows wether the api endpoint is alive and working...
This is the base URL    

Actual Endpoints...
==========================
/beg/userid/unix
Beg command, classic

/search/userid/unix
Search command, sadly we cannot await options as we only really have one oppurtunity or request if you will :p

/pickup/userid/unix
Pickup command, just another way to earn money

/shop/unix/page_number
Shows shop with given page_number

/info/userid/unix/object
View an item, another player, you're profile... Up to you

/inv/userid/unix/page_number
View your inventory which also includes a page_number

/buy/userid/unix/item/amount
Buy something, simple.

/sell/userid/unix/item/amount
Sell something, extremely difficult.

/use/userid/unix/item
Use an item... What else

/hourly/userid/unix
Hourly command to get your hourly reward since I need more ways to get money

/daily/userid/unix
Daily Command to get your daily reward since we still need more ways to get money

/leaderboards/unix/type
Leaderboards for the following types, Wallet Bal, Bank Bal, Bank Space

Error/Testing Endpoints
==========================
/cnf/unix/command
Command not found, just an error image saying the command wasn't found

Read stuff under here if you want, I won't explain any of it really further"""

# Mongo DB shit, env-ing pass and user so people can't access the db :p 
pymongo_client = pymongo.MongoClient(f"mongodb+srv://{os.environ['MongoUser']}:{os.environ['MongoPass']}@dankmemer.ntbr7.mongodb.net/database?retryWrites=true&w=majority")

# assigning collections and the actual database
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
            "You found a old tik tok",
            ""
        ],
        [ # Fail
            "You opened a troll virus that shut down your computer.",
            "You found Free_Nitro_2017_[100% LEGIT].mp4",
            ""
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
            "proper": user["proper"]
        }
    })

font_dict = {
    "bold": "fonts/bold.otf",
    "medium": "fonts/medium.otf"
}

# Functions
def get_font(type, size=25):
    """We have many fonts available too us, so to simplify things we got a nice simple get function to retrieve fonts for us
    Though currently we only use 2 of them :p"""
    if type not in font_dict:
        return None
    font = ImageFont.truetype(font_dict[type], size)
    return font

def user_check(_id_):
    """Checking userid against built cache, tells us if we need to open up a new account or just keep going"""
    if str(_id_) in dict:
        return True
    # Do stuff here
    return False

def uib_check(_id_, utime):
    """Comparing the current unix to the time given, helps deter people who aren't using everything properly
    Rounds unix and checks if its off by 4 or negative, if it doesn't match returns false, else returns true
    We also check the id, all valid discord user snowflakes are 17 or 18 digits.
    
    Finally we also have to check if the user's been banned for being a bad boy >:L"""
    time_diff = round(time.time())-utime
    if time_diff > 4 or time_diff < 0 or len(str(_id_)) not in [17, 18]:
        return False

    elif users_data.get("banned"):
        """Add an image"""
        pass

    return True

def create_beg(_id_):
    """Stuff"""
    image = Image.open("images/create_beg.png")
    
    medium = get_font("medium")
    bold = get_font("bold")
    
    image_text = ImageDraw.Draw(image)

    image_text.text((10, 5), "Pls Beg", font=bold)
    image_text.text((10, 30), "This is a test", font=medium)

    image.save('finished/beg_image.png')

app = Flask('')

@app.route('/')	
def home():
	return jsonify(
        {"status": "API Alive"}
    )  

# Basic Beg Command, we request the id and the users proper without the # finally we take the unix to try and defer bots
@app.route('/beg/<int:id>/<int:unix>', methods=['GET']) # Technically we don't need to use a list for this but it looks cool so :p
def beg(id, unix):
    if uib_check(id, unix) is False: # Yes I know I can use not
        return "Tag has been altered. Will not work"
    else:
        beg_image = create_beg(id)
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
    Doesn't always work"""
    while 1:
        urllib.request.urlopen("https://carlmemer.tagscript1.repl.co")
        await asyncio.sleep(300)

keep_alive()



def hi(check_word, word):
    final_word = check_word(word)
    width_o, height_o = (498, 498)

    carls_beautiful_shell = Image.open("images/Shell_Carl.png")
    font = ImageFont.truetype('FreeSans.ttf', 100)

    keeping_shell_safe = ImageDraw.Draw(carls_beautiful_shell)

    width_n, height_n = keeping_shell_safe.textsize(final_word, font=font)
    keeping_shell_safe.text(((width_o-width_n)/2,(height_o-height_n)/2), final_word, font=font, fill=(255, 255, 255))

    carls_beautiful_shell.save("dirty_shell.png")