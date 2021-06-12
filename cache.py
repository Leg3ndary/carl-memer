import os

# Because repl sucks we need to make sure packages are installed
try:
    import pymongo
except:
    os.system("pip install pymongo[srv]")
    import pymongo

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
            "Normie triehipp": user["items"]["Normie Shell"],
            "God triehiup": user["items"]["God Shell"],
            "carltriehpup": user["items"]["Carl Shell"],
            "Pandas Chocolate": user["items"]["Pandas Chocolate"],
            "Astys Baguette": user["items"]["Astys Baguette"],
            "Oriels Neko": user["items"]["Oriels Neko"],
            "LPBs Brick": user["items"]["LPBs Brick"],
            "Mooshs Moosh": user["items"]["Mooshs Moosh"]
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
