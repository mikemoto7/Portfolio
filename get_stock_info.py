#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append('lib')
sys.path.append('bin')

import os, re
from   web_requests import get_web_data
import getopt
from launch_threads import launch_threads
import time
from logging_wrappers import reportError, reportWarning

# import test_flags


#====================================================

scriptName = os.path.basename(sys.argv[0])

def usage():
    print("Runstring help:")
    print('')
    print((scriptName + " [--r|--rlh] --sp symbol,symbol,..."))
    print("--sp symbol,symbol,... = Get current share prices.")
    print("--r = Get current share prices in a loop so you can watch them change dynamically.")
    print("--rlh = Same as --r but also display low and high for the current running of this script.  Show alert flags when bottom or top are breached.")
    print('')
    print((scriptName + " --ac symbol,symbol,..."))
    print("--ac symbol,symbol,... = Get asset class names.")
    print('')

    sys.exit(0)

#====================================================

global symbols_csv_string
symbols_csv_string = ''

def get_share_price(symbols_csv_string):
    # Can also use--  http://www.jarloo.com/yahoo_finance/
    url = "https://www.google.com/finance/info?q=" + symbols_csv_string
    rc, results = get_web_data(url, json_data=True)
    if rc != 0:
        return rc, reportError("Calling get_web_data().  Symbol: " + symbols_csv_string + ".  Results: " + str(results), mode="return_msg_only")
    # print results
    # print results.content
    # for entry in results:
    #    print entry['t'] + ":" + entry['l']
    # return 0, results[0]['l']

    return_dict = {}
    for entry in results:
          # if hasattr(test_flags, '_product_called_from_test'):
          #     if test_flags._product_called_from_test == True:
          #         # called from within a test run
          #         return_dict[entry['t']] = '20.00'
          #         continue 
          # called normally:
          return_dict[entry['t']] = entry['l']

    return 0, return_dict


#====================================================

def get_and_filter_stock_asset_class(threadname, url=''):
    # global threadname
    symbol = threadname
    # url = "https://finance.yahoo.com/quote/" + symbol + "/profile?p=" + symbol


    '''
    # url = "https://www.bloomberg.com/markets/symbolsearch?query=" + symbol + "&commit=Find+Symbols"
    rc, results = get_web_data(url, json_data=False)
    # print 60, threadname
    if rc != 0:
       return rc, reportError("Calling get_web_data().  Symbol: " + symbols_csv_string + ".  Results: " + str(results), mode="return_msg_only")

    results_list = results.content.split('\n')
    for index in xrange(len(results_list)):
       if 'Industry/Objective' in results_list[index]:
           # print("%s:%s" % (symbol, results_list[index+7].replace('<td>','').replace('</td>', '')))
           return 0, symbol + ':' + results_list[index+7].replace('<td>','').replace('</td>', '')
    return 1, symbol + ':None'
    '''

    '''
    url = "https://www.google.com/finance?q=" + symbol
    rc, results = get_web_data(url, json_data=False)
    # print 77, threadname
    if rc != 0:
       return rc, reportError("Calling get_web_data().  Symbol: " + symbols_csv_string + ".  Results: " + str(results), mode="return_msg_only")

    results_list = results.content.split('\n')
    for index in xrange(len(results_list)):
       if 'Morningstar category:' in results_list[index]:
           # print("%s:%s" % (symbol, results_list[index+7].replace('<td>','').replace('</td>', '')))
           return 0, symbol + ':' + re.sub('</*div[^>]*>', '', results_list[index]).replace('Morningstar category: ', '')
    return 1, symbol + ':None'
    '''

    if symbol == 'NOSYMB':
        return 0, 'NOSYMB:NOSYMB'

    url_list = [ "http://www.morningstar.com/funds/XNAS/" + symbol + "/quote.html", "http://www.morningstar.com/funds/XNYS/" + symbol + "/quote.html"]
    if url != '':
        url_list.insert(0, url)

    return_msg = reportError("Calling get_web_data().  Symbol: " + symbol + ".  url_problem .", mode="return_msg_only")
    rc = 1
    for url_entry in url_list:
        rc, results = get_web_data(url_entry, json_data=False)
        # print 77, threadname
        if rc == 0:  break
        return_msg += reportError("Calling get_web_data().  Symbol: " + symbol + ".  url_entry = " + url_entry + " .  Results: " + str(results), mode="return_msg_only")

    if rc != 0:
        return rc, return_msg

    results_list = str(results.content).split('\n')
    # print(106, results_list)
    for index in range(len(results_list)):
        if '"fundCategoryName":' in results_list[index]:
            # print("%s:%s" % (symbol, results_list[index+7].replace('<td>','').replace('</td>', '')))
            return 0, symbol + ':' + re.sub('^.*?"fundCategoryName":"*([^"]*)"*,.*$', r'\1', results_list[index])

    if not re.search('error', str(results.content), re.IGNORECASE):
        return 0, symbol + ':Individual_Stocks'

    return 1, reportError("get ac for symbol " + symbol + " = not_found.  url_entry = " + url_entry + " .  Results: " + str(results), mode="return_msg_only")



