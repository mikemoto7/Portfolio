#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, re
import getopt
from web_requests import get_web_data
from columnize_output import columnize_output
import string


#====================================================

scriptName = os.path.basename(sys.argv[0])

def usage():
    print('''
Runstring help:
'''.strip())
    print("   " + scriptName + " symbol1,symbol2,symbol3")
    print('''

TBD
'''.strip())
    sys.exit(1)

#====================================================



if __name__ == '__main__':

    if len(sys.argv) == 1:
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["debug", "get="])
    except:
        print("ERROR: Unrecognized runstring option.")
        usage()

    get_url = ''
    debug = False

    for opt, arg in opts:
        any_option = True
        if opt == "--debug":
            debug = True
        elif opt == "--get":
            get_url = arg
        else:
            print("ERROR: Unrecognized runstring option: " + opt)
            usage()

    tempfile = scriptName + ".for_debug.txt"
    fd = open(tempfile, 'w')

    table = ['Ticker,Name,Stars']
    for symbol in args[0].split(','):
        # url = "http://performance.morningstar.com/fund/ratings-risk.action?t=" + symbol + "&region=usa&culture=en-US"
        url = "http://performance.morningstar.com/fund/ratings-risk.action?t=" + symbol + "&region=usa&culture=en-US"
        # url = "http://www.morningstar.com/funds/xnas/" + symbol + "/quote.html"
        # url = "http://performance.morningstar.com/fund/performance-return.action?t=" + symbol + "&region=usa&culture=en_US"
        # Does not work: url = "http://performance.morningstar.com/fund/performance-return.action?t=" + symbol + "&region=usa&culture=en_US&id=tab-1day-content"
        # Does not work: url = "http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t=" + symbol + "&reportType=is&period=12&dataType=A&order=asc&columnYear=5&number=3"
        # Does not work: url = "http://quotespeed.morningstar.com/quote.jsp?&jsoncallback=jQuery172017541670752689242_1441265385395&preAfter=1&ty=D&mtype=ST&exch=126&ticker=VEIPX&stype=1&days=5&_tid=1441265386097&ver=1.6.0&f=1&instid=MSRT&sdkver=2.1.20150320&qs_wsid=2D2114F870F6B844CDF8271C99BB8C7A&_=1441265386099"


        rc, results = get_web_data(url=url, json_data=False)
        if rc != 0:
            print("ERROR: get_web_data() error: " + str(results))
            sys.exit(1)

        fd.write(results.content + '\n')

        # for line in results.content:
        #    fd.write(line + '\n')

        for line in results.content.split('\n'):
            # print "71 line: ", line
            stars = ''
            name  = ''
            ticker = ''
            found = re.search('starRating":([^,]+),', line)
            if found:
                stars = found.group(1)
                if debug: print("72", line)
            found = re.search('ticker":"([^"]+)"', line)
            if found:
                ticker = found.group(1)
            found = re.search('securityName":"([^"]+)"', line)
            if found:
                name = re.sub(r'[^\x00-\x7f]',r'', found.group(1))
            if stars != '' and name != '' and ticker != '':
                table.append(ticker + ',' + name + ',' + stars)
                break
            if stars == '' and name == '' and ticker == '':
                continue

            print("ERROR: Cannot find all field values for " + symbol + ": stars = '" + stars + "', name = '" + name + "', ticker = '" + ticker + "'")
            print("line: " + line)
            continue

    fd.close()

    rc, table_columnized = columnize_output(input_data=table, justify_cols="L,L,L", save_filename=scriptName)

    for row in table_columnized:
        print(row)
