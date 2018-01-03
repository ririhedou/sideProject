#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ketian'
__version__ = '1.04b'
__email__ = 'ririhedou@gmail.com'

import os
import gzip
from multiprocessing import Pool
import multiprocessing

def intersection_of_domains(p1, p2):
    p1_domains = recursively_analyze_gz_files_no_multipleProcess(p1)
    print ("P1 size {}".format(len(p1)))

    p2_domains = recursively_analyze_gz_files_no_multipleProcess(p2)
    print ("P2 size {}".format(len(p2)))

    print ("intersection")
    print (len(p1_domains.intersection(p2_domains)))

    print ("union")
    print (len(p1_domains.union(p2_domains)))

def get_compressed_domains(gz_file):
    f = gzip.open(gz_file, 'rb')
    domains = list()
    c = 0
    for line in f.readlines():
        domain_array = line.strip().split()  # by tab or space
        if len(domain_array) > 1:
            domain = domain_array[0]
            domains.append(domain)

    return domains


def recursive_glob(rootdir='.', suffix=''):
    return [os.path.join(looproot, filename)
            for looproot, _, filenames in os.walk(rootdir)
            for filename in filenames if filename.endswith(suffix)]


def recursively_analyze_gz_files(direcory):
    files = recursive_glob(direcory,'.gz')
    files.sort()
    print ("[Stat]TOTALLY we analyze {} files".format(len(files)))

    args_list = list()
    for i,f in enumerate(files):
        print ("We get {}-th file as {}".format(i, f))
        args_list.append(f)

    n_core = multiprocessing.cpu_count()
    print ("[Stat]The cores we use is {}".format(n_core))
    pool = Pool(n_core)
    res = pool.map(get_compressed_domains, args_list)

    totalDomains = list()
    for i in res:
        totalDomains.extend(i)
    print (len(totalDomains))


def recursively_analyze_gz_files_no_multipleProcess(direcory):
    files = recursive_glob(direcory,'.gz')
    files.sort()
    print ("[Stat]TOTALLY we analyze {} files".format(len(files)))

    args_list = list()
    for i,f in enumerate(files):
        args_list.append(f)

    totalDomains = list()
    for i in args_list:
        print ("We are analyzing {}".format(i))
        domains = get_compressed_domains(i)
        totalDomains.extend(domains)

    print ("Leng of the List is {}".format(len(totalDomains)))
    totalDomains = set(totalDomains)

    print ("leng of the Set is {}".format(len(totalDomains)))
    print (len(totalDomains))

    return totalDomains

if __name__ == "__main__":
    directory = "/home/datashare/dns/history/20170906/"
    #directory = "/home/ketian/Desktop/toad_test_dataset/20170906/"
    #recursively_analyze_gz_files(directory)
    recursively_analyze_gz_files_no_multipleProcess(directory)