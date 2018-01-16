#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ketian'
__version__ = '0.01a'
__email__ = 'ririhedou@gmail.com'


browser_data = '/media/fbeyond/APPs/Phishing/browser_data/'
screen = browser_data + 'screenshots/'
pages = browser_data + 'sources/'

Dist = '/media/fbeyond/APPs/Phishing/Crawl/'

import shutil
import os
import sys


def move_screen_page_with_id(_id):
    # we set the dist
    destination = Dist + str(_id) + '/'

    if not os.path.exists(destination):
        os.makedirs(destination)

    for i in os.listdir(screen):
        if i.endswith('.png'):
            shutil.move(screen + i, destination)

    for i in os.listdir(pages):
        if i.endswith('.html'):
            shutil.move(pages + i, destination)

    print ("Done the movement of {}".format(_id))


if __name__ == "__main__":
    _id = sys.argv[1]
    move_screen_page_with_id(_id)