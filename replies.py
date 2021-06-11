import random
import textwrap

"""Just reply shit
Returns a dict with the reply and other data that we need :p"""

# Beg replies...
beg_replies = {
    "Carl-bot": {
        "success": [
            "Go buy yourself some subway",
            "Go buy Carl-bot premium and be cool"
        ],
        "fail": [
            "Boop, Beep, you are sheet",
            "I don't help peasants",
            "I don't help plastic litterers",
            "Imagine begging a bot"
        ],
    },
    "Discord Mod": {
        "success": [
            "I like you, sure"
        ],
        "fail": [
            "I hate you, loser"
        ]
    }
}

# Search replies... What else 
search_replies = {
    "Docs": {
        "success": [
            "You searched docs and found your answer!",
            "You read docs and understood something.",
            "You scrolled docs and avoided being social while finding your answer...",
            "You did something productive with your life",
            "You made an attempt to learn something and it worked out!"
        ],
        "fail": [
            "You procrastinated reading and decided to yell at some mods.",
            "You got muted after being too lazy to read",
            "You refused to read because everyone is ur servant and you can't do something so hard."
        ]
    },
    "Old Folder": {
        "success": [
            "You found a dank meme",
            "You found an old tik tok",
            "You found a macroscript you made a while ago",
            "You found an old file"
        ],
        "fail": [
            "You opened a troll virus that shut down your computer.",
            "You found Free_Nitro_2017_[100% LEGIT].mp4",
            "Your computer froze.",
            "Your computer crashed."
        ]
    },
    "Carl": {
        "success": [
            ""
        ],
        "fail": [
            ""
        ]
    },
    "Discord": {
        "success": [
            ""
        ],
        "fail": [
            ""
        ]
    },
    "Bank": {
        "success": [
            ""
        ],
        "fail": [
            ""
        ]
    }
}

# Pickup Replies
pickup_replies = {

}

def get_reply(r_type: str, wrap=290):
    """Gets a reply upon given type, also wraps text, default 290"""
    r_type = r_type.lower()
    
    if r_type in ["beg"]:
        reply_dict = beg_replies

    elif r_type in ["search"]:
        reply_dict = search_replies
    
    elif r_type in ["pickup"]:
        reply_dict = pickup_replies
    
    else:
        return None

    person_place = random.choice(list(reply_dict))
    outcome = random.choice(["success", "fail"])
    description = textwrap.wrap(random.choice(reply_dict[person_place][outcome]), wrap) # Reformatting everything so we can use it perfectly!

    final_dict = {
        "output": {
            "person_place": person_place,
            "description": description
        },
        "outcome": outcome
    }
    
    return final_dict