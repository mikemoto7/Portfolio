#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, re

from operator import itemgetter

scriptName = os.path.basename(__file__).replace('.pyc', '.py')
scriptDir  = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptDir + '/lib')
sys.path.append(scriptDir + '/bin')

from Money import Money
from traverse_Python_data_tree import traverse_Python_data_tree
from logging_wrappers import reportError


class Investment():

    #==============================

    def __init__(self, Investment_Python_data_tree=None):

        self._Investment_Python_data_tree = Investment_Python_data_tree

        self._errors = []

    #==============================

    def get_total_value(self):
        if self._fields["share_price"] == "TBD_share_price" or self._fields["quantity"] == "TBD_quantity":
            return "TBD_total_value"

        return Money().set_by_string(self._fields["share_price"]).mult(self._fields["quantity"]).__str__()

    #==============================

    def sort_str(self, fields_dict):
        fields_list_sorted = []

        for key, value in dict.items(fields_dict):
            if type(value) is dict:
                rc, value = self.sort_str(value)

            fields_list_sorted.append([key, value])

        sorted(fields_list_sorted,key=itemgetter(0))

        return 0, fields_list_sorted

    #==============================

    def __str__(self, command="output", line_break_char="\n", indent=False, key="", Investment_Python_data_tree='', search_key='', key_path=''):
        if Investment_Python_data_tree == '':
            Investment_Python_data_tree = self._Investment_Python_data_tree
        result = traverse_Python_data_tree(command=command, line_break_char=line_break_char, indent=indent, key=key, Python_data_tree=Investment_Python_data_tree, search_key=search_key, key_path=key_path)
        return str(result)

    #==============================

    def get_fields(self):
        output_list = []

        for key in sorted(self._Investment_Python_data_tree.keys()):
            output_list.append("<" + key + ">" + self._fields[key] + "</" + key + ">")

        return output_list

    #==============================

    def search_value(self, key):
        result_list = traverse_Python_data_tree(command="search", search_key=key, Python_data_tree=self._Investment_Python_data_tree)
        return result_list

    #==============================

    def get_value(self, key_path):
        '''
        Example key_path--  cost_basis:cb_event[1]:cb_total_value
        cb_event is a list, so you must specify which list cell to use.

        '''
        '''
        print self._Investment_Python_data_tree
        temp = dict(self._Investment_Python_data_tree)
        # for key,value in dict.items(self._Investment_Python_data_tree):
        print str(temp)
        for key,value in dict.items(temp):
           print key, value
        if key not in self._Investment_Python_data_tree:
           reportError("Key " + key + " does not exist in Investment instance.")
           return "Key_" + key + "_does_not_exist"
        '''

        # print "key_path", key_path
        value = ''
        for key in key_path.split(':'):
            # print '90', key, str(type(value)), value
            if value == '':
                value = self._Investment_Python_data_tree[key]
                # print "93", key, str(type(value)), value
                continue
            if 'list' in str(type(value)):
                # print "96", key, "value", value
                '''
                found = re.search('^[^\[]+\[([^\]]+)]', value)
                if not found:
                   reportError("Could not find index for value " + str(value))
                   return ''
                index = int(found.group(1))
                value = value[index]
                '''
                value = value[-1]
                continue

            if 'dict' in str(type(value)):
                value = value[key]
                # print "106", key, "value", value

        # print '112', key, str(type(value)), value
        return value

    #==============================

    def set_value(self, key, value):
        self._Investment_Python_data_tree[key] = value

    #==============================

    '''
    def valid_format(self, investment):
       investment._errors = []
       rc = -1
       for key in sorted(self._fields.keys()):
          if investment.get_value(key) is None:
             msg = "ERROR: Field " + key + " missing from investment record " + investment.get_value("name")
             reportError(msg)
             investment._errors.append(msg)
             rc = 1
          else:
             if rc != 0:
                continue
             rc = 0

       if rc == -1:
          rc = 0
       return rc
    '''

    #==============================

    def get_ID(self):
        symbol = self.get_value("symbol")
        account_ID = self.get_value("account_ID")
        owner = self.get_value("owner")
        name = self.get_value("name")
        return symbol + "," + account_ID + "," + owner + "," + str(name.encode('utf-8'))

    #==============================
