#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, sys, re
from pprint import pprint
import Money
from Investments import Investments
from Investment import Investment
from Money import Money
from Investments import update_Master_list
from Investments import copy_list


#========================================================================

scriptName = os.path.basename(os.path.abspath(sys.argv[0])).replace('.pyc', '.py')


def usage():

    print ""
    print "Runstring:"
    print scriptName + " temp_Vanguard_screencopy_Master_file  Master_file"
    print ""
    print "Manually screen-copy our Vanguard accounts page into a text file and then run this script on the text file to get updated share quantities and prices."
    print ""
    sys.exit(1)

#========================================================================

if __name__ == '__main__':

    if len(sys.argv) == 1:
        usage()

    error_list = []

    print "<Investments>"
    print

    rc, results = update_Master_list(sys.argv[1], sys.argv[2])
    # print "rc = " + str(rc)
    error_list = results[0]
    updated_Master_list = copy_list(results[1], "updated_Master_list")

    print updated_Master_list.__str__()

    updated_Master_list.__show_stats__()
    error_list += updated_Master_list._errors

    print
    if len(error_list) > 0:
        print "<errors>"
        for line in results[0]:
            print line
        print "</errors>"

    print
    print "</Investments>"
