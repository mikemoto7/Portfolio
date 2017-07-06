#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, re

from operator import itemgetter


#==============================================

def traverse_Python_data_tree(command="output", line_break_char="\n", indent=False, key="", Python_data_tree='', search_key='', key_path='', list_of_list_key_paths = []):

    if command == "output":
        result_xml = ''
        result_pdt = []
    elif command == "find_lists":
        result_xml = ''
        result_pdt = []
    elif command == "correct_to_list_type":
        result_xml = ''
        result_pdt = []
    else:  # search
        result_xml = []
        result_pdt = []
        if key_path != '':
            key_path += ":" + key
        else:
            key_path = key

    if type(indent) == bool:
        if indent == False:
            indent_spaces = ''
        else:
            indent_spaces = '   '
        indent = ''
    else:
        if indent == '':
            indent_spaces = ''
        else:
            indent_spaces = '   '


    '''
    print "---------------"
    print "command: " + command
    print "key: " + key
    print "type(Python_data_tree): " + str(type(Python_data_tree))
    # print "len(Python_data_tree): " + str(len(Python_data_tree))
    # print "str(Python_data_tree): " + str(Python_data_tree)
    print "Python_data_tree.__class__.__name__: " + Python_data_tree.__class__.__name__
    if 'dict' in str(type(Python_data_tree)):
       print 'dict:'
       for key,value in Python_data_tree.__dict__.iteritems():
          print key, value
    if 'list' in str(type(Python_data_tree)):
       print 'list.'
    print 'end_str'
    print "key: " + key
    print "search_key: " + search_key
    '''

    Python_data_tree_type = str(type(Python_data_tree))

    # Python_data_tree_name = Python_data_tree.__class__.__name__
    # print 64, "key:" + key + ", Python_data_tree_name: " + Python_data_tree_name + ", Python_data_tree_type: " + Python_data_tree_type


    '''
    if command == "correct_to_list_type":
       if key_path == '':
          temp_key_path = key
       else:
          temp_key_path += ':' + key
       for row in list_of_list_key_paths:
          if temp_key_path == row:
             Python_data_tree_type = 'list'
             break
    '''


    if 'list' in Python_data_tree_type:
        if command == "output":
            # print "key: " + str(key)
            # print "result_xml: " + str(result_xml)
            result_xml += indent + "<" + key + ">" + line_break_char
            result_pdt.append( {
               'type': 'list',
               'indent': indent,
               'key': key,
               'key_path': key_path,
               'full_entry': indent + key + "[ # list",
               'alt_entry': indent + key + ":{ # dict",
               } )
        elif command == "find_lists":
            if key_path == '':
                key_path = key
            else:
                key_path += ':' + key
            already_exists = False
            for row in result_pdt:
                if key_path == row:
                    already_exists = True
                    break
            if already_exists == False:
                result_pdt.append(key_path)
        elif command == 'search':
            if key == search_key:
                if key_path == '':
                    key_path = key
                result_xml.append([key_path, Python_data_tree])

        # print len(Python_data_tree)
        # print Python_data_tree
        for entry in Python_data_tree:
            # print indent + "show2: key: " + key + ", entry: " + str(entry)
            # print indent + key + ":" + str(value[key])
            # print entry.__class__.__name__, entry[0]
            # print "str: " + str(entry)
            result_xml_temp, result_pdt_temp = traverse_Python_data_tree(command=command, indent=indent+indent_spaces, key=entry[0], Python_data_tree=entry[1], search_key=search_key, key_path=key_path, list_of_list_key_paths=list_of_list_key_paths)
            result_xml += result_xml_temp
            result_pdt += result_pdt_temp

        if command == "output":
            if key != '':
                result_xml += indent + "</" + key + ">" + line_break_char
                result_pdt.append( {
                   'type': 'list',
                   'indent': indent,
                   'key': key,
                   'key_path': key_path,
                   'full_entry': indent + "], # list:" + key,
                   'alt_entry': indent + "}, # dict:" + key,
                   } )

    elif 'dict' in Python_data_tree_type.lower():
        if command == "output":
            # print "key: " + str(key)
            # print "result_xml: " + str(result_xml)
            if key != '':
                result_xml += indent + "<" + key + ">" + line_break_char
                result_pdt.append( {
                   'type': 'dict',
                   'indent': indent,
                   'key': key,
                   'key_path': key_path,
                   'full_entry': indent + key + ":{ # dict",
                   'alt_entry': indent + key + "[ # list",
                   } )
        elif command == "find_lists":
            if key_path == '':
                key_path = key
            else:
                key_path += ':' + key
        elif command == 'search':
            if key == search_key:
                if key_path == '':
                    key_path = key
                result_xml.append([key_path, Python_data_tree])

        temp_result_xml = []
        for key_loop, value_loop in dict.items(Python_data_tree):
            # print indent + "show2: key: " + key + ", entry: " + str(entry)
            # print indent + key + ":" + str(value[key])
            # print entry.__class__.__name__
            # print key_loop, value_loop
            temp_result_xml, temp_result_pdt = traverse_Python_data_tree(command=command, indent=indent+indent_spaces, key=key_loop, Python_data_tree=value_loop, search_key=search_key, key_path=key_path, list_of_list_key_paths=list_of_list_key_paths)
            # print "len(result_xml): " + str(len(result_xml))
            # print "len(temp_result_pdt): " + str(len(temp_result_pdt))
            #  temp_result_xml.append([key_loop, temp_result_xml])
            result_xml += temp_result_xml
            result_pdt += temp_result_pdt

        # temp_list_sorted = sorted(temp_list,key=itemgetter(0))
        # for loop in temp_list_sorted:
        #     result_xml += loop[1]

        if command == "output":
            if key != '':
                result_xml += indent + "</" + key + ">" + line_break_char
                result_pdt.append( {
                   'type': 'dict',
                   'indent': indent,
                   'key': key,
                   'key_path': key_path,
                   'full_entry': indent + "}, # dict:" + key,
                   'alt_entry': indent + "], # list:" + key,
                   } )

