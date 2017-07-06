#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, re
import getopt

#====================================================

def replace_block(xml_file, search_block_file, replacement_xml_file):

    search_block = []
    for line in open(search_block_file, 'r').read().splitlines():
        search_block.append(line)

    xml_file_lines = open(xml_file, 'r').read().splitlines()
    index = -1
    while True:
        index += 1
        if index >= len(xml_file_lines):
            break
        save_lines = []
        match = False
        for row in search_block:
            save_lines.append(xml_file_lines[index])
            if row != xml_file_lines[index]:
                match = False
                break
            index += 1
            match = True
        if match == False:
            for line in save_lines:
                print(line)
            continue

        fd = open(replacement_xml_file, 'r')
        for row in fd.read().splitlines():
            print(row)
        fd.close()

#====================================================

def replace_line(xml_file, search_string, replacement_xml_file):

    for line in open(xml_file, 'r').read().splitlines():
        found = re.search('^([ ]*)'+search_string+'$', line)
        if not found:
            print(line)
            continue

        indent = found.group(1)
        fd = open(replacement_xml_file, 'r')
        for row in fd.read().splitlines():
            print(indent + row)
        fd.close()

#====================================================

def replace_substring(xml_file, search_string, replace_string, replacement_string):

    for line in open(xml_file, 'r').read().splitlines():
        found = re.search('^([ ]*)(.*'+search_string+'.*)$', line)
        if not found:
            print(line)
            continue

        indent = found.group(1)
        xml_string = found.group(2)
        revised_xml_string = xml_string.replace(replace_string, replacement_string)
        print(indent + revised_xml_string)

#====================================================

def add_inv_ID_field(xml_file):

    count = 0
    for line in open(xml_file, 'r').read().splitlines():
        search_string = '<account_ID>'
        found = re.search('^([^<]*)'+search_string, line)
        if not found:
            print(line)
            continue

        indent = found.group(1)
        count += 1
        print(indent + '<inv_ID>' + str(count) + '</inv_ID>')
        print(line)

#====================================================

def insert_field(xml_file, existing_field, field_to_insert):

    for line in open(xml_file, 'r').read().splitlines():
        found = re.search('^([^<]*)'+existing_field, line)
        if not found:
            print(line)
            continue

        indent = found.group(1)
        print(indent + field_to_insert) # example:   </cost_basis>
        print(line)

#====================================================

def del_line(xml_file, search_string, del_string):

    filelist = open(xml_file, 'r').read().splitlines()
    index = -1
    while True:
        index += 1
        if index >= len(filelist):  break
        found = re.search('^([ ]*)(.*'+search_string+'.*)$', filelist[index])
        if found:
            print(filelist[index])
            index += 1
            found = re.search('^([ ]*)(.*'+del_string+'.*)$', filelist[index])
            if found:
                continue
        print(filelist[index])


#====================================================

scriptName = os.path.basename(sys.argv[0])

def usage():
    print('''
Runstring help:
'''.strip())
    print(scriptName + " --replace xml_file  search_string  replacement_xml_file")
    print(scriptName + " --replace_string xml_file  search_string  replace_string  replacement_string")
    print(scriptName + " --replace_block xml_file  block_file  replacement_xml_file")
    print(scriptName + " --add_inv_ID xml_file")
    print(scriptName + " --del xml_file search_string del_string")
    print('''

Adding new field line to every Investment, use sed:
sed 's/^\( *\)<name>\([^<]*\)<\/name>/\\1<name>\\2<\/name>\\n\\1<name_short>\\2<\/name_short>/g' MASTER_LIST.xml  > foo

'''.strip())
    sys.exit(1)

#====================================================



if __name__ == '__main__':

    if len(sys.argv) == 1:
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["replace", "replace_string", "replace_block", "add_inv_ID", "debug", "unit_test", "insert_field", "del"])
    except:
        print("ERROR: Unrecognized runstring option.")
        usage()

    any_option = False

    for opt, arg in opts:
        any_option = True
        if opt == "--replace":
            xml_file = args[0]
            search_string = args[1]
            replacement_xml_file = args[2]
            replace_line(xml_file, search_string, replacement_xml_file)
        elif opt == "--replace_block":
            xml_file = args[0]
            search_block_file = args[1]
            replacement_xml_file = args[2]
            replace_block(xml_file, search_block_file, replacement_xml_file)
        elif opt == "--replace_string":
            xml_file = args[0]
            search_string = args[1]
            replace_string = args[2]
            replacement_string = args[3]
            replace_substring(xml_file, search_string, replace_string, replacement_string)
        elif opt == "--add_inv_ID":
            xml_file = args[0]
            add_inv_ID_field(xml_file)
        elif opt == "--insert_field":
            xml_file = args[0]
            existing_field = args[1]
            field_to_insert = args[2]
            insert_field(xml_file, existing_field, field_to_insert)
        elif opt == "--del":
            xml_file = args[0]
            search_string = args[1]
            del_string = args[2]
            del_line(xml_file, search_string, del_string)
        elif opt == "--debug":
            # setLoggingLevel(logging.DEBUG)
            debug_option = True
        elif opt == "--unit_test":
            unittest_flag = True
        else:
            print("ERROR: Unrecognized runstring option: " + opt)
            usage()

    if any_option == False:
        print("ERROR: Missing required params in runstring.")
        usage()
