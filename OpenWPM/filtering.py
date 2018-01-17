# used for data processing
# -*- coding: utf-8 -*-
# this is python 2.7

__author__ = "ketian"
__time__ = "Jan2018"

import requests
import time
import tldextract

from multiprocessing import Pool
import multiprocessing
from ast import literal_eval as make_tuple
import os
import sys

#global variables
TIMEOUT = 5

print ("Current request version is: {}".format(requests.__version__))

class Record(object):
    def __init__(self, idx, _type, base, url):
        self.idx = idx
        self.base = base
        self.url = url
        self._type = _type
        self.final_url = ''

    def set_final_url(self, s):
        self.final_url = s

    def set_idx(self, idx):
        self.idx = idx

    def get_type(self):
        return self._type
    
    def get_idx(self):
        return self.idx

    def get_url(self):
        return self.url

    def print_record(self):
        print ("[STAT]The idx is {}, the base is {}, , the type is {}".
               format(self.idx, self.base, self._type))

    def print_url_chain(self):
        print ("original {} -> request {} -> openWPM {}".format(self.base.encode('utf-8'), self.url.encode('utf-8'), self.final_url.encode('utf-8')))

FILTER = [u'amazonaws.com', u'aliyun.com', u'dummyns.com', u'markmonitor.com', u'ovh.net', u'google.com', u'ewebdevelopment.com', u'aliyun-cdn.com', u'deleted-domain.eu', u'com.com', u'netflix.com', u'miracle-ear.com', u'pagesjaunes.fr', u'wix.com', u'wordpress.com', u'amazon.com', u'lwspanel.com', u'facebook.com', u'world4you.com', u'spb.ru', u'booking.com', u'serving-sys.com', u'microxml.net', u'zunmi.cn', u'goserver.host', u'webgo24.de', u'bitly.com', u'top-domains.ch', u'yolasite.com', u'moniker.com', u'jimdo.com', u'hoststar.ch', u'findingresult.com', u'com.de', u'warnerbros.com', u'domainhub.com', u'afternic.com', u'google-cdn.org', u'yahoo.com', u'sedo.com', u'com.ru', u'herokuapp.com', u'namebay.com', u'apple.com', u'wixsite.com', u'porkbun.com', u'easily.co.uk', u'advexplore.com', u'googleapis.com', u'sedoparking.com']
FILTER_brand = [u'amazon.com', u'paypal.com', u'ebay.com']
FILTER = FILTER + FILTER_brand


def basic_request_function(tp):
    general_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    squat_type, url = tp[3], tp[1]
    url = 'http://'+url
    try:
        r1 = requests.get(url, headers=general_headers, allow_redirects=True, timeout=TIMEOUT)
        if r1.status_code > 400:
            fail_tp = tp + tuple([u'failed'])
            return fail_tp
        t1 = r1.url
        tmp1 = (u'General', t1)
        ttp = tp + tmp1
        return ttp

    except:
        # print("Connection refused by the server..Let me sleep for 5 seconds,ZZzzzz...")
        time.sleep(5)
        fail_tp = tp + tuple([u'failed'])
        return fail_tp


def analysis_redirection_for_final_url(HttpDomainListTuple):
    assert isinstance(HttpDomainListTuple, list)
    # A tuple sample tp =(0,1,2,3,4,5)
    # ('amazon-optimizing.com.', 'amazon-optimizing.com',
    # 'combo', '208.73.210.217', u'LIVE', u'http://amazon-optimizing.com.'
    print ("[REDIRECT]we beign to analyze redirected URLs")
    start = time.time()

    n_core = multiprocessing.cpu_count()
    n_core = 100

    print ("[REDIRECT]The cores we use is {}".format(n_core))

    pool = Pool(n_core)
    res = pool.map(basic_request_function, HttpDomainListTuple)

    redirected_url_tuples = list()
    for i in res:
        redirected_url_tuples.append(i)

    end = time.time()

    print ("[REDIRECTION]redirection took {} seconds to successfully resolve "
           "{} redirected hosts.".format(end - start, len(redirected_url_tuples)))

    return redirected_url_tuples


def filtering_redirect_url_tuples(redirect_tps):
    if len(redirect_tps) == 0:
        return None

    original_full_domain = redirect_tps[0][0]
    ex = tldextract.extract(original_full_domain)
    original_domain_tld = ex.domain + '.' + ex.suffix

    filter_failed_connect = 0
    filter_same_origin = 0
    filter_in_sale = 0

    survive_records = list()
    idx = 0
    for tp in redirect_tps:
        if tp[5] == 'failed':
            filter_failed_connect += 1
        else:
            mobile_url = tp[6]
            ex = tldextract.extract(mobile_url)
            domain_tld = ex.domain + '.' + ex.suffix
            if domain_tld == original_domain_tld:
                filter_same_origin += 1
            elif domain_tld in FILTER:
                filter_in_sale += 1
            else:
                base = tp[1]
                _type = tp[3]
                record = Record(str(idx), _type, base, mobile_url)
                survive_records.append(record)
        idx += 1

    print ("total leng", len(redirect_tps))
    print ("filter connect failed", filter_failed_connect)
    print ("filter same origin", filter_same_origin)
    print ("filter in sale list", filter_in_sale)
    print ("survive tuples", len(survive_records))
    return survive_records


def get_redirect_all_from_file_id(path, _id):
    files = os.listdir(path)
    files.sort()
    f = path + files[int(_id)]
    print ("analyze" + f)

    f_open = open(f, 'r')
    tps = list()
    for line in f_open.readlines():
        line = line.strip()
        tp = make_tuple(line)
        tps.append(tp)

    redirect = analysis_redirection_for_final_url(tps)
    survive_tps = filtering_redirect_url_tuples(redirect)

    for i in survive_tps:
        cur_idx = str(_id) + '_' + i.get_idx()
        i.set_idx(cur_idx)

    return survive_tps


if __name__ == "__main__":
    path = './domain_collect/'
    _id = sys.argv[1]
    get_redirect_all_from_file_id(path, _id)