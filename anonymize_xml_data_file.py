#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append('lib')
sys.path.append('bin')

import os, re
import getopt
import time

#====================================================

scriptName = os.path.basename(sys.argv[0])

def usage():
    print("Runstring help:")
    print()
    print(scriptName + " xml_data_file")
    print("Anonymize your data file.")
    print()

    sys.exit(0)

#====================================================



if __name__ == '__main__':

    if len(sys.argv) == 1:
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["ac=", "sp=", "r"])
    except:
        print("ERROR: Unrecognized runstring option.")
        usage()

    symbols_csv_string = ''
    repeating_loop = False

    for opt, arg in opts:
        if opt == "--sp":
            symbols_csv_string = arg
        else:
            print("ERROR: Unrecognized runstring option: " + opt)
            usage()


    anon_doc = []
    curr_quantity = 50.000
    cb_quantity = 10.0
    account_ID = 777
    owner = 'owner1'
    owner_short = 'os1'
    for line in open(args[0], 'r').read().splitlines():
        found = re.search("^( *)(<curr_quantity>)[0-9.]*(</curr_quantity>)$", line)
        if found:
            anon_doc.append(found.group(1)+found.group(2)+str(curr_quantity)+found.group(3))
            curr_quantity += 10.000
            continue

        found = re.search("^( *)(<account_ID>)[^<]*(</account_ID>)$", line)
        if found:
            anon_doc.append(found.group(1)+found.group(2)+str(account_ID)+found.group(3))
            account_ID += 1000
            continue

        found = re.search("^( *)(<owner>).*(</owner>)$", line)
        if found:
            if owner == 'owner1':
                owner = 'owner2'
            else:
                owner = 'owner1'
            anon_doc.append(found.group(1)+found.group(2)+str(owner)+found.group(3))
            continue

        found = re.search("^( *)(<owner_short>).*(</owner_short>)$", line)
        if found:
            if owner_short == 'os1':
                owner_short = 'os2'
            else:
                owner_short = 'os1'
            anon_doc.append(found.group(1)+"<owner_short>"+owner_short+"</owner_short>")
            continue

        found = re.search("^( *)(<description>).*(</description>)$", line)
        if found:
            anon_doc.append(found.group(1)+found.group(2)+'TBD'+found.group(3))
            continue

        found = re.search("^( *)(<filename>).*(</filename>)$", line)
        if found:
            anon_doc.append(found.group(1)+found.group(2)+'demo_data_file.xml'+found.group(3))
            continue

        found = re.search("^( *)(<cb_quantity>)[0-9-\.]*(</cb_quantity>)$", line)
        if found:
            anon_doc.append(found.group(1)+found.group(2)+str(cb_quantity)+found.group(3))
            cb_quantity += 10
            continue


        anon_doc.append(line)

    for row in anon_doc:
        print(row)
