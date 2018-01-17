#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
scan the phishing Tank for suspicious URLs
"""
__author__ = 'ketian'
__version__ = '0.01a'
__email__ = 'ririhedou@gmail.com'

import requests
from bs4 import BeautifulSoup
import random
import copy
import demo_ke

TIMEOUT = 20
Paypal_search_url = "https://www.phishtank.com/target_search.php?target_id=1&valid=All&active=All&Search=Search"
Facebook_search_ur = "https://www.phishtank.com/target_search.php?target_id=74&valid=All&active=All&Search=Search"

#url format https://www.phishtank.com/target_search.php?target_id=209&valid=All&active=y&Search=Search

def phishing_tank_scanning(url, my_dir, UA):

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

    headers = [general_header_1, general_header_2, general_header_3, mobile_header_1,mobile_header_2]

    r = random.randint(0, 4)
    random_header = headers[r]

    if UA == "Mobile":
        print ("We use Mobile UA")
        r2 = requests.get(url, headers=general_header_1, allow_redirects=True, timeout=TIMEOUT)
    elif UA == "General":
        print ("We use General UA")
        r2 = requests.get(url, headers=mobile_header_1, allow_redirects=True, timeout=TIMEOUT)
    else:
        print ("We use Random UA")
        r2 = requests.get(url, headers=random_header, allow_redirects=True, timeout=TIMEOUT)

    soup = BeautifulSoup(r2.text, "html.parser")
    soup.prettify()
    live_urls = find_table_elements_for_urls(soup)

    demo_ke.run_open_wpm(live_urls, my_dir=my_dir)

    print ("Begin to sleep")
    print ("z")
    print ("zz")
    print ("zzzz")

"""
an example here:
<table border="0" cellpadding="9" cellspacing="0" class="data" width="100%">
<td class="value" valign="center">
    http://langostacruda.com/wp-includes/loa.php
         <br/>
         <span class="small">
          added on Oct 18th 2017 5:57 PM
         </span>
</td>

[u'5287632', u'https://payment.ceteshop.com/myaccount/addedonOct18th20176:09PM', u'byPhishReporter', u'Unknown', u'ONLINE']
"""

def analyze_each_record_for_url(records):
    #each record is a list
    three_dots = '...'
    add_on = 'addedon'

    live_urls = list()
    for record in records:
        if len(record) == 5:
            status = record[4]
            if status.lower() == 'Offline'.lower():
                continue
            url = record[1]
            true_url = None
            if three_dots in url:
                true_url = url.split(three_dots)[0]
            elif add_on in url:
                true_url = url.split(add_on)[0]
            else:
                true_url = url
            live_urls.append(true_url)
    return live_urls


def save_page_from_beautifulsoup(soup, fname='output.html'):
    html = soup.prettify("utf-8")
    with open(fname, "wb") as file:
        file.write(html)


def find_table_elements_for_urls(soup):
    table = soup.find("table", {"class": "data"})

    records = []
    record = None
    for row in table.findAll('tr', recursive=False):
        record = list()
        for td in row.findAll("td"):
            if td is not None:
                try:
                    record.append(''.join(td.text.split()))
                except:
                    print ("[Warn]cannot extract text")
                    print (td)
        records.append(copy.deepcopy(record))
    live_urls = analyze_each_record_for_url(records)
    live_urls = list(set(live_urls))

    print ("The length of the live urls are {}".format(len(live_urls)))
    return live_urls


if __name__ == "__main__":

    ua_mobile = "Mobile"
    ua_general = "General"

    my_dir_mobile = "/home/fbeyond/Desktop/Paypal/mobile/"
    my_dir_general = "/home/fbeyond/Desktop/Paypal/general/"

    #phishing_tank_scanning(Paypal_search_url, my_dir_mobile, ua_mobile)
    phishing_tank_scanning(Paypal_search_url, my_dir_general, ua_general)


# hit this url to run the drupal cron process every hour of every day
# this command will run at 12:05, 1:05, etc.
# 5 * * * * /usr/bin/wget -O - -q -t 1 http://localhost/cron.php

