import os
from flask import Flask, send_file
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from threading import Thread
import urllib
import asyncio

import image_gen as ig
import replies 
import data

async def cooldown_check(_id_, type):
    """Basic cooldown checker, checks a cooldown against a given user + type will update data accordingly if needed
    Types are for every endpoint, if the type is daily or hourly we do a special func with it"""

    if type == "daily":
        return None
    elif type == "hourly":
        return None

# Flask App Instance
app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["3/second"] 
)


@app.route('/')	
async def home():
	return {"status": "Alive"}

@app.route('/beg/<int:id>/<int:unix>', methods=['GET'])
async def beg(id, unix):
    """The beg command"""
    if data.check_ban(id):
        return send_file("errors/banned.png")
    elif data.basic_check(id, unix):
        return send_file("errors/tag_altered.png")
    elif data.check_user(id):
        return send_file("finished/new_user.png")
    else:
        reply = replies.get_reply("beg")
        ig.create_image("finished/beg_image.png", None, reply["output"]["person_place"], reply["output"]["description"])
        return send_file("finished/beg_image.png")

@app.route('/search/<int:id>/<int:unix>', methods=['GET'])
async def search(id, unix):
    """The search command"""
    if data.check_ban(id):
        return send_file("errors/banned.png")
    elif data.basic_check(id, unix):
        return send_file("errors/tag_altered.png")
    elif data.check_user(id):
        return send_file("finished/new_user.png")
    else:
        return "Approved, do stuff"

@app.route('/shop/<int:unix>/<int:page_number>', methods=['GET'])
async def shop(unix, page_number):
    """Shop command for viewing items"""
    if data.check_ban(id):
        return send_file("errors/banned.png")
    elif data.basic_check(id, unix):
        return send_file("errors/tag_altered.png")
    elif data.check_user(id):
        return send_file("finished/new_user.png")
    else:
        return "Approved, do stuff"

@app.route('/buy/<int:id>/<int:unix>/<string:item>/<int:amount>', methods=['GET'])
async def buy(id, unix, item, amount):
    """Buy items from the shop"""
    if data.check_ban(id):
        return send_file("errors/banned.png")
    elif data.basic_check(id, unix):
        return send_file("errors/tag_altered.png")
    elif data.check_user(id):
        return send_file("finished/new_user.png")
    else:
        return "Approved, do stuff"

@app.route('/sell/<int:id>/<int:unix>/<string:item>/<int:amount>', methods=['GET'])
async def sell(id, unix, item, amount):
    """Sell items to the shop"""
    if data.check_ban(id):
        return send_file("errors/banned.png")
    elif data.basic_check(id, unix):
        return send_file("errors/tag_altered.png")
    elif data.check_user(id):
        return send_file("finished/new_user.png")
    else:
        return "Approved, do stuff"

@app.route('/use/<int:id>/<int:unix>/<string:item>/<int:amount>', methods=['GET'])
async def use(id, unix, item, amount):
    """Use an item if it has a use."""
    if data.check_ban(id):
        return send_file("errors/banned.png")
    elif data.basic_check(id, unix):
        return send_file("errors/tag_altered.png")
    elif data.check_user(id):
        return send_file("finished/new_user.png")
    else:
        return "Approved, do stuff"

@app.route("/info/<int:id>/<int:unix>/<string:item>", methods="GET")
async def info(id, unix, item, amount):
    """Get info on a given item"""
    if data.check_ban(id):
        return send_file("errors/banned.png")
    elif data.basic_check(id, unix):
        return send_file("errors/tag_altered.png")
    elif data.check_user(id):
        return send_file("finished/new_user.png")
    else:
        item_info = await data.get_item(id, item)

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
            import motor
        except:
            os.system("pip install motor")
            import motor

        await asyncio.sleep(150) # 150 Seconds or 2:30 min, sec

keep_alive()