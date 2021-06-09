from PIL import Image, ImageFont, ImageDraw

"""This just simplifies us having to make images really :p
I could include this all in main.py but who doesn't like simplified stuff"""

font_dict = { # just a small dict so we can add fonts quickly without much fuss :p
    "bold": "fonts/bold.otf",
    "medium": "fonts/medium.otf"
}

def get_font(type, size=25):
    """We have many fonts available too us, so to simplify things we got a nice simple get function to retrieve fonts for us
    Though currently we only use 2 of them :p"""
    if type not in font_dict:
        return None
    font = ImageFont.truetype(font_dict[type], size)
    return font

def clear_background():
    """Clear the background or make a new canvas, call it what you want
    does the same thing, just if I accidently overwrite existing canvas"""
    blank = Image.new(mode="RGB", size=(400, 300), color=(48,52,52)) # going to try making the background transperent
    blank.save("images/blank_canvas.png")

def create_basic(filepath, thumbnail, title, *description):
    """Here we create a basic "embed" as you might call it...
    This will be a basic template that we can use"""
    canvas = Image.open("images/blank_canvas.png")

    bold = get_font("bold")
    medium = get_font("medium")
    
    canvas_write = ImageDraw.Draw(canvas)
    canvas_write.text((10, 5), title, font=bold)
    line_distance = 30
    for line in description:
        line_distance += 25
        canvas_write.text((10, line_distance), line, font=medium)

    if thumbnail is not None:
        pass # we have to add this later :p

    canvas.save(filepath)


def create_beg(_id_):
    """Stuff"""
    image = Image.open("images/create_beg.png")
    
    medium = get_font("medium")
    bold = get_font("bold")
    
    image_text = ImageDraw.Draw(image)

    image_text.text((10, 5), "Pls Beg", font=bold)
    image_text.text((10, 30), "This is a test", font=medium)

    image.save('finished/beg_image.png')

clear_background()