def get_stock_asset_class(symbols_csv_string):
    global threadname
    func_dict = {}
    all_results = ''
    # func_call = globals()['get_and_filter_stock_asset_class']()
    for symbol in symbols_csv_string.split(','):
        if symbol == 'NOSYMB':
            all_results += 'NOSYMB:NOSYMB'
            continue
        threadname = symbol
        # func_dict[symbol] = {'func':get_and_filter_stock_asset_class(symbol), 'timeout':5}
        # func_dict[symbol] = {'func':globals()['get_and_filter_stock_asset_class'](symbol), 'timeout':5}
        func_dict[symbol] = {'func':get_and_filter_stock_asset_class, 'args': None, 'timeout':5}
        # func_dict[symbol] = {'func':globals()['get_and_filter_stock_asset_class'](), 'timeout':5}
        # func_dict[symbol] = {'func':func_call, 'param': symbol, 'timeout':5}
        # print 72, threadname

    rc, all_results_temp = launch_threads(func_dict=func_dict)

    all_results += all_results_temp

    '''
       # url = "http://www.morningstar.com/funds/XNAS/" + symbol + "/quote.html"
       # url = "http://quotes.morningstar.com/fund/f?t=" + symbol
       url = "https://www.bloomberg.com/markets/symbolsearch?query=" + symbol + "&commit=Find+Symbols"
       rc, results = get_web_data(url, json_data=False)
       if rc != 0:
          return rc, reportError("Calling get_web_data().  Symbol: " + symbols_csv_string + ".  Results: " + str(results), mode="return_msg_only")
    '''


    if rc != 0:
        return rc, reportError("launch_threads() error.  results: " + all_results, mode='return_msg_only')
    else:
        return rc, all_results

    # return_dict = {}
    # for entry in results:
    #    return_dict[entry['t']] = entry['l']
    #
    # return 0, return_dict


#====================================================



if __name__ == '__main__':

    import command_list
    command_list.command_list(argv=sys.argv)

    if len(sys.argv) == 1:
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["ac=", "sp=", "spr=", "sprlh="])
    except:
        print("ERROR: Unrecognized runstring option.")
        usage()

    symbols_csv_string = ''

    not_repeating = 'no'
    show_curr_price = 'show_curr_price'
    show_curr_price_and_low_high = 'show_curr_price_and_low_high'
    repeating_loop = not_repeating
    action = ''

    low = 0.0
    high = 0.0

    for opt, arg in opts:
        if opt == "--sp" or opt == "--spr" or opt == "--sprlh":
            action = opt
            symbols_csv_string = arg
        elif opt == "--ac":
            symbols_csv_string = arg
            rc, results = get_stock_asset_class(symbols_csv_string)
            if rc != 0:
                print(("ERROR: near line 121: rc = " + str(rc) + ", results = " + results))
            print(results)
            sys.exit(rc)
        else:
            print(("ERROR: Unrecognized runstring option: " + opt))
            usage()

    low_high = {}
    flag = ''
    while True:
        rc, results = get_share_price(symbols_csv_string)
        if rc == 0:
            for key, value in dict.items(results):
                if action == 'spr' or action == 'sprlh':
                    flag_change = ''

                    value_float = float(value)
                    if low_high.get(key, False) == False:
                        low_high[key] = {'low': value_float, 'low_count': 0, 'high': value_float, 'high_count': 0}

                    low = low_high[key]['low']
                    if value_float < low:
                        low = value_float
                        low_high[key]['low'] = low
                        low_high[key]['low_count'] += 1
                        low_count = low_high[key]['low_count']
                        high_count = low_high[key]['high_count']
                        flag_change = 'vvv'
                        flag = 'v %d ^ %d' % (low_count, high_count)

                    high = low_high[key]['high']
                    if value_float > high:
                        high = value_float
                        low_high[key]['high'] = high
                        low_high[key]['high_count'] += 1
                        high_count = low_high[key]['high_count']
                        low_count = low_high[key]['low_count']
                        flag_change = '^^^'
                        flag = '^ %d V %d' % (high_count, low_count)

                    from datetime import datetime
                    datestamp = datetime.now().strftime('%Y%m%d%H%M%S')

                    print(("%s %s %.2f  %.2f %.2f %s %s" % (datestamp, key, value_float, low, high, flag, flag_change)))
                else:
                    print((key + ' ' + value))

            '''
            for entry in results:
               print entry['t'] + ":" + entry['l']

               print
               for key,value in dict.items(entry):
                  print key + " : " + value
               '''

        if action == '--sp':
            break




        try:
            time.sleep(5)
        except:
            sys.exit(0)
