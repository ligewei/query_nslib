#!/usr/bin/env python
# encoding=utf-8

import sys
import csv
import requests
import hashlib
from bs4 import BeautifulSoup

def get_loan_list(login_info):
    login_url = 'http://opac.nslib.cn/MyLibrary/readerLoginM.jsp'
    print '\n-----start login user:' + login_info['username'] + '-----'
    r = requests.post(login_url, login_info)
    #print r
    #print r.cookies
    req_cookies = {}
    req_cookies['JSESSIONID'] = r.cookies['JSESSIONID']
    req_cookies['Username'] = r.cookies['Username']
    req_cookies['UserID'] = r.cookies['UserID']
    req_cookies['recordno'] = r.cookies['recordno']
    req_cookies['Name'] = r.cookies['Name']
    req_cookies['library'] = r.cookies['library']

    #loan_status = 'http://opac.nslib.cn/MyLibrary/Loan-Status.jsp'
    #r = requests.get(loan_status, cookies=req_cookies)
    #print r
    #print r.text

    loan_list = 'http://opac.nslib.cn/MyLibrary/getloanlist.jsp?' + 'readerno=' + req_cookies['recordno']
    #print loan_list
    r = requests.get(loan_list, cookies=req_cookies)
    #print r
    #print r.text
    rsp_trip_up_magic_meta = r.text.replace('meta', 'magic_meta')
    soup = BeautifulSoup(rsp_trip_up_magic_meta, 'lxml')
    print 'Total: ' + soup.root.loanlist.loannum.string

    for loanlist in soup.root.loanlist:
        if loanlist.name == 'magic_meta':
            s = loanlist.recordno.string + "|"
            s += loanlist.loandate.string + "~"
            s += loanlist.returndate.string + "|"
            s += loanlist.local.string + "\t|"
            s += loanlist.title.string
            print s


login_info = {}

if len(sys.argv) != 2:
    print "Usage: python " + sys.argv[0] + " $user_pwd.csv"
    exit(1)
else:
    with open(sys.argv[1], 'rb') as csvfile:
        rd = csv.reader(csvfile)
        for user, pwd in rd:
            login_info['username'] = user
            # md5 pwd
            m = hashlib.md5()
            m.update(pwd)
            login_info['password'] = m.hexdigest()
            # http operation
            get_loan_list(login_info)


