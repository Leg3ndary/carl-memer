"""License not released."""

import os
from flask import Flask, send_file
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import urllib
import asyncio

import image_gen as ig
import replies 
from data import *

"""
Imports because I keep forgetting them
pip install pymongo[srv]

Notes:
Removed all checks for now because I can't be arsed to get them to be perfect rn
"""

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
def home():
	return {"status": "Alive"}

@app.route('/beg/<int:id>/<int:unix>')
def beg(id, unix):
    """The beg command"""
    reply = replies.get_reply("beg")
    ig.create_image("finished/beg_image.png", None, reply["output"]["person_place"], reply["output"]["description"])
    return send_file("finished/beg_image.png")

@app.route('/search/<int:id>/<int:unix>')
def search(id, unix):
    """The search command"""
    return "Approved, do stuff"

@app.route('/shop/<int:unix>/<int:page_number>')
def shop(unix, page_number):
    """Shop command for viewing items"""
    return "Approved, do stuff"

@app.route('/buy/<int:id>/<int:unix>/<string:item>/<int:amount>')
def buy(id, unix, item, amount):
    """Buy items from the shop"""
    return "Approved, do stuff"

@app.route('/sell/<int:id>/<int:unix>/<string:item>/<int:amount>')
def sell(id, unix, item, amount):
    """Sell an item"""
    return "Approved, do stuff"

@app.route('/use/<int:id>/<int:unix>/<string:item>/<int:amount>')
def use(id, unix, item, amount):
    """Use an item if it has a use."""
    return "Approved, do stuff"

@app.route("/info/<int:id>/<int:unix>/<string:item>")
def info(id, unix, item):
    """Get info on a given item"""
    item_info = loop.run_until_complete(data_inter.get_item(id, item))

    if item_info:
        ig.create_image("finished/info_command", None, item.title()+" Item Info", f"You have {item_info} left.")
        return send_file("finished/info_command")
    else:
        # item not found
        pass

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

app.run(host="0.0.0.0", port=8080)