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
import crawl_phishing

TIMEOUT = 20  # we set global timeout
DATABASE_DIR = "/media/fbeyond/APPs/Phishing/database/"  # we set global output dir


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
    if len(left_records) > 0:
        crawl_phishing.run_open_wpm_for_records(left_records)
    else:
        print ("we did not see new records")

    print ("Done the crawler part")


BrandMap = {1: 'PayPal', 2: 'eBay', 3: 'Chase', 4: 'HSBC', 5: 'Barclays', 6: 'Bank of America / MBNA', 7: 'Wells Fargo', 8: 'Other', 9: 'LaSalle', 12: 'M &amp; I', 13: 'Wachovia', 14: 'Citizens', 15: 'Ameritrade', 16: 'Regions', 17: 'Associated Bank', 18: 'Huntington', 19: 'Charter One', 20: 'Key Bank', 21: 'Washington Mutual', 22: 'Comerica', 23: 'Peoples', 24: 'US Bank', 25: 'Westpac', 26: 'NatWest', 27: 'Bendigo', 28: 'Amarillo', 29: 'Capital One', 30: 'Compass', 31: 'Crown', 32: 'CIBC', 33: 'DBS', 34: 'National City', 35: 'Salem Five', 36: 'RBC', 37: 'Nantucket Bank', 39: 'Franklin', 40: 'Bank of KC', 41: 'FHB', 42: 'Citibank', 43: 'TD Canada Trust', 44: 'BMO', 45: 'Bank of the West', 48: 'Fifth Third Bank', 50: 'First Federal Bank of California', 51: 'Alliance Bank', 53: 'Western Union', 55: 'Sky Financial', 56: 'WalMart', 57: 'Independent Bank', 58: 'Volksbanken Raiffeisenbanken', 59: 'e-gold', 60: 'Downey Savings', 61: 'Amazon.com', 62: 'IRS', 63: 'BB&amp;T', 64: 'Poste', 65: 'Career Builder', 66: 'MBTrading', 67: 'Interactive Brokers', 68: 'Accurint', 69: 'PNC Bank', 70: 'RBS', 71: 'Nedbank', 72: 'KCFCU (Kauai Credit Union)', 73: 'Banca di Roma', 74: 'Facebook', 75: 'Salesforce', 76: 'Google', 77: 'EPPICard', 78: 'MySpace', 81: 'Habbo', 82: 'Bradesco', 84: 'Scotiabank', 85: 'Tibia', 86: 'Steam', 87: 'CUA (Credit Union Australia)', 88: 'World of Warcraft', 89: 'Orkut', 90: 'Standard Bank Ltd.', 91: 'First National Bank (South Africa)', 92: 'ABSA Bank', 93: 'South African Revenue Service', 94: 'Groupon', 95: 'LivingSocial', 96: 'BloomSpot', 97: 'HomeRun', 98: 'BuyWithMe', 99: 'Tippr', 100: 'Plum District', 101: 'Zynga', 102: 'Egg', 103: 'First Direct', 104: 'Halifax', 105: 'Cariparma Credit Agricole', 106: 'Gruppo Carige', 107: 'Cartasi', 108: 'HMRC', 109: 'Santander UK', 110: 'AOL', 111: 'Yahoo', 112: 'Live', 113: 'Craigslist', 114: 'Playdom', 115: 'Playfish', 116: 'ZML', 117: 'Skype', 118: 'American Airlines', 120: 'Caixo', 121: 'Safra National Bank of New York', 122: 'Blizzard', 123: 'ING', 124: 'Bancasa', 125: 'Banco Real', 126: 'Cahoot', 127: 'NEXON', 128: 'Rabobank', 129: 'Visa', 130: 'Mastercard', 131: 'Centurylink', 132: 'Twitter', 133: 'ANZ', 134: 'RuneScape', 135: 'Itau', 136: 'TAM Fidelidade', 137: 'Cielo', 138: 'Caixa', 139: 'ABL', 140: 'Delta', 141: 'American Greetings', 144: 'ASB', 145: 'Tagged', 146: 'Co-operative Bank', 147: 'Smile Bank', 148: 'Nationwide', 149: 'Northern Rock', 150: 'CIMB Bank', 151: 'GTBank', 152: 'Littlewoods', 153: 'Very', 154: 'Hotmail', 155: 'Vodafone', 156: 'Capitec Bank', 157: 'US Airways', 158: 'Banco De Brasil', 159: 'otoMoto', 160: 'Allegro', 161: 'Nets', 163: 'Suncorp', 164: 'NAB', 165: 'ATO', 166: 'St George Bank', 167: 'Commonwealth Bank of Australia', 168: 'Orange', 169: 'Verizon', 170: 'ArenaNet', 171: 'GuildWars2', 172: 'Swedbank', 173: 'Metro Bank', 175: 'Nordea', 176: 'PKO', 177: 'Microsoft', 178: 'Banca Intesa', 179: 'Lottomatica', 180: 'Pintrest', 181: 'TSB', 182: 'Lloyds Bank', 183: 'Apple', 184: 'American Express', 185: 'Deutsche Bank', 186: 'Discover Card', 187: 'Discover Bank', 188: 'Diners Club', 189: 'AT&amp;T', 192: 'PagSeguro', 193: 'Tesco', 194: 'Dropbox', 195: 'Permanent TSB', 196: 'Discovery', 197: 'DHL', 199: 'USAA', 200: 'Netflix', 201: 'ABN', 202: 'Intesa Sanpaolo', 203: 'Kiwibank', 204: 'LinkedIn', 205: 'NetSuite', 206: 'WhatsApp', 207: 'Adobe', 208: 'Bank Millennium', 209: 'Aetna', 210: 'Blockchain', 211: 'Alibaba.com', 212: 'BT', 213: 'Uber', 214: 'Coinbase', 215: 'LocalBitcoins.com', 216: 'Paxful', 217: 'Bitfinex', 218: 'GitHub', 219: 'Credit Karma', 220: 'UniCredit', 221: 'Rackspace', 222: 'Xapo', 223: 'MyEtherWallet', 224: 'bitFlyer', 225: 'MyMonero'}
if __name__ == "__main__":
    _id = sys.argv[1]
    print ("We analyze"),
    print ("IDX {} Brand {}".format(_id, BrandMap[int(_id)]))
    phishing_tank_scanning(_id)