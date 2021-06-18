from PIL import Image, ImageFont, ImageDraw

"""This just simplifies us having to make images really :p
I could include this all in main.py but who doesn't like simplified stuff"""

font_dict = { # just a small dict so we can add fonts quickly without much fuss :p
    "bold": "fonts/bold.otf",
    "medium": "fonts/medium.otf",
    "semibold": "fonts/semibold.otf",
    "light": "fonts/light.otf"
}

def get_font(type, size=18):
    """We have many fonts available too us, so to simplify things we got a nice simple get function to retrieve fonts for us
    Though currently we only use 2 of them :p"""
    if type not in font_dict:
        return None
    font = ImageFont.truetype(font_dict[type], size)
    return font

def create_canvas(size=(400, 300)):
    """Clear the background or make a new canvas, call it what you want
    does the same thing, used to generate new size canvases for better image creation"""
    blank = Image.new(mode="RGBA", size=size, color=(48, 52, 52, 0))
    blank.save("images/blank_canvas.png")

def thumbnail_magic(thumbnail):
    """Resizing thumbnail if the requested image isn't already the right shape"""
    canvas = Image.open(thumbnail)

    if canvas.size == (50, 50):
        return

    canvas_resize = canvas.resize((50,50))

    canvas_resize.save(thumbnail) # voila done

def create_image(filepath, thumbnail, title, description):
    """Creating an image to use, autoresizes to the size we need..."""

    y_canvas = 24 + (len(description) * 18)

    if thumbnail is not None and y_canvas < 51:
        y_canvas = 50

    create_canvas(size=(400, y_canvas))

    canvas = Image.open("images/blank_canvas.png")

    semibold = get_font("semibold")
    light = get_font("light")
    
    canvas_write = ImageDraw.Draw(canvas)
    canvas_write.text((0, -5), title, font=semibold)
    line_distance = 20
    for line in description:
        canvas_write.text((0, line_distance), line, font=light)
        line_distance += 18

    if thumbnail is not None:
        thumbnail_magic(thumbnail)
        t_image = Image.open(thumbnail)

        canvas.paste(t_image, (50,0))

    canvas.save(filepath)

def create_gif(filepath, thumbnail, ):
    pass