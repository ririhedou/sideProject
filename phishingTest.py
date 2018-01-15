#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ketian'
__version__ = '0.01a'
__email__ = 'ririhedou@gmail.com'

import requests
from bs4 import BeautifulSoup
import random
import copy
import os
import csv

TIMEOUT = 20  # we set global timeout
DATABASE_DIR = ""  # we set global output dir


import sys
reload(sys)
sys.setdefaultencoding('utf8')


class Record(object):
    def __init__(self, idx, url, date):
        self.idx = idx
        self.url = url
        self.date = date

    def get_idx(self):
        return self.idx

    def get_url(self):
        return self.url

    def get_date(self):
        return self.date

    def print_record(self):
        print ("The idx is {}, the url is {}, the date is {}".format(self.idx, self.url, self.date))


def save_page_from_beautifulsoup(soup, fname='output.html'):
    html = soup.prettify("utf-8")
    with open(fname, "wb") as file:
        file.write(html)


def find_table_elements_for_urls(soup):
    table = soup.find("table", {"class": "data"})

    three_dots = "...added on"
    add_on = "added on"
    records = list()

    for row in table.findAll('tr', recursive=False):
        tds = row.findAll("td")
        if not len(tds) == 5:
            continue
        idx = tds[0].text

        true_url = ""
        add_date = ""

        url = tds[1].text
        if three_dots in url:
            true_url = url.split(three_dots)[0]
            add_date = url.split(three_dots)[1]
        elif add_on in url:
            true_url = url.split(add_on)[0]
            add_date = url.split(add_on)[1]
        else:
            true_url = url
            add_date = ""

        add_date = add_date.strip()
        re = Record(idx, true_url, add_date)
        records.append(copy.deepcopy(re))
    return records


# we store a csv file as the database
def search_and_add_into_database(_id, records):
    database = DATABASE_DIR + str(_id) + '.csv'
    exist_indexes = list()
    if os.path.exists(database):
        with open(database, 'r') as userFile:
            userFileReader = csv.reader(userFile)
            for row in userFileReader:
                exist_indexes.append(row[0])

    writeRecords = list()
    with open(database, 'a') as newFile:
        newFileWriter = csv.writer(newFile)
        for i in records:
            if i.idx in exist_indexes:
                continue

            writeRecords.append(i)
            l = [i.idx, i.url, i.date]
            newFileWriter.writerow(list(l))

    print ("The length of records we need to write is {}".format(len(writeRecords)))
    return writeRecords



def phishing_tank_scanning(_id):
    """
    :param _id: the index of phishing Tank
    :return:
    #url format in PhishingTank: https://www.phishtank.com/target_search.php?target_id=209&valid=All&active=y&Search=Search
    """
    general_header_1 = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                                     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    general_header_2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

    general_header_3 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:27.3) Gecko/20130101 Firefox/27.3'}

    mobile_header_1 = {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) '
                                     'AppleWebkit/534.30 '
                                     '(KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'}

    mobile_header_2 ={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) '
                                    'AppleWebKit/536.26 (KHTML, like Gecko)'
                                    ' Version/6.0 Mobile/10B350 Safari/8536.25'}

    headers = [general_header_1, general_header_2, general_header_3, mobile_header_1, mobile_header_2]

    r = random.randint(0, 4)
    random_header = headers[r]

    url = "https://www.phishtank.com/target_search.php?target_id={0}&valid=All&active=y&Search=Search".format(str(_id))

    print ("We use Random UA")
    r2 = requests.get(url, headers=random_header, allow_redirects=True, timeout=TIMEOUT)

    soup = BeautifulSoup(r2.text, "html.parser")
    soup.prettify()
    records = find_table_elements_for_urls(soup)
    left_records = search_and_add_into_database(_id, records)


if __name__ == "__main__":
    _id = 183
    phishing_tank_scanning(_id)