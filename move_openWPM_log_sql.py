#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ketian'
__version__ = '0.01a'
__email__ = 'ririhedou@gmail.com'


import os
import shutil
from datetime import datetime


def move_log_and_sqlite():
    cur = datetime.now().strftime('%Y-%b-%d-%H')
    print ("Current time: ", cur)

    browser_data = '/media/fbeyond/APPs/Phishing/browser_data/'
    log = browser_data + 'crawl-data.sqlite'
    sql = browser_data + 'openwpm.log'

    Dist = '/media/fbeyond/APPs/Phishing/log/'

    if os.path.isfile(log):
        shutil.move(log, Dist + cur + '-openwpm.log')
    if os.path.isfile(sql):
        shutil.move(sql, Dist + cur + '-crawl-data.sqlite')
    print ("Done the move sqlite and log")


if __name__ == "__main__":
    move_log_and_sqlite()
