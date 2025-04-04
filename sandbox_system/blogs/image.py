import os
from PIL import Image
from flask import current_app

def add_image(image_data):
    image_filename = image_data.filename
    filepath = os.path.join(current_app.root_path, r'static/image', image_filename)
    image = Image.open(image_data)
    image_size = (800, 800)
    image.thumbnail(image_size)
    image.save(filepath)
    return image_filename