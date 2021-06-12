import os
from flask import Flask, send_file, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from threading import Thread
import time
import urllib
import asyncio

import image_gen as ig
import replies 
import cache

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

    #elif users_data.get("banned"):
        # user was banned for being stupid
        #return False

    return True

def cooldown_check(_id_, type):
    """Basic cooldown checker, checks a cooldown against a given user + type will update data accordingly if needed
    Types are for every endpoint, if the type is daily or hourly we do a special func with it"""

    if type == "daily":
        pass
    elif type == "hourly":
        pass

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["4/second"]
)

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
        reply = replies.get_reply("beg")
        ig.create_image("finished/beg_image.png", None, reply["output"]["person_place"], reply["output"]["description"])
        return send_file("finished/beg_image.png")

@app.route('/search/<int:id>/<int:unix>', methods=['GET'])
def search(id, unix):
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
        try:
            import pymongo
        except:
            os.system("pip install pymongo[srv]")
            import pymongo

        await asyncio.sleep(150) # 150 Seconds or 2:30 min, sec

keep_alive()