#   elif 'instance' in Python_data_tree_type:
#       # print Python_data_tree
#       # print '190', Python_data_tree.__class__.__name__
#       # print '191', Python_data_tree_type
#       # print dir(Python_data_tree)
#
#       '''
#       for key,value in Python_data_tree.__dict__.iteritems():
#          print key, value
#
#       '''
#
#       '''
#       if command == "output":
#          if key != '':
#             result_xml += indent + "<" + key + ">" + line_break_char
#             result_pdt.append( {
#                'type': 'instance',
#                'indent': indent,
#                'key': key,
#                'full_entry': indent + '# ' + key + ": instance start",
#                'alt_entry': indent + '# ' + key + ": instance start",
#                } )
#       else:
#          if key == search_key:
#             if key_path == '':
#                key_path = key
#             result_xml.append([key_path, Python_data_tree])
#       '''
#
#       Python_data_tree = Python_data_tree.__class__.__name__
#
#       result_xml_temp, result_pdt_temp = traverse_Python_data_tree(command=command, indent=indent, key=key, Python_data_tree=Python_data_tree, search_key=search_key, key_path=key_path, list_of_list_key_paths=list_of_list_key_paths)
#       result_xml += result_xml_temp
#       result_pdt += result_pdt_temp
#
#       '''
#       if command == "output":
#          if key != '':
#             result_xml += indent + "</" + key + ">" + line_break_char
#             result_pdt.append( {
#                'type': 'instance',
#                'indent': indent,
#                'key': key,
#                'full_entry': indent + '# ' + key + ": instance end",
#                'alt_entry': indent + '# ' + key + ": instance end",
#                } )
#      '''
#

    else:  # single data variable
        if command == "output":
            if key != '':
                # print "--------"
                # print key
                # print "Python_data_tree type: " + str(type(Python_data_tree))
                # print "Python_data_tree type: " + type(Python_data_tree)
                # print "Python_data_tree: " + str(Python_data_tree)
                # print "--------"
                if 'instance' in Python_data_tree_type:
                    Python_data_tree_param = Python_data_tree.__str__()
                elif Python_data_tree == None:
                    Python_data_tree_param = ''
                else:
                    Python_data_tree_param = Python_data_tree

                result_xml += indent + "<" + key + ">" + str(Python_data_tree_param) + "</" + key + ">" + line_break_char
                result_pdt.append( {
                   'type': 'element',
                   'indent': indent,
                   'key': key,
                   'key_path': key_path,
                   'full_entry': indent + key + ':' + str(Python_data_tree_param) + ',',
                   'alt_entry': indent + key + ':' + str(Python_data_tree_param) + ',',
                   } )

        elif command == 'search':
            if key == search_key:
                if key_path == '':
                    key_path = key
                result_xml.append([key_path, Python_data_tree])


    '''
    for entry in result_xml:
       print "--------"
       print entry
       print type(entry)
       for row in entry:
          print row
          print type(row)

    for item in list(map(lambda x: x[1], result_xml)):
       print item
    '''

    '''
    TBD: Need to implement a better way of detecting dict vs. list usage:

       for index in xrange(len(output_pdt)):
          if output_pdt[index]['type'] == 'list':
             continue
          count = 0
          for index2 in xrange(len(output_pdt)):
             if output_pdt[index]['key'] == output_pdt[index2]['key'] and index != index2:
                count += 1
                if count > 1:
                   break
          if count > 1:
             for index2 in xrange(len(output_pdt)):
                if output_pdt[index]['key'] == output_pdt[index2]['key']:
                   output_pdt[index2]['type'] = 'list'
                   output_pdt[index2]['full_entry'] = output_pdt[index2]['alt_entry']

    '''



    # print("result_xml: %s" % result_xml)
    # print "len(result_xml): " + str(len(result_xml))


    # Remove duplicates.
    if key == "top" and command == "find_lists":
        temp_result_pdt = []
        for row in result_pdt:
            if row in temp_result_pdt:
                continue
            temp_result_pdt.append(row)
        result_pdt = temp_result_pdt



    return result_xml, result_pdt
