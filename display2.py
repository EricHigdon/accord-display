#!/usr/bin/env python
#
#  Copyright (c) 2013, 2015, Corey Goldberg
#
#  Dev: https://github.com/cgoldberg/py-slideshow
#  License: GPLv3


import argparse
import random
import os

import pyglet

base_index = 0

def slide_in(dt):
    if sprite2.x < 0:
        sprite1.x += dt * 1000
        sprite2.x += dt * 1000
    else:
        update_image()

def update_image():
    base_index += 1
    img1 = pyglet.image.load(image_paths[base_index])
    sprite1.image = img1
    sprite1.scale = get_scale(window, img1)
    sprite1.x = 0
    sprite1.y = 0
    img2 = pyglet.image.load(image_paths[base_index + 1])
    sprite2.image = img2
    sprite2.scale = get_scale(window, img2)
    sprite2.x = (0 - img2.width) * sprite2.scale
    sprite2.y = 0
    window.clear()

def get_image_paths(input_dir='.'):
    paths = []
    for root, dirs, files in os.walk(input_dir, topdown=True):
        for file in sorted(files):
            if file.endswith(('jpg', 'png', 'gif')):
                path = os.path.abspath(os.path.join(root, file))
                paths.append(path)
    return paths

def get_scale(window, image):
    if image.width > image.height:
        scale = float(window.width) / image.width
    else:
        scale = float(window.height) / image.height
    return scale

window = pyglet.window.Window(fullscreen=True)
batch = pyglet.graphics.Batch()

@window.event
def on_draw():
    batch.draw()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='directory of images',
                        nargs='?', default=os.getcwd())
    args = parser.parse_args()
    image_paths = get_image_paths(args.dir)
    img1 = pyglet.image.load(image_paths[base_index])
    sprite1 = pyglet.sprite.Sprite(img1, batch=batch)
    sprite1.scale = get_scale(window, img1)
    sprite1.x = 0
    img2 = pyglet.image.load(image_paths[base_index + 1])
    sprite2 = pyglet.sprite.Sprite(img2, batch=batch)
    sprite2.scale = get_scale(window, img2)
    sprite2.x = (0 - img2.width) * sprite2.scale

    pyglet.clock.schedule_interval(slide_in, 1/60.0)

    pyglet.app.run()
