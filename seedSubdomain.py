#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ketian'
__version__ = '1.04b'
__email__ = 'ririhedou@gmail.com'


import tldextract

KEYWORDS = ['aws']

def aws_subdomain_ratio(_f):
    f = open(_f, 'rb')
    subdomain_count = 0
    no_domain_count = 0

    lines = list()
    for line in f.readlines():
        domain = line.strip()  # by tab or space
        ex = tldextract.extract(domain)
        if ex.domain == "amazonaws":
            lines.append(line)

    f_write = open("AWS_subdomain.txt", 'wb')
    for i in lines:
        f_write.write(i)
    f_write.close()


if __name__ == "__main__":
    log_file = "aws.log"
    aws_subdomain_ratio(log_file)
