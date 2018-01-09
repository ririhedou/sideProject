#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ketian'
__version__ = '1.04b'
__email__ = 'ririhedou@gmail.com'


from historyDataChange import *
import tldextract

KEYWORDS = ['aws']


def domain_subdomain_ratio(gz_file):
    f = gzip.open(gz_file, 'rb')
    subdomain_count = 0
    no_domain_count = 0
    for line in f.readlines():
        domain_array = line.strip().split()  # by tab or space
        if len(domain_array) > 1:
            domain = domain_array[0]
            ex = tldextract.extract(domain)
            if ex.subdomain:
                subdomain_count += 1
            else:
                no_domain_count += 1

    print ("No_sub_domain Count", no_domain_count)
    print ("Sub_domain Count", subdomain_count)
    return subdomain_count, no_domain_count


def recursive_glob(rootdir='.', suffix=''):
    return [os.path.join(looproot, filename)
            for looproot, _, filenames in os.walk(rootdir)
            for filename in filenames if filename.endswith(suffix)]


def run_analysis(direcory):
    files = recursive_glob(direcory, '.gz')
    files.sort()

    print ("[Stat]Total Size of files are {}".format(len(files)))
    args_list = list()
    for i, f in enumerate(files):
        args_list.append(f)

    sub, no_sub =0, 0
    for i in args_list:
        s, no_s = domain_subdomain_ratio(i)
        sub += s
        no_sub += no_s

    print ("Total sub", sub, "Total no sub", no_sub)
    return


if __name__ == "__main__":
    directory = "/home/ketian/Desktop/toad_test_dataset/20170906/"
    run_analysis(directory)