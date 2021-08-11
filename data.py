import os
import time
import image_gen as ig
from pymongo import MongoClient
import asyncio

"""
Why Not Motor?

Flask is very quirky and for some reason creates a new event loop when I want it to use the running event loop
after trying for around 2 weeks I've just given up as no solution I can come up with actually works.

Please just don't question it, loops literally work fine.
"""

loop = asyncio.new_event_loop()

user_template = {
    "_id": "0",
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
    "Carl Crown": 25000000, # trade item
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

# Here we have all the cooldown dictionaries...
# We'll be using these...
command_cooldowns = {}
streak_cooldowns = {}

class DataInteractions():
    """because python is dumb we gotta do stuff"""

    def __init__(self):
        """initialize everything"""
        self.pymongo_client = MongoClient(f"""mongodb+srv://{os.environ["MongoUser"]}:{os.environ["MongoPass"]}@dankmemer.ntbr7.mongodb.net/database?retryWrites=true&w=majority""")
        self.database = self.pymongo_client["users_db"]
        self.users = self.database["users"]
        self.banned_users = self.database["banned"]

    def get_price(self, item: str, amount: int):
        """Get the price for an item multiplied by the amount the player is buying
        it for"""
        try:
            item_price = shop[item]
            item_price *= amount
            return item_price
        except:
            return None

    def update_bal(self, _id_: str, action: str, bal_type: str, amount: int):
        """Update the bal type for given id with given amount"""
        user_data = self.users.find_one({
            "_id": _id_
        })

        if action.lower() == "add":
            amount = user_data[bal_type] + amount

        elif action.lower() == "remove":
            amount = user_data[bal_type] - amount

        self.users.update_one({"_id": _id_}, {"$set":{bal_type:amount}})

    def get_bal(self, _id_: str):
        """Returns a dictionary with all our data in it"""
        users_data = self.users.find_one({
            "_id": _id_
        })

        user_dict = {
            "wallet": users_data["wallet"],
            "bank": users_data["bank"],
            "bankmax": users_data["bankmax"]
        }
        return user_dict

    def get_item(self, _id_: str, item: str):
        """Returns data for a users items... We actually need this"""
        users_data = self.users.find_one({
            "_id": _id_
        })
        return users_data["items"].get(item)

    def buy_item(self, _id_, item, amount):
        """Buys items with an id, allows for more then one item"""
        pass

    def sell_item(self, _id_, item, amount):
        """Sells items with an id, allows for more then one item"""
        pass

    def streak_magic(self, _id_, streak_type):
        """Checks Streaks, updates it, etc"""
        pass

    def transfer_bal(self, _id_, action, amount=None):
        """Action can be deposit and withdraw, if amount is None we assume they want to with/dep max
        Just a simple cmd that makes stuff a bit faster"""
        pass

    # Creating Accounts
    def create_account(self, _id_):
        """Creating a brand new account for a new user, includes adding it to our cache"""
        # Creating another dict to alter and use...
        user_temp = user_template
        user_temp["_id"] = str(_id_)

        self.users.insert_one(user_temp)

    # Checks
    def check_time(self, unix_time):
        """Comparing the current unix to the time given, helps deter people who aren't using everything properly
        Rounds unix and checks if its off by 4 or negative, if it doesn't match returns false, else returns true"""
        time_diff = round(time.time())-unix_time
        if time_diff > 4 or time_diff < 0:
            # Time difference was too short
            return True
        return False

    def check_snowflake(self, _id_):
        """Also discord user ids are 17 or 18 digits long, if the given id isn't either tag's been altered
        We could go even deeper and use the api to see if a valid id but that would slow the API down and it might be against tos
        Idk :P"""
        if len(str(_id_)) not in [17, 18]:  
            return True
        return False

    def check_ban(self, _id_): # could convert to str but its fine :3
        """Checking if user was banned for abusing api, what a loser tbh"""
        if str(_id_) in []: # create a cursor later
            ig.create_image("errors/banned.png", None, "User Banned", f"{str(_id_)} was banned from using this tag, not appealable.")
            return True
        return False

    def basic_check(self, _id_, unix_time):
        """Combining basic tag altering checks, might help in the future ig"""
        if not self.check_time(unix_time) or not self.check_snowflake(_id_):
            ig.create_image("errors/tag_altered.png", None, "Tag Altered", "Please do not alter this tag in any shape, way or form. Reimport if you think this is a mistake")
            return True
        return False

    def check_user(self, _id_):
        """Checking the user id in our db and doing stuff if we need to"""
        if str(_id_) not in dict:
            self.create_account(_id_)
            ig.create_image("finished/new_user.png", None, "Welcome!", "Please wait a few seconds as your account's being created!")
            return True
        return False

    # Shells/Items
    """We have to add chances/functions to add items/coins to the users data
    We do that here
        "Subway": 10000, # gives u 5000-10000 bank space
        "Subway Coupon": 1000, # Trade in 5 for a Subway or sell...
        "Normie Shell": 10000, # box
        "God Shell": 100000, # box
        "Carl Shell": 1000000, # above three are boxes, what did ya expect

    usable_items = ["subway", "coupon", "normie", "god", "carl"]
    def use_item(_id_, item: str, amount):
        if item.lower() not in usable_items:
            return None
    """

data_inter = DataInteractions()