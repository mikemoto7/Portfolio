#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, re

output = ''

if len(sys.argv) == 1:
    print "Usage:"
    print "grep_xml_list.py search_strings xml_file"
    print "grep_xml_list.py search_strings xml_file return_xml_line_1:return_xml_line_2:..."
    print "grep_xml_list.py search_strings xml_file full"
    print "where"
    print "search_strings = str1:str2:...  All strings must be present for a match to occur."
    print "return_xml_line_1:return_xml_line_2:... = If a match occurs, return these lines from the Investment entry."
    print
    print "If return_xml_line params are not specified, this script will return search_strings matching lines, the same behavior as the regular grep command."
    print
    print "full = Return whole <investment> entries that contain all of the matching search strings."
    print
    sys.exit(1)

search_strings = sys.argv[1]
xml_file = sys.argv[2]

full_entry = False
wanted_xml_lines = ''
if len(sys.argv) == 4:
    wanted_xml_lines = sys.argv[3]
    if wanted_xml_lines == 'full':
        full_entry = True
else:
    wanted_xml_lines = search_strings

num_matches = 0
fileline_num = 0
investment_start_line_num = 0
for line in open(xml_file, 'r').read().splitlines():
    fileline_num += 1

    found = re.search('^[ ]*<Investment>$', line)
    if found:
        investment_start_line_num = fileline_num
        search_string_list = search_strings.split(':')
        investment_entry = line
        wanted_xml_list = wanted_xml_lines.split(':')
        return_xml_list = []
        continue

    found = re.search('^[ ]*</Investment>$', line)
    if found:
        investment_entry += line + '\n'
        if len(search_string_list) == 0:
            # output += "Investment Match: File line " + str(investment_start_line_num) + '\n'
            if full_entry:
                output += investment_entry
            else:
                for return_line in return_xml_list:
                    output += return_line + '\n'
            num_matches += 1
        investment_start_line_num = 0
        continue

    if investment_start_line_num > 0:
        if full_entry:
            investment_entry += line + '\n'
        else:
            for wanted_xml_line in wanted_xml_list:
                if wanted_xml_line in line:
                    return_xml_list.append(str(fileline_num) + ":" + line)
                    wanted_xml_list.remove(wanted_xml_line)

        for string_to_match in search_string_list:
            if string_to_match in line:
                search_string_list.remove(string_to_match)
                break

print "Matches = " + str(num_matches)
print output
