import os
from flask import Flask, send_file
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from threading import Thread
import urllib
import asyncio


import image_gen as ig
import replies 
import cache

def cooldown_check(_id_, type):
    """Basic cooldown checker, checks a cooldown against a given user + type will update data accordingly if needed
    Types are for every endpoint, if the type is daily or hourly we do a special func with it"""

    if type == "daily":
        return None
    elif type == "hourly":
        return None

# Flask App Instance, I think thats what you call it 
app = Flask(__name__)

# The Rate limiter
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

@app.route('/beg/<int:id>/<int:unix>', methods=['GET'])
def beg(id, unix):
    if cache.check_ban(id):
        return send_file("errors/banned.png")
    elif cache.basic_check(id, unix):
        return send_file("errors/tag_altered.png")
    elif cache.check_user(id):
        return send_file("finished/new_user.png")
    else:
        reply = replies.get_reply("beg")
        ig.create_image("finished/beg_image.png", None, reply["output"]["person_place"], reply["output"]["description"])
        return send_file("finished/beg_image.png")

@app.route('/search/<int:id>/<int:unix>', methods=['GET'])
def search(id, unix):
    if cache.check_ban(id):
        return send_file("errors/banned.png")
    elif cache.basic_check(id, unix):
        return send_file("errors/tag_altered.png")
    elif cache.check_user(id):
        return send_file("finished/new_user.png")
    else:
        return "Approved, do stuff"

@app.route('/shop/<int:unix>/<int:page_number>', methods=['GET'])
def shop(unix, page_number):
    if cache.check_ban(id):
        return send_file("errors/banned.png")
    elif cache.basic_check(id, unix):
        return send_file("errors/tag_altered.png")
    elif cache.check_user(id):
        return send_file("finished/new_user.png")
    else:
        return "Approved, do stuff"

@app.route('/buy/<int:id>/<int:unix>/<string:item>/<int:amount>', methods=['GET'])
def buy(id, unix, item, amount):
    if cache.check_ban(id):
        return send_file("errors/banned.png")
    elif cache.basic_check(id, unix):
        return send_file("errors/tag_altered.png")
    elif cache.check_user(id):
        return send_file("finished/new_user.png")
    else:
        return "Approved, do stuff"

@app.route('/sell/<int:id>/<int:unix>/<string:item>/<int:amount>', methods=['GET'])
def sell(id, unix, item, amount):
    if cache.check_ban(id):
        return send_file("errors/banned.png")
    elif cache.basic_check(id, unix):
        return send_file("errors/tag_altered.png")
    elif cache.check_user(id):
        return send_file("finished/new_user.png")
    else:
        return "Approved, do stuff"

@app.route('/use/<int:id>/<int:unix>/<string:item>/<int:amount>', methods=['GET'])
def sell(id, unix, item, amount):
    if cache.check_ban(id):
        return send_file("errors/banned.png")
    elif cache.basic_check(id, unix):
        return send_file("errors/tag_altered.png")
    elif cache.check_user(id):
        return send_file("finished/new_user.png")
    else:
        return "Approved, do stuff"



def run():
    """The run function that runs the app"""
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