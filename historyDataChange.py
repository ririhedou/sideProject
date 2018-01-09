#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ketian'
__version__ = '1.04b'
__email__ = 'ririhedou@gmail.com'

import os
import gzip
from multiprocessing import Pool
import multiprocessing
import tldextract

def intersection_of_domains(p1, p2):
    print ("Analyzing {}".format(p1))
    p1_domains = recursively_analyze_gz_files_no_multipleProcess(p1)
    print ("{} size {}".format(p1, len(p1_domains)))

    print ("Analyzing {}".format(p2))
    p2_domains = recursively_analyze_gz_files_no_multipleProcess(p2)
    print ("{} size {}".format(p2, len(p2_domains)))

    print ("\nIntersection"),
    print (len(p1_domains.intersection(p2_domains)))

    print ("\nUnion"),
    print (len(p1_domains.union(p2_domains)))

    print ("\n")

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
    files = recursive_glob(direcory, '.gz')
    files.sort()

    print ("[Stat]Total Size of files are {}".format(len(files)))
    args_list = list()
    for i, f in enumerate(files):
        args_list.append(f)

    totalDomains = list()

    for i in args_list:
        domains = get_compressed_domains(i)
        totalDomains.extend(domains)

    print ("[Stat]Leng of the List is {}".format(len(totalDomains)))
    totalDomains = set(totalDomains)

    print ("[Stat]Leng of the Set is {}".format(len(totalDomains)))

    return totalDomains


def url_subdomain_ratio(totalDomains):
    subdomain_count = 0
    no_domain_count = 0

    for domain in totalDomains:
        ex = tldextract.extract(domain)
        if ex.subdomain:
            subdomain_count += 1
        else:
            no_domain_count += 1

    print ("No_sub_domain Count", no_domain_count)
    print ("Sub_domain Count", subdomain_count)


if __name__ == "__main__":

    directory = "/home/datashare/dns/history/20170906/"
    #directory = "/home/ketian/Desktop/toad_test_dataset/20170906/"
    totalDomains = recursively_analyze_gz_files(directory)
    url_subdomain_ratio(totalDomains)

    #recursively_analyze_gz_files_no_multipleProcess(directory)
    #p1 = "/home/datashare/dns/history/20170906/"
    #p2 = "/home/datashare/dns/history/20170905/"
    #p3 = "/home/datashare/dns/history/20170806/"
    #intersection_of_domains(p1, p3)