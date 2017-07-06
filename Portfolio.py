#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
%(scriptName)s Script Description:

An xml data file is used to store your investment information.
You must create this xml data file manually and update it manually.  Some commands can help you with this updating, e.g., automatically go out to the web to retrieve the latest share prices.
All commands require this xml data file.
Each command:
- Reads the xml data file and creates a long xml string from it.
- The xml string is converted into a Python data structure tree (abbrev: pdt) made up of:
   - lists (e.g., Investments, cost_basis)
   - dicts (e.g., Investment)
   - elements (e.g., account_number, symbol)
   - object instances (e.g., Investment, Money)
- The commands read and query this Python data structure to do their work.


Runstring help:

General Options:

   %(scriptName)s
      With no options, displays this help screen.

   %(scriptName)s ... --pfile Portfolio_xml_file
   %(scriptName)s ... --pfile $Portfolio_xml_file_env_variable
      Portfolio_xml_file can be the relative or full path name to your Portfolio_xml_file.  For security purposes, it can also be the name of an environment variable containing the path.

   %(scriptName)s --price_web_update --pfile Portfolio_xml_file
      Use stock prices from the web.  This option can be used with any other option, but it is ignored when the 'diff' option is used.  See the 'diff' section for details.

   %(scriptName)s --ac_web_update --pfile Portfolio_xml_file
      Use asset class names from the web to identify incorrect assset class categorization in our xml data file.

Views:

   %(scriptName)s --stats --pfile Portfolio_xml_file
      List out the stats for your xml file.

   %(scriptName)s --xml --pfile Portfolio_xml_file
      List out the xml from your xml file.  More than just listing the file, this script will read and error-check each xml line and nested block.  Because of the potential large amount of output, when this command is used, no other runstring commands will be performed.

      To capture current share prices, you can add the --price_web_update option and redirect this output to a new empty candidate xml file and use that to replace your existing xml data file:

         %(scriptName)s --price_web_update --xml --pfile Portfolio_xml_file

Analyses:

   Percents Table:

      %(scriptName)s --pt show --pfile Portfolio_xml_file
         Show both the percent table and the brokerage/owner tables.

      %(scriptName)s --pt show_percent --pfile Portfolio_xml_file
         Show the percent table.

      %(scriptName)s --pt show_ac_misc_totals --pfile Portfolio_xml_file
         Show the brokerage/owner tables.

      %(scriptName)s --pt lp --pfile Portfolio_xml_file
         Show the asset classes with the lowest percentages.  Focus on investing in these to balance asset allocation.

      %(scriptName)s --pt add:'Small Value',Non_Retirement,50000:'Small Value',Retirement,20000:Healthcare,Retirement,50000 --pfile Portfolio_xml_file
         Temporarily add dollars to asset classes to see how asset class percentages will change.
         Note that the 'add' params are strung together with ':'.  So all of these 'add' param results will show up on the same table.  If you string them together using '%%', they will be treated as separate commands and show up on separate tables.

      %(scriptName)s --pt lp%%add:'Small Value',Non_Retirement,50000:'Small Value',Retirement,20000:Healthcare,Retirement,50000%%lp --pfile Portfolio_xml_file
         You can string together options using the %% character.  NOTE: When strung together like this, the 'add' option temporary changes will affect the rest of the 'show...' options in the --pt option.

      %(scriptName)s --pt add:'Small Value',Non_Retirement,50000:'Small Value',Retirement,20000:Healthcare,Retirement,50000%%lp_diff --pfile Portfolio_xml_file
         lp_diff after an add will show you the effect the add had on before-and-after lowest percentages sortinig/ranking.


   Investments Table:

      %(scriptName)s --inv show --pfile Portfolio_xml_file
         Show investments general data.

      %(scriptName)s --inv diff --pfile Portfolio_xml_file
         Do a diff between the xml file and the xml file updated by the web.

      %(scriptName)s --inv diff --pfile Portfolio_xml_file1,Portfolio_xml_file2
         Do a diff between two xml files.  Neither are updated by the web.

      %(scriptName)s --inv lots --pfile Portfolio_xml_file
         Show investment cost basis purchase lots for sell planning.

   All:

      %(scriptName)s --all [--silent] show --pfile Portfolio_xml_file
         Create and display all of the major results tables.  Commands used:

            %(all_option_preconfigured)s

Misc. Commands:

   %(scriptName)s --noindent  ... --pfile Portfolio_xml_file
      Indentation of displayed xml is the default.  To disable indentation, use the --noindent option.

   %(scriptName)s --silent  ... --pfile Portfolio_xml_file
      Displaying all results is the default.  Use this --silent option to reduce intermediate results output.

   %(scriptName)s --h
      Help screen.

   %(scriptName)s --cl
      Bring up the interactive command list.  "--cl" must be the first param in the %(scriptName)s runstring.

   %(scriptName)s --cl 10
      Run command #10 from the command list without bringing up interactive mode first.

   %(scriptName)s --cl 10 --debug 1
      Run command #10 from the command list without bringing up interactive mode first.  Include any extra params in the command #10 runstring, e.g., '--debug 1'.

Debugging Commands:

   %(scriptName)s --xmlfile  --pfile Portfolio_xml_file
      Show the xml string created from your xml file.  This command is similar to the --xml command.  But regular users should use --xml and not --xmlfile .  Because of the potential large amount of output, when this command is used, no other runstring commands will be performed.

   %(scriptName)s --pdt --pfile Portfolio_xml_file
      Show the Python data structure tree created from the xml string.  Calculations and totals will be updated.  Data structure fields will be nested = indented.  Because of the potential large amount of output, when this command is used, no other runstring commands will be performed.

   %(scriptName)s --debug 1|2|12  ...  --pfile Portfolio_xml_file
      Output debug statements at level 1 (highest) or level 2 (more detail) or both.  You can add more levels 0 and 3 to 9.

   %(scriptName)s --debug_linenum  ...  --pfile Portfolio_xml_file
      Show the filename and line number at the start of every screen output line.  Useful for tracking down table formatting and value problems faster.

   %(scriptName)s --trace [wc:var_name]  ...  --pfile Portfolio_xml_file
      Output a trace logfile for the test run.  The file will contain a line for each function call and return.  Lines will be nested to indicate calling relationships.  The wc:var_name option (var_name with no quotes, e.g., wc:tempvar1) allows trace to output a notification line when the value of the var_name variable changes.

TBD


"""

#=============================================================

"""
Design Notes:


- Reading XML data file into this script:

Read our investment data from an XML file into a big XML string.

Convert our big XML string into a Python nested data structure (Python_data_tree):

   dict containing:
      list of:
         dict Investment which contains:
            actual data fields
         dict Investment 2
            actual data fields
         dict Investment 3
            .
            .
            .

- Writing/modifying your XML data file:

These scripts will NEVER modify or overwrite your XML data file.  They will read, possibly modify, and output XML data file lines to stdout.  But then you are responsible for capturing this output to a file and replacing your XML data file with it (after archiving the current version of your XML data file).  Your financial data is important, and so we don't want to take the chance of a bug in these scripts corrupting your XML data file.


"""
#=============================================================

import os, sys, re

scriptName = os.path.basename(__file__).replace('.pyc', '.py')
scriptDir  = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptDir + '/lib')
sys.path.append(scriptDir + '/bin')

import getopt

from Investment import Investment
from Money import Money
from traverse_Python_data_tree import traverse_Python_data_tree

# import elementtree.ElementTree as ET
import xml.etree.ElementTree as ET

from operator import itemgetter

from pprint import pprint

from logging_wrappers import reportError, reportWarning, logging_setup, debug_run_status

from columnize_output import columnize_output

from get_stock_info import get_share_price, get_stock_asset_class

import lxml.etree as etree

import csv2html

import command_list

import logging

import trace_mi

import printoutput
from printoutput import printout, printout_format

#=============================================================

if sys.version_info[0] == 3:
    xrange = range

global processing_message 
processing_message = ''

global all_table_files
all_table_files = None


global options
options = {}

global output_file_prefix
output_file_prefix = ''

#=============================================================

class Investments():

    #==============================

    def __init__(self, data_tree={}):
        self._errors = []
        self._python_data_tree_start = "top"
        self._python_data_tree = data_tree

    #==============================

    def __str__(self, indent=False, line_break_char="\n"):
        self.xml_from_pdt(indent=False, line_break_char="\n")


    def xml_from_pdt(self, indent=False, line_break_char="\n"):
        xml_output_string = ''

        errors_old = []
        if len(self._errors) > 0:
            errors_old = self._errors
            xml_output_string += "<errors_old>\n"
            for error in self._errors:
                xml_output_string += error + '\n'
            xml_output_string += "</errors_old>\n"
            xml_output_string += "\n"
            self._errors = []

        # Output the whole pdt to a string.
        xml_output_string_temp, dont_care = traverse_Python_data_tree(command="output", indent=indent, key="top", Python_data_tree=self._python_data_tree)
        xml_output_string += xml_output_string_temp
        # print "__str__: " + xml_output_string
        # sys.exit(1)

        # Search the string looking for TBD items.
        tbd_fields = []
        # tbd_fields_expected = []
        # tbd_fields_unexpected = []
        result, dont_care = traverse_Python_data_tree(command="search", indent=indent, key="top", Python_data_tree=self._python_data_tree, search_key="Investment")
        for row in result:
            # print '89', row
            row_string = row[1].__str__()
            # print '90', row_string
            if "TBD" in row_string:
                # temp_string = row[1].get_ID() + ": TBD fields-- " + '\n'
                # temp_string = row.get_ID() + ": TBD fields-- " + '\n'
                temp_string = Investment(row[1]).get_ID() + ": TBD fields-- " + '\n'
                for field in row_string.split('\n'):
                    if 'TBD' in field:
                        temp_string += field + '\n'
                tbd_fields.append(temp_string)

                '''
                temp_row_string = row_string
                for remove in ["TBD_account_ID", 'TBD_cost_basis']:
                   temp_row_string = temp_row_string.replace(remove, '')
                if 'TBD' in temp_row_string:
                   tbd_fields_unexpected.append(row[1].get_ID() + ": TBD field-- " + temp_row_string)
                else:
                   tbd_fields_expected.append(row[1].get_ID() + ": TBD field-- " + row_string)
                '''

        if len(tbd_fields) > 0:
            xml_output_string += "<TBD_fields>\n"
            for field in tbd_fields:
                xml_output_string += "ID:" + field + '\n'
            xml_output_string += "</TBD_fields>\n"
            xml_output_string += "\n"


        '''
        for row in result:
           try:
              # print "xml_output_string = " + row.__str__(line_break_char)
              xml_output_string += row.__str__(indent=indent, line_break_char=line_break_char)
              if "TBD" in row:
                 tbd_fields_expected.append([row, row.get_ID()])
           except Exception as e:
              reportError("In Investments record:")
              print "account_ID = " + row.get_value("account_ID")
              print "name = " + row.get_value("name")
              print "owner = " + row.get_value("owner")
              print "symbol = " + row.get_value("symbol")
              print e.message, e.args
           xml_output_string += "\n"

           xml_output_string += "<TBD_fields_expected>\n"
           for field in tbd_fields_expected:
              xml_output_string += "ID:" + field + '\n'
           xml_output_string += "</TBD_fields_expected>\n"
           xml_output_string += "\n"
           if len(tbd_fields_unexpected) > 0:
              xml_output_string += "<TBD_fields_unexpected>\n"
              for field in tbd_fields_unexpected:
                 xml_output_string += "ID:" + field + '\n'
              xml_output_string += "</TBD_fields_unexpected>\n"
              xml_output_string += "\n"
        '''

        if len(self._errors) > 0:
            xml_output_string += "<errors>\n"
            for error in self._errors:
                xml_output_string += error + '\n'
            xml_output_string += "</errors>\n"
        if len(errors_old) > 0:
            xml_output_string += "<errors_old>\n"
            for error in errors_old:
                xml_output_string += error + '\n'
            xml_output_string += "</errors_old>\n"
            xml_output_string += "\n"

        return xml_output_string

    #==============================

    def get_Investments_list(self):
        result, dont_care = traverse_Python_data_tree(command="search", indent=False, key="", Python_data_tree=self._python_data_tree, search_key="Investment")
        # print self._python_data_tree
        # print '163', len(result)
        # print result
        # for loop in result:
        #    print "get_Investments_list: " + str(loop[1])

        # Make all investment-specific curr_share_prices the same.  Use the largest value.
        curr_share_prices = {}
        for row in result:
            # print Money(row[1]["curr_share_price"]).__str__()
            curr_share_price = Money(row[1]["curr_share_price"])
            symbol = row[1]["symbol"]
            if symbol not in curr_share_prices:
                curr_share_prices[symbol] = curr_share_price
            elif curr_share_price.get_cents() > curr_share_prices[symbol].get_cents():
                curr_share_prices[symbol].set_cents(curr_share_price.get_cents())

        result_list = []
        for index in xrange(len(result)):
            if result[index][0] == 'Investments:Investment':
                # print "name_entry: " + result[index][1].__class__.__name__
                symbol = result[index][1]['symbol']
                # print "182", symbol, result[index][1]['curr_share_price'], curr_share_prices[symbol]
                # print "186", symbol, result[index][1]['curr_share_price']
                # print "193", symbol, curr_share_prices[symbol]
                # print "186", symbol, type(result[index][1]['curr_share_price'])
                # print "193", symbol, type(curr_share_prices[symbol])
                result[index][1]['curr_share_price'] = curr_share_prices[symbol].__str__()
                result_list.append(Investment(result[index][1]))

        # print '185', len(result_list)
        # for row in result_list:
        #    print row.__str__()

        return result_list


    #==============================

    def show_stats(self, label=''):
        printout("<Stats>")
        printout()
        if label != '':
            printout("<label>" + label + "</label>")

        errors_old = []
        if len(self._errors) > 0:
            errors_old = self._errors
            printout("<errors_old>")
            for error in errors_old:
                printout(error)
            printout("</errors_old>")
            printout()

        # self._errors = []
        retirement_class_totals = {}

        result = self.get_Investments_list()

        '''
        print len(result)
        for row in result:
           print str(row)
        sys.exit(1)
        print result
        '''

        total_amount_temp = Money()
        asset_class_temp = {}
        # asset_class_temp["Large Growth"] = Money()
        for row in result:
            # print type(row)
            # print "row: " + str(row)
            # row = row[1]
            # asset_class_money_instance = Money().set_by_string(row["curr_total_value"])
            asset_class_money_instance = Money().set_by_string(row.get_value("curr_total_value"))
            # asset_class_money_instance = Money()
            # asset_class_money_instance.set_by_string(row.get_value("curr_total_value"))

            # total_amount_temp.add(money_instance)
            # print row.get_value('asset_class'), total_amount_temp.__str__()
            # print "debug: 155: " + row.get_value('asset_class') + "," + money_instance.__str__()


            ac = row.get_value('asset_class')
            # print "debug: ac: " + ac
            if ac not in asset_class_temp:
                # print ac + " created"
                # if "Large Growth" in asset_class_temp:
                #    print "debug: 160 Large Growth: " + asset_class_temp["Large Growth"].__str__()

                asset_class_temp[ac] = asset_class_money_instance
                # asset_class_temp[ac] = Money()
                # print "debug: 168 after create: " + ac + ", " + ", " + asset_class_temp[ac].__str__()
                # money_instance = asset_class_temp[ac]  # debug
                # print id(money_instance)
                # print row.get_value("curr_total_value")
                # asset_class_temp[ac].set_by_string(row.get_value("curr_total_value"))
                # print "debug: 170 Large Growth: " + asset_class_temp["Large Growth"].__str__()
            else:
                # print "debug: before add: " + ac + ", " + asset_class_money_instance.__str__() + ", " + asset_class_temp[ac].__str__()
                # print "debug: 171 Large Growth: " + asset_class_temp["Large Growth"].__str__()
                asset_class_temp[ac].add(asset_class_money_instance)
                # print "debug: 173 Large Growth: " + asset_class_temp["Large Growth"].__str__()

            # print "debug: 176 after add: " + ac + ", " + asset_class_money_instance.__str__() + ", " + asset_class_temp[ac].__str__()
            # print "debug: 181 Large Growth: " + asset_class_temp["Large Growth"].__str__()

            if len(asset_class_money_instance._errors) > 0:
                msg = "In show_stats: " + row.get_value("filename") + ", line " + row.get_value("file_line_num") + ": " + row.get_ID()
                reportError(msg)
                self._errors.append(msg)
                for msg in asset_class_money_instance._errors:
                    printout(msg)
                    self._errors.append(msg)
            else:
                retirement_class_money_instance = Money().set_by_string(row.get_value("curr_total_value"))
                if row.get_value("retirement_class") not in retirement_class_totals:
                    # if "Large Growth" in asset_class_temp:
                    #    print "debug: 210 Large Growth: " + asset_class_temp["Large Growth"].__str__()
                    retirement_class_totals[row.get_value("retirement_class")] = [1, retirement_class_money_instance]
                else:
                    # if "Large Growth" in asset_class_temp:
                    #    print "debug: 212 Large Growth: " + asset_class_temp["Large Growth"].__str__()
                    # print row.get_ID()
                    # print row.__str__()
                    # print "rc: 216: " + row.get_value("retirement_class")
                    retirement_class_totals[row.get_value("retirement_class")][0] += 1
                    # if "Large Growth" in asset_class_temp:
                    #    print "debug: 216a Large Growth: " + asset_class_temp["Large Growth"].__str__()
                    retirement_class_totals[row.get_value("retirement_class")][1].add(retirement_class_money_instance)

                # if "Large Growth" in asset_class_temp:
                #    print "debug: 217 Large Growth: " + asset_class_temp["Large Growth"].__str__()

        # for key, value in sorted(asset_class_temp.items(), key=itemgetter(0)):
        #    print key, value

        retirement_total = Money()
        non_retirement_total = Money()
        total_amount = Money()
        for key, value in dict.items(retirement_class_totals):
            total_amount.add(value[1])
            if key == "Non_Retirement":
                non_retirement_total.add(value[1])
            else:
                retirement_total.add(value[1])

        printout("<general>")
        printout("Total number investments = " + str(len(result)))
        printout('Total amount = "' + total_amount.__str__(pretty_print=True) + '", ' + str(total_amount.percent(total_amount)) + "%")

        printout("</general>")
        printout()
        printout("<retirement_classes>")

        retirement_classes_total_assets = 0
        for key, value in dict.items(retirement_class_totals):
            printout(key + ", " + str(value[0]) + ", " + '"' + value[1].__str__(pretty_print=True) + '", ' + str(value[1].percent(total_amount)) + "%")
            retirement_classes_total_assets += value[0]

        printout()
        printout("Total number retirement_classes assets = " + str(retirement_classes_total_assets))
        printout("Total number retirement_classes = " + str(len(retirement_class_totals)))
        printout()
        printout('Total amount non-retirement = "' + non_retirement_total.__str__(pretty_print=True) + '", ' + str(non_retirement_total.percent(total_amount)) + "%")
        printout('Total amount retirement = "' + retirement_total.__str__(pretty_print=True) + '", ' + str(retirement_total.percent(total_amount)) + "%")
        total_amount_temp = Money()
        total_amount_temp.add(non_retirement_total)
        total_amount_temp.add(retirement_total)

        total_percent_temp = non_retirement_total.percent(total_amount) + retirement_total.percent(total_amount)
        printout('Total amount = "' + total_amount_temp.__str__(pretty_print=True) + '", ' + str(total_percent_temp) + "%")
        printout()
        printout("</retirement_classes>")
        printout()

        self.show_ac_stats()

        printout("</Stats>")
        printout()

        if len(self._errors) > 0:
            printout()
            printout("<errors>")
            for error in self._errors: printout(error)
            printout("</errors>")
        if len(errors_old) > 0:
            printout("<errors_old>")
            for error in errors_old:
                printout(error)
            printout("</errors_old>")
            printout()

        return

    #==============================

    def show_ac_stats(self):
        totals_table = {}  # can have multiple entries for each asset class, e.g., retirement, non-retirement
        self._errors = []
        asset_class_totals = {}
        retirement_asset_class_totals = {}
        temp_debug = Money()
        result = self.get_Investments_list()
        for row in result:
            asset_class_money_instance = Money().set_by_string(row.get_value("curr_total_value"))
            asset_class_name = row.get_value("asset_class")
            if asset_class_name not in asset_class_totals:
                asset_class_totals[asset_class_name] = [1, asset_class_money_instance]
            else:
                # print row.get_ID()
                # print row.__str__()
                asset_class_totals[asset_class_name][0] += 1
                asset_class_totals[asset_class_name][1].add(asset_class_money_instance)

            '''
            temp_debug.add(asset_class_totals[asset_class_name][1])
            print asset_class_name, temp_debug.__str__()
            print asset_class_name + "," + str(asset_class_totals[asset_class_name][1])
            print "--------"
            for key, value in dict.items(asset_class_totals):
               print key, value[1].__str__()
            '''

            retirement_class_name = row.get_value("retirement_class")
            if retirement_class_name != 'Non_Retirement':
                retirement_class_name = 'Retirement'
            retirement_asset_class_name = asset_class_name + ':' + retirement_class_name
            retirement_class_money_instance = Money().set_by_string(row.get_value("curr_total_value"))
            if retirement_asset_class_name not in retirement_asset_class_totals:
                retirement_asset_class_totals[retirement_asset_class_name] = [1, retirement_class_money_instance]
            else:
                # print row.get_ID()
                # print row.__str__()
                retirement_asset_class_totals[retirement_asset_class_name][0] += 1
                retirement_asset_class_totals[retirement_asset_class_name][1].add(retirement_class_money_instance)

            if asset_class_name not in totals_table:
                totals_table[asset_class_name] = {}

            if 'Total' not in totals_table[asset_class_name]:
                totals_table[asset_class_name]['Total'] = ''
            '''
            print asset_class_name
            print asset_class_totals[asset_class_name]
            print asset_class_totals[asset_class_name][1]
            '''
            totals_table[asset_class_name]['Total'] = asset_class_totals[asset_class_name][1]

            if retirement_class_name == 'Retirement':
                if 'Retirement' not in totals_table[asset_class_name]:
                    totals_table[asset_class_name][retirement_class_name] = []
                totals_table[asset_class_name][retirement_class_name] = retirement_asset_class_totals[retirement_asset_class_name][1]

            if retirement_class_name == 'Non_Retirement':
                if 'Non_Retirement' not in totals_table[asset_class_name]:
                    totals_table[asset_class_name][retirement_class_name] = []

                '''
                print asset_class_name
                print str(totals_table[asset_class_name])
                print totals_table[asset_class_name][retirement_class_name]
                # print totals_table[asset_class_name][retirement_class_name] = retirement_asset_class_totals[retirement_class_name]
                '''
                totals_table[asset_class_name][retirement_class_name] = retirement_asset_class_totals[retirement_asset_class_name][1]

            '''
            if 'Non_Retirement' not in totals_table[asset_class_name]:
               if retirement_class_name == 'Non_Retirement':
                  totals_table[asset_class_name]['Non_Retirement'] = retirement_asset_class_totals[retirement_class_name]

               # totals_table[asset_class_name] = {'asset_class':asset_class_totals[asset_class_name], 'retirement_asset_class':retirement_asset_class_totals[retirement_asset_class_name],
            '''


        printout("<asset_classes>")
        total_amount = Money()
        for key, value in dict.items(asset_class_totals):
            # print key + "," + value[1].__str__()
            total_amount.add(value[1])

        asset_class_total_investments = 0
        total_percent = 0.0
        for key_value_pair in sorted(list(asset_class_totals.items()), key=itemgetter(0)):
            key = key_value_pair[0]
            value = key_value_pair[1]
            printout(str(key) + ", " + str(value[0]) + ", " + '"' + value[1].__str__(pretty_print=True) + '", ' + str(value[1].percent(total_amount)) + "%")
            asset_class_total_investments += value[0]
            total_percent += float(value[1].percent(total_amount))

        printout("Total percent = " + str(total_percent) + "%")
        printout("Total number asset_classes investments = " + str(asset_class_total_investments))
        printout("Total number asset_classes = " + str(len(asset_class_totals)))
        printout('Total amount = ' + total_amount.__str__(pretty_print=True))
        printout()
        printout("</asset_classes>")
        printout()

        printout("<retirement_asset_classes>")
        retirement_total_amount = Money()
        for key, value in dict.items(retirement_asset_class_totals):
            retirement_total_amount.add(value[1])

        retirement_asset_classes_missing = 0
        retirement_asset_class_total_investments = 0
        retirement_total_percent = 0
        expect_2_entries = ''
        for key_value_pair in sorted(list(retirement_asset_class_totals.items()), key=itemgetter(0)):
            key = key_value_pair[0]
            value = key_value_pair[1]

            if expect_2_entries == '':
                expect_2_entries = key.split(':')[0]
            else:
                asset_class_name = key.split(':')[0]
                if asset_class_name != expect_2_entries:
                    if key.split(':')[1] == 'Non_Retirement':
                        missing = 'Retirement'
                    else:
                        missing = 'Non_Retirement'
                    reportWarning("   " + expect_2_entries + ": WARNING: Missing " + missing + " class")
                    expect_2_entries = asset_class_name
                    retirement_asset_classes_missing += 1
                else:
                    expect_2_entries = ''

            printout(str(key) + ", " + str(value[0]) + ", " + '"' + value[1].__str__(pretty_print=True) + '", ' + str(value[1].percent(total_amount)) + "%")
            retirement_asset_class_total_investments += value[0]
            retirement_total_percent += float(value[1].percent(retirement_total_amount))
        printout("Total percent retirement = " + str(retirement_total_percent) + "%")
        printout("Total amount all retirement classes = " + retirement_total_amount.__str__(pretty_print=True))
        printout("Total number retirement_asset_classes investments = " + str(retirement_asset_class_total_investments))
        printout("Total number existing retirement_asset_classes = " + str(len(retirement_asset_class_totals)))
        printout("Total number missing retirement_asset_classes = " + str(retirement_asset_classes_missing))
        printout("</retirement_asset_classes>")
        printout()

        printout("<totals_percents_table>")
        # Consolidate totals_table one total per line into reorganized_totals_table one line containing all totals for an asset class.

        output_list = self.show_ac_percents_table()
        for row in output_list:
            printout(row)

        printout("</totals_percents_table>")


    #==============================

    def get_ac_amounts_from_inv_list(self):
        self._errors = []
        asset_class_totals = {}

        result = self.get_Investments_list()
        for row in result:
            status = row.get_value("status")
            if status != 'active':
                continue
            asset_class_name = row.get_value("asset_class")
            if asset_class_name not in asset_class_totals:
                asset_class_totals[asset_class_name] = {}
                asset_class_totals[asset_class_name]['Total'] = {'count':0, 'amount':Money(), 'orig_amount':Money(), 'new_candidate_amount':Money(), 'added_amount':Money()}
                asset_class_totals[asset_class_name]['Retirement'] = {'count':0, 'amount':Money(), 'orig_amount':Money(), 'new_candidate_amount':Money(), 'added_amount':Money()}
                asset_class_totals[asset_class_name]['Non_Retirement'] = {'count':0, 'amount':Money(), 'orig_amount':Money(), 'new_candidate_amount':Money(), 'added_amount':Money()}
            # print row.get_ID()
            # print row.__str__()
            retirement_class_name = row.get_value("retirement_class")
            asset_class_amount = Money().set_by_string(row.get_value("curr_total_value"))
            if retirement_class_name == 'Non_Retirement':
                asset_class_totals[asset_class_name]['Non_Retirement']['amount'].add(asset_class_amount)
                asset_class_totals[asset_class_name]['Non_Retirement']['orig_amount'].add(asset_class_amount)
                asset_class_totals[asset_class_name]['Non_Retirement']['new_candidate_amount'].add(asset_class_amount)
                asset_class_totals[asset_class_name]['Non_Retirement']['added_amount'].set_cents(0)
                asset_class_totals[asset_class_name]['Non_Retirement']['count'] += 1
            else:
                asset_class_totals[asset_class_name]['Retirement']['amount'].add(asset_class_amount)
                asset_class_totals[asset_class_name]['Retirement']['orig_amount'].add(asset_class_amount)
                asset_class_totals[asset_class_name]['Retirement']['new_candidate_amount'].add(asset_class_amount)
                asset_class_totals[asset_class_name]['Retirement']['added_amount'].set_cents(0)
                asset_class_totals[asset_class_name]['Retirement']['count'] += 1

            asset_class_totals[asset_class_name]['Total']['amount'].add(asset_class_amount)
            asset_class_totals[asset_class_name]['Total']['orig_amount'].add(asset_class_amount)
            asset_class_totals[asset_class_name]['Total']['new_candidate_amount'].add(asset_class_amount)
            asset_class_totals[asset_class_name]['Total']['added_amount'].set_cents(0)
            asset_class_totals[asset_class_name]['Total']['count'] += 1

        ac_totals_sorted_list = sorted(list(asset_class_totals.items()), key=itemgetter(0))

        return 0, ac_totals_sorted_list


    #==============================

    def show_ac_lp_diff_table(self, ac_percents_table_body_no_add, ac_percents_table_body_with_add):
        global processing_message

        totals = ['Totals', 0.0, '', 0.0, '', 0.0, '', 0.0, '', 0.0, '', 0.0]
        totals_index_start = 0
        percents_tables_side_by_side = []
        for _ in ac_percents_table_body_no_add:
            percents_tables_side_by_side.append([])
        column = 0
        for sort_by in ['Total_percent', 'Retirement_percent', 'Non_Retirement_percent']:

            show_at_bottom_of_table = []
            for which_list in [ac_percents_table_body_no_add, ac_percents_table_body_with_add]:
                percents_tbl = []
                for row in which_list:
                    # if 'Bonds' in row[0] or 'Individual_Stocks' in row[0]:
                    #     continue
                    Total_percent = float(row[3].split('<')[0])
                    Retirement_percent = float(row[6].split('<')[0])
                    Non_Retirement_percent = float(row[9].split('<')[0])
                    if 'Bonds' in row[0] or 'Individual_Stocks' in row[0]:
                        show_at_bottom_of_table.append({'Asset_class': row[0], 'Total_percent': Total_percent, 'Retirement_percent': Retirement_percent, 'Non_Retirement_percent': Non_Retirement_percent})
                    else:
                        percents_tbl.append({'Asset_class': row[0], 'Total_percent': Total_percent, 'Retirement_percent': Retirement_percent, 'Non_Retirement_percent': Non_Retirement_percent})

                percents_retirement_class_sorted = sorted(percents_tbl, key=itemgetter(sort_by))
                percents_retirement_class_sorted += show_at_bottom_of_table

                # print 705, sort_by

                if len(percents_tables_side_by_side[0]) > 0:
                    for index in xrange(len(percents_tables_side_by_side)):
                        for index2 in xrange(len(percents_retirement_class_sorted)):
                            # print 707, percents_tables_side_by_side[index]
                            # print 708, percents_tables_side_by_side[index][0]
                            # print 709, percents_retirement_class_sorted[index2]
                            # print 710, percents_retirement_class_sorted[index2]['Asset_class']
                            if len(percents_tables_side_by_side[index]) > 0 and percents_tables_side_by_side[index][column] in percents_retirement_class_sorted[index2]['Asset_class'] and '*' in percents_retirement_class_sorted[index2]['Asset_class']:
                                # print 707, percents_tables_side_by_side[index]
                                # print 708, percents_tables_side_by_side[index][column]
                                # print 709, percents_retirement_class_sorted[index2]
                                # print 710, percents_retirement_class_sorted[index2]['Asset_class']
                                percents_tables_side_by_side[index][column] = percents_retirement_class_sorted[index2]['Asset_class']
                                break
                    column += 2

                for index in xrange(len(percents_tables_side_by_side)):
                        # percents_tables_side_by_side[index] += map(lambda row: [row['Asset_class'], "%1.2f" % row['Total_percent'], "%1.2f" % row['Retirement_percent'], "%1.2f" % row['Non_Retirement_percent']], [percents_retirement_class_sorted[index]])[0]
                    percents_tables_side_by_side[index] += [percents_retirement_class_sorted[index]['Asset_class'], "%1.2f" % percents_retirement_class_sorted[index][sort_by]]

                    totals_index = totals_index_start
                    # totals[totals_index] = 'Totals'
                    totals_index += 1
                    totals[totals_index] += percents_retirement_class_sorted[index][sort_by]
                    totals_index += 1

                totals_index_start = totals_index

        percents_tables_side_by_side.insert(0, ['', 'Before', '', 'After', '', 'Before', '', 'After', '', 'Before', '', 'After'])
        percents_tables_side_by_side.insert(1, ['Asset', 'Tot_%', 'Asset', 'Tot_%', 'Asset', 'Ret_%', 'Asset', 'Ret_%', 'Asset', 'Non_%', 'Asset', 'Non_%'])

        percents_tables_side_by_side.append(["%1.2f" % cell if 'float' in str(type(cell)) else cell for cell in totals])  # skip strings in totals

        filename = output_file_prefix + 'lp_diff_table'
        rc, percents_sorted_columnized = columnize_output(input_data=percents_tables_side_by_side, justify_cols='L,R,  ,L,R,  ,L,R,  ,L,R,  ,L,R,  ,L,R,', save_filename=filename)
        if rc != 0:
            reportWarning("Non-zero status from columnize_output()")

        msg = "What to invest in next = has the lowest percents = at the top of the list--\n"
        msg = msg + "-" * len(msg) + '\nList includes Bonds and Individual_Stocks but they are pushed down to the bottom of the lists.\n'
        text_to_insert = processing_message + '\n' + msg + "-" * len(percents_sorted_columnized[0])
        fd_output = open(filename + ".txt.new", "w")
        fd_output.write(text_to_insert + '\n')
        for line in open(filename + ".txt", "r").read().splitlines():
            fd_output.write(line + '\n')
        fd_output.close()
        os.rename(filename + ".txt.new", filename + ".txt")

        if silent_option == False:
            if len(percents_sorted_columnized) > 0:
                printout(text_to_insert)
                for row in percents_sorted_columnized: printout(row)

        rc, html_table_string = csv2html.csv2html(list_of_objects=percents_sorted_columnized, num_header_lines_from_top=2)
        html_table_string = '<br>' + processing_message + '\n' + html_table_string
        with open(filename + ".html", 'w') as fd:
            fd.write(html_table_string)
        if all_table_files is not None:
            all_table_files.append(filename)
        processing_message = ''

        # return 0, lowest_percents_rows2, percents_avg_columnized, percents_sorted_columnized
        return 0, percents_sorted_columnized

    #==============================

    def show_ac_lp_table(self, ac_percents_table_body='', pt_cmd_lp=''):
        global options
        global processing_message

        '''
        # METHOD 1: Search Retirement list for lowest percents then search that list for the lowest in Non_Retirement.

        if looking_for_lp == 'Retirement':
           percent_index = 4
        else:
           percent_index = 6
        lowest_percents_rows = []
        lowest_percents_row = []
        for row in ac_percents_table_body:
           if 'Bonds' in row[0] or 'Individual_Stocks' in row[0]:
              continue
           candidate_percent = float(row[percent_index].split('<')[0])
           if len(lowest_percents_row) == 0:
              lowest_percents_row = row
           elif candidate_percent <= float(lowest_percents_row[percent_index].split('<')[0]):
              lowest_percents_row = row
              lowest_percents_rows.append(row)
        if len(lowest_percents_row) == 0:
           lowest_percents_rows.append(lowest_percents_rows)

        if looking_for_lp == 'Retirement':
           percent_index = 6
        else:
           percent_index = 4
        lowest_percents_rows2 = []
        lowest_percents_row2 = []
        for row in lowest_percents_rows:
           if 'Bonds' in row[0] or 'Individual_Stocks' in row[0]:
              continue
           candidate_percent = float(row[percent_index].split('<')[0])
           if len(lowest_percents_row2) == 0:
              lowest_percents_row2 = row
           elif candidate_percent <= float(lowest_percents_row2[percent_index].split('<')[0]):
              lowest_percents_row2 = row
              lowest_percents_rows2.append(row)
        if len(lowest_percents_rows2) == 0:
           lowest_percents_rows2.append(lowest_percents_row2)

        # print "Lowest percents:"
        # for row in lowest_percents_rows2:
        #    print row


        # METHOD 2:

        percents_avg = [['Asset', 'Avg(Ret vs Non)', 'Tot', 'Ret', 'Non']]
        for row in ac_percents_table_body:
           if 'Bonds' in row[0] or 'Individual_Stocks' in row[0]:
              continue
           Total_percent = float(row[2].split('<')[0])
           Retirement_percent = float(row[4].split('<')[0])
           Non_Retirement_percent = float(row[6].split('<')[0])
           avg = (Retirement_percent + Non_Retirement_percent) / 2
           # print("%s,%1.2f,%1.2f,%1.2f" % (row[0], avg, Retirement_percent, Non_Retirement_percent))
           percents_avg.append([row[0], "%1.2f" % avg, "%1.2f" % Total_percent, "%1.2f" % Retirement_percent, "%1.2f" % Non_Retirement_percent])
        rc, percents_avg_columnized = columnize_output(input_data=percents_avg)

        # for row in columnizeercents_avg):
        #    print row
        '''

        # METHOD 3: Sorts

        # print 747, looking_for_lp

        show_at_bottom_of_table = []
        percents_tbl = []
        for row in ac_percents_table_body:
            # if 'Bonds' in row[0] or 'Individual_Stocks' in row[0]:
            #     continue
            Total_percent = float(row[3].split('<')[0])
            Retirement_percent = float(row[6].split('<')[0])
            Non_Retirement_percent = float(row[9].split('<')[0])
            if 'Bonds' in row[0] or 'Individual_Stocks' in row[0]:
                show_at_bottom_of_table.append({'Asset_class': row[0], 'Total_percent': Total_percent, 'Retirement_percent': Retirement_percent, 'Non_Retirement_percent': Non_Retirement_percent})
            else:
                percents_tbl.append({'Asset_class': row[0], 'Total_percent': Total_percent, 'Retirement_percent': Retirement_percent, 'Non_Retirement_percent': Non_Retirement_percent})

        totals = ['Totals', 0.0, 0.0, 0.0, 'Totals', 0.0, 0.0, 0.0, 'Totals', 0.0, 0.0, 0.0]
        totals_index_start = 0
        percents_tables_side_by_side = []
        for sort_by in ['Total_percent', 'Retirement_percent', 'Non_Retirement_percent']:
            percents_retirement_class_sorted = sorted(percents_tbl, key=itemgetter(sort_by))
            percents_retirement_class_sorted += show_at_bottom_of_table
            if len(percents_tables_side_by_side) == 0:
                # This is the first table.
                # percents_tables_side_by_side = [[row['Asset_class'], "%1.2f" % row['Total_percent'], "%1.2f" % row['Retirement_percent'], "%1.2f" % row['Non_Retirement_percent']] for row in percents_retirement_class_sorted]
                for row in percents_retirement_class_sorted:
                        # percents_tables_side_by_side = [row['Asset_class'], "%1.2f" % row['Total_percent'], "%1.2f" % row['Retirement_percent'], "%1.2f" % row['Non_Retirement_percent']]
                    percents_tables_side_by_side.append([row['Asset_class'], "%1.2f" % row['Total_percent'], "%1.2f" % row['Retirement_percent'], "%1.2f" % row['Non_Retirement_percent']])

                    totals_index = 0
                    # totals[totals_index] = 'Totals'
                    totals_index += 1
                    totals[totals_index] += row['Total_percent']
                    totals_index += 1
                    totals[totals_index] += row['Retirement_percent']
                    totals_index += 1
                    totals[totals_index] += row['Non_Retirement_percent']

                totals_index_start = totals_index

            else:
                # Concatenate the rows of the next table to the right of the existing table of tables we are building.
                for index in xrange(len(percents_tables_side_by_side)):
                    # percents_tables_side_by_side[index] += map(lambda row: [row['Asset_class'], "%1.2f" % row['Total_percent'], "%1.2f" % row['Retirement_percent'], "%1.2f" % row['Non_Retirement_percent']], [percents_retirement_class_sorted[index]])[0]
                    percents_tables_side_by_side[index] += list(map(lambda row: [row['Asset_class'], "%1.2f" % row['Total_percent'], "%1.2f" % row['Retirement_percent'], "%1.2f" % row['Non_Retirement_percent']], [percents_retirement_class_sorted[index]]))[0]

                    totals_index = totals_index_start
                    totals_index += 1
                    # totals[totals_index] = 'Totals'
                    totals_index += 1
                    totals[totals_index] += float(percents_tables_side_by_side[index][totals_index])
                    totals_index += 1
                    totals[totals_index] += float(percents_tables_side_by_side[index][totals_index])
                    totals_index += 1
                    totals[totals_index] += float(percents_tables_side_by_side[index][totals_index])

                totals_index_start = totals_index

        percents_tables_side_by_side.insert(0, ['Asset', 'Tot_%', 'Ret_%', 'Non_%', 'Asset', 'Tot_%', 'Ret_%', 'Non_%', 'Asset', 'Tot_%', 'Ret_%', 'Non_%'])
        percents_tables_side_by_side.insert(0, ['', 'Sorted', '', '', '', '', 'Sorted', '', '', '', '', 'Sorted'])

        percents_tables_side_by_side.append(["%1.2f" % cell if 'float' in str(type(cell)) else cell for cell in totals])  # skip strings in totals

        filename = output_file_prefix + 'lp_table'
        rc, percents_sorted_columnized = columnize_output(input_data=percents_tables_side_by_side, justify_cols='L,R,R,R,   ,L,R,R,R,   ,L,R,R,R', save_filename=filename)
        if rc != 0:
            reportWarning("Non-zero status from columnize_output()")

        msg = "What to invest in next = has the lowest percents = at the top of the list--\n"
        msg = msg + "-" * len(msg) + '\nList includes Bonds and Individual_Stocks but they are pushed down to the bottom of the lists.\n'
        text_to_insert = processing_message + '\n' + msg + "-" * len(percents_sorted_columnized[0])
        fd_output = open(filename + ".txt.new", "w")
        fd_output.write(text_to_insert + '\n')
        for line in open(filename + ".txt", "r").read().splitlines():
            fd_output.write(line + '\n')
        fd_output.close()
        os.rename(filename + ".txt.new", filename + ".txt")

        if silent_option == False:
            if len(percents_sorted_columnized) > 0:
                printout(text_to_insert)
                for row in percents_sorted_columnized: printout(row)

        rc, html_table_string = csv2html.csv2html(list_of_objects=percents_sorted_columnized, num_header_lines_from_top=2)
        html_table_string = '<br>' + processing_message + '\n' + html_table_string
        with open(filename + ".html", 'w') as fd:
            fd.write(html_table_string)
        if all_table_files is not None:
            all_table_files.append(filename)
        processing_message = ''

        # return 0, lowest_percents_rows2, percents_avg_columnized, percents_sorted_columnized
        # return 0, percents_sorted_columnized
        return 0, ac_percents_table_body

    #==============================

    def show_ac_percents_table(self, pt_cmd_add='', ac_totals_sorted_list=None, pt_cmd_lp='', pt_cmd_show=''):
        global options
        global processing_message

        if '1' in get_option('--debug', ''): printout("Entering show_ac_percents_table")

        if ac_totals_sorted_list is None:
            ac_totals_sorted_list = []

        # print "678", options

        # print(984, len(ac_totals_sorted_list))

        if len(ac_totals_sorted_list) == 0:
            rc, ac_totals_sorted_list = self.get_ac_amounts_from_inv_list()
            # print(988, "Created ac_totals_sorted_list = ", ac_totals_sorted_list)

        # print(989, ac_totals_sorted_list)

        # percent_symbol = '%'
        percent_symbol = ''

        ac_percents_table = []

        header_row = [ \
           '', \
           'Tot', \
           'Tot', \
           'Tot', \
           'Ret', \
           'Ret', \
           'Ret', \
           'Non_Ret', \
           'Non_Ret', \
           'Non_Ret' \
          ]
        ac_percents_table.append(header_row)

        header_row = [ \
           'Asset_Class', \
           'inv_count', \
           'amt', \
           'pct', \
           'inv_count', \
           'amt', \
           'pct', \
           'inv_count', \
           'amt', \
           'pct' \
          ]
        ac_percents_table.append(header_row)

        ac_percents_table_body = []

        ac_percents_table_totals = { \
           'Total': { \
               'count': 0, \
               'amount': Money(), \
               'percent': 0.00, \
               'orig_amount': Money(), \
               'orig_percent_total': 0.00, \
               'new_candidate_amount': Money(), \
               }, \
           'Retirement': { \
               'count': 0, \
               'amount': Money(), \
               'percent': 0.00, \
               'orig_amount': Money(), \
               'orig_percent_total': 0.00, \
               'new_candidate_amount': Money(), \
               }, \
           'Non_Retirement': { \
               'count': 0, \
               'amount': Money(), \
               'percent': 0.00, \
               'orig_amount': Money(), \
               'orig_percent_total': 0.00, \
               'new_candidate_amount': Money(), \
               }, \
            }

        # Get final totals to create row percentages.

        # print(1051, ac_totals_sorted_list)
        # for row in ac_totals_sorted_list: printout(1052, row)
        for row in ac_totals_sorted_list:
            for ret_type in ['Total', 'Retirement', 'Non_Retirement']:
                # print(1053, ac_totals_sorted_list)
                # print(1054, row)
                ac_percents_table_totals[ret_type]['count'] += row[1][ret_type]['count']
                if pt_cmd_add != '':
                    ac_percents_table_totals[ret_type]['orig_amount'].add(row[1][ret_type]['orig_amount'])
                    # print "746", row[0], ret_type, ac_percents_table_totals[ret_type]['orig_amount'].__str__(), row[1][ret_type]['new_candidate_amount'].__str__(), row[1][ret_type]['orig_amount'].__str__()
                    ac_percents_table_totals[ret_type]['new_candidate_amount'].add(row[1][ret_type]['new_candidate_amount']).add(row[1][ret_type]['added_amount'], keep=False)
                else:
                    ac_percents_table_totals[ret_type]['orig_amount'].add(row[1][ret_type]['amount'])
                    ac_percents_table_totals[ret_type]['new_candidate_amount'].add(row[1][ret_type]['amount'])

        # print 925, ac_percents_table_totals['Total']['new_candidate_amount']
        # print 925, ac_percents_table_totals['Retirement']['new_candidate_amount']
        # print 925, ac_percents_table_totals['Non_Retirement']['new_candidate_amount']

        # print ac_percents_table_totals['Total']['amount'].__str__()
        # print ac_percents_table_totals['Retirement']['amount'].__str__()
        # print ac_percents_table_totals['Non_Retirement']['amount'].__str__()

        # print "749", ac_percents_table_totals['Retirement']['orig_amount'].__str__()

        # Then do real row-by-row.

        string_params = { \
           'Total': { \
              'string_amount': '', \
              'string_percent': '', \
              'new_candidate_amount': '', \
              'new_candidate_percent': '', \
              'orig_percent': '', \
              }, \
           'Retirement': { \
              'string_amount': '', \
              'string_percent': '', \
              'new_candidate_amount': '', \
              'new_candidate_percent': '', \
              'orig_percent': '', \
              }, \
           'Non_Retirement': { \
              'string_amount': '', \
              'string_percent': '', \
              'new_candidate_amount': '', \
              'new_candidate_percent': '', \
              'orig_percent': '', \
              }, \
           }

        if pt_cmd_add != '':

            for row in ac_totals_sorted_list:
                if row[1].get('added_to', False) == True:
                    add_to_marker = ' *'
                else:
                    add_to_marker = ''

                for ret_type in ['Total', 'Retirement', 'Non_Retirement']:
                    # print 965, ret_type
                    if row[1][ret_type]['added_amount'].get_cents() != 0:
                        ac_percents_table_totals[ret_type]['amount'].add(row[1][ret_type]['added_amount'].add(row[1][ret_type]['orig_amount'], keep=False))
                        ac_percents_table_totals[ret_type]['percent'] += row[1][ret_type]['new_candidate_amount'].percent(ac_percents_table_totals[ret_type]['new_candidate_amount'])
                        # print 968, row[1][ret_type]['new_candidate_amount'].percent(ac_percents_table_totals[ret_type]['new_candidate_amount'])
                        # print 969, ac_percents_table_totals[ret_type]['percent']

                        string_params[ret_type]['string_amount'] = row[1][ret_type]['added_amount'].__str__() + "+" + row[1][ret_type]['orig_amount'].__str__()
                        string_params[ret_type]['orig_percent'] = "%1.2f" % row[1][ret_type]['orig_amount'].percent(ac_percents_table_totals[ret_type]['orig_amount'])
                        # string_params[ret_type]['string_percent'] = "%1.2f" % row[1][ret_type]['new_candidate_amount'].percent(ac_percents_table_totals[ret_type]['orig_amount'].add(row[1][ret_type]['added_amount'], keep=False)) + '<' + string_params[ret_type]['orig_percent']
                        string_params[ret_type]['string_percent'] = "%1.2f" % row[1][ret_type]['new_candidate_amount'].percent(ac_percents_table_totals[ret_type]['new_candidate_amount']) + '<' + string_params[ret_type]['orig_percent']
                        # print 973, string_params[ret_type]['string_percent']
                    else:
                        # ac_percents_table_totals[ret_type]['percent'] += row[1][ret_type]['orig_amount'].percent(ac_percents_table_totals[ret_type]['orig_amount'])
                        ac_percents_table_totals[ret_type]['amount'].add(row[1][ret_type]['orig_amount'])
                        ac_percents_table_totals[ret_type]['percent'] += row[1][ret_type]['orig_amount'].percent(ac_percents_table_totals[ret_type]['new_candidate_amount'])
                        # print 980, row[1][ret_type]['orig_amount'].percent(ac_percents_table_totals[ret_type]['new_candidate_amount'])
                        # print 981, ac_percents_table_totals[ret_type]['percent']

                        # string_params[ret_type]['string_amount'] = row[1][ret_type]['orig_amount']
                        # string_params[ret_type]['string_percent'] = "%1.2f" % row[1][ret_type]['orig_amount'].percent(ac_percents_table_totals[ret_type]['orig_amount'])
                        string_params[ret_type]['string_amount'] = row[1][ret_type]['new_candidate_amount']
                        string_params[ret_type]['string_percent'] = "%1.2f" % row[1][ret_type]['orig_amount'].percent(ac_percents_table_totals[ret_type]['new_candidate_amount'])
                        # print 984, string_params[ret_type]['string_percent']

                new_row = [row[0] + add_to_marker]
                for ret_type in ['Total', 'Retirement', 'Non_Retirement']:
                    new_row.append(row[1][ret_type]['count'])
                    new_row.append(string_params[ret_type]['string_amount'])
                    new_row.append(string_params[ret_type]['string_percent'])
                ac_percents_table_body.append(new_row)

        else:  # for all views after 'add', must continue to show add-adjusted values

            for row in ac_totals_sorted_list:
                if row[1].get('added_to', False) == True:
                    add_to_marker = ' *'
                else:
                    add_to_marker = ''

                for ret_type in ['Total', 'Retirement', 'Non_Retirement']:
                    ac_percents_table_totals[ret_type]['amount'].add(row[1][ret_type]['amount'])
                    # ac_percents_table_totals[ret_type]['percent'] += row[1][ret_type]['amount'].percent(ac_percents_table_totals[ret_type]['orig_amount'])
                    ac_percents_table_totals[ret_type]['percent'] += row[1][ret_type]['amount'].percent(ac_percents_table_totals[ret_type]['new_candidate_amount'])
                    # print 1001, row[1][ret_type]['amount'].percent(ac_percents_table_totals[ret_type]['new_candidate_amount'])
                    # print 1002, ac_percents_table_totals[ret_type]['percent']

                    string_params[ret_type]['string_amount'] = row[1][ret_type]['amount']
                    # string_params[ret_type]['string_percent'] = "%1.2f" % row[1][ret_type]['amount'].percent(ac_percents_table_totals[ret_type]['orig_amount'])
                    string_params[ret_type]['string_percent'] = "%1.2f" % row[1][ret_type]['amount'].percent(ac_percents_table_totals[ret_type]['new_candidate_amount'])
                    # print 1006, string_params[ret_type]['string_percent']

                new_row = [row[0] + add_to_marker]
                for ret_type in ['Total', 'Retirement', 'Non_Retirement']:
                    new_row.append(row[1][ret_type]['count'])
                    new_row.append(string_params[ret_type]['string_amount'])
                    new_row.append(string_params[ret_type]['string_percent'])
                ac_percents_table_body.append(new_row)
                # print 1006, new_row

        # An extra amount check.
        for ret_type in ['Total', 'Retirement', 'Non_Retirement']:
            # print 1008, ac_percents_table_totals[ret_type]['amount'].get_cents()
            if ac_percents_table_totals[ret_type]['amount'].get_cents() != ac_percents_table_totals[ret_type]['new_candidate_amount'].get_cents():
                reportError("Mismatch ac_percents_table_totals[ret_type]['amount'].get_cents() (" + str(ac_percents_table_totals[ret_type]['amount'].get_cents()) + ") != ac_percents_table_totals[ret_type]['new_candidate_amount'].get_cents() (" + str(ac_percents_table_totals[ret_type]['new_candidate_amount'].get_cents()) + ")")

                sys.exit(1)

        ac_percents_table += ac_percents_table_body

        totals_row = [ \
           'Totals', \
           ac_percents_table_totals['Total']['count'], \
           ac_percents_table_totals['Total']['amount'], \
           "%1.2f" % ac_percents_table_totals['Total']['percent'], \
 \
           ac_percents_table_totals['Retirement']['count'], \
           ac_percents_table_totals['Retirement']['amount'], \
           "%1.2f" % ac_percents_table_totals['Retirement']['percent'], \
 \
           ac_percents_table_totals['Non_Retirement']['count'], \
           ac_percents_table_totals['Non_Retirement']['amount'], \
           "%1.2f" % ac_percents_table_totals['Non_Retirement']['percent'], \
          ]
        ac_percents_table.append(totals_row)

        # ac_percents_table += ['']  # Blank line after table

        # fd = open("pt.csv", "w")
        # for row in ac_percents_table:
        #    fd.write(','.join(list(map(lambda x: str(x), row))) + '\n')
        # fd.close()

        ac_percents_table.append([list().append(' ') for x in new_row]) # blank row

        filename = output_file_prefix + "percents_table"
        rc, output_list_ac_percents_table_columnized = columnize_output(input_data=ac_percents_table, save_filename=filename)
        if rc != 0:
            reportWarning("Non-zero status from columnize_output()")

        # next_option_name, next_option_value = get_next_option()
        # processing_message = "Processing: " + scriptName + ' ' + str(next_option_name) + ' ' + str(next_option_value) + ' ' + Portfolio_xml_filename
        text_to_insert = processing_message + '\n' + "-" * len(output_list_ac_percents_table_columnized[0])
        fd_output = open(filename + ".txt.new", "w")
        fd_output.write(text_to_insert + '\n')
        for line in open(filename + ".txt", "r").read().splitlines():
            fd_output.write(line + '\n')
        fd_output.close()
        os.rename(filename + ".txt.new", filename + ".txt")

        if silent_option == False:
            if len(output_list_ac_percents_table_columnized) > 0:
                printout(text_to_insert)
                for row in output_list_ac_percents_table_columnized: printout(row)

        rc, html_table_string = csv2html.csv2html(list_of_objects=ac_percents_table, num_header_lines_from_top=2)
        # print "875", options
        html_table_string = '<br>' + processing_message + '\n' + html_table_string
        with open(filename + ".html", 'w') as fd:
            fd.write(html_table_string)
        if all_table_files is not None:
            all_table_files.append(filename)
        processing_message = ''

        return 0, ac_percents_table_body


    #==============================

    def show_ac_misc_totals_table(self, ac_totals_sorted_list=None):
        if ac_totals_sorted_list == None:
            ac_totals_sorted_list = []

        # print 1064
        # pprint(ac_totals_sorted_list)

        global options
        global processing_message

        ac_misc_totals = []

        header_row = [ \
              '', \
              'Tot', \
              'Tot', \
              'Tot', \
              'Ret', \
              'Ret', \
              'Ret', \
              'Non_Ret', \
              'Non_Ret', \
              'Non_Ret', \
          ]
        ac_misc_totals.append(header_row)

        header_row = [ \
              '', \
              'count', \
              'amt', \
              'pct', \
              'count', \
              'amt', \
              'pct', \
              'count', \
              'amt', \
              'pct', \
          ]
        ac_misc_totals.append(header_row)

        ac_totals_table = []

        # Scan Investments list and create list of unique ac's being used.  Group them by retirement_class.
        list_of_unique_ac_from_inv_list = {}
        result = self.get_Investments_list()
        for row in result:
            ac_from_inv_list = row.get_value("asset_class")
            retirement_class = row.get_value("retirement_class")
            if retirement_class != 'Non_Retirement':
                retirement_class = 'Retirement'
            if retirement_class not in list_of_unique_ac_from_inv_list:
                list_of_unique_ac_from_inv_list[retirement_class] = []
            if 'Total' not in list_of_unique_ac_from_inv_list:
                list_of_unique_ac_from_inv_list['Total'] = []
            if ac_from_inv_list not in list_of_unique_ac_from_inv_list[retirement_class]:
                list_of_unique_ac_from_inv_list[retirement_class].append(ac_from_inv_list)
            if ac_from_inv_list not in list_of_unique_ac_from_inv_list['Total']:
                list_of_unique_ac_from_inv_list['Total'].append(ac_from_inv_list)

        # print 1119, "before add, list_of_unique_ac_from_inv_list"
        # pprint(list_of_unique_ac_from_inv_list)

        if len(ac_totals_sorted_list) != 0:
            # 'add' option used
            ac_names_we_will_add_money_to = {}
            ac_names_we_will_add_money_to['Total'] = []
            ac_names_we_will_add_money_to['Retirement'] = []
            ac_names_we_will_add_money_to['Non_Retirement'] = []
            for row in ac_totals_sorted_list:
                # print(1320, row)
                for count in xrange(row[1]['Total']['count']):
                    if row[0] not in ac_names_we_will_add_money_to['Total']:
                        ac_names_we_will_add_money_to['Total'].append(row[0])
                for count in xrange(row[1]['Retirement']['count']):
                    if row[0] not in ac_names_we_will_add_money_to['Retirement']:
                        ac_names_we_will_add_money_to['Retirement'].append(row[0])
                for count in xrange(row[1]['Non_Retirement']['count']):
                    if row[0] not in ac_names_we_will_add_money_to['Non_Retirement']:
                        ac_names_we_will_add_money_to['Non_Retirement'].append(row[0])

            list_of_unique_ac_from_inv_list['Total'] = ac_names_we_will_add_money_to['Total']
            list_of_unique_ac_from_inv_list['Retirement'] = ac_names_we_will_add_money_to['Retirement']
            list_of_unique_ac_from_inv_list['Non_Retirement'] = ac_names_we_will_add_money_to['Non_Retirement']

            # print 1132, "added"
            # pprint(list_of_unique_ac_from_inv_list)

        new_row = [ \
           'Asset Classes', \
           len(list_of_unique_ac_from_inv_list['Total']), \
           '', \
           '', \
           len(list_of_unique_ac_from_inv_list['Retirement']), \
           '', \
           '', \
           len(list_of_unique_ac_from_inv_list['Non_Retirement']), \
           '', \
           '', \
          ]
        ac_totals_table.append(new_row)
        ac_totals_table.append([list().append(' ') for x in new_row]) # blank row

        ac_misc_totals += ac_totals_table

        # ac_misc_totals += ['']  # Blank line after table
        ac_misc_totals.append([list().append(' ') for x in new_row]) # blank row

        brokerage_types = {}
        brokerage_per_retirement_class = {}
        result = self.get_Investments_list()
        for row in result:
            brokerage = row.get_value("brokerage")
            curr_total_value = row.get_value("curr_total_value")
            retirement_class = row.get_value("retirement_class")
            if retirement_class != 'Non_Retirement':
                retirement_class = 'Retirement'
            if brokerage not in brokerage_types:
                brokerage_types[brokerage] = {}
            if retirement_class not in brokerage_types[brokerage]:
                brokerage_types[brokerage]['Total'] = {'count':0, 'amount': Money(), 'percent': 0.0}
                brokerage_types[brokerage]['Retirement'] = {'count':0, 'amount': Money(), 'percent': 0.0}
                brokerage_types[brokerage]['Non_Retirement'] = {'count':0, 'amount': Money(), 'percent': 0.0}

            brokerage_types[brokerage][retirement_class]['count'] += 1
            brokerage_types[brokerage][retirement_class]['amount'].add(Money().set_by_string(curr_total_value))

            brokerage_types[brokerage]['Total']['count'] += 1
            brokerage_types[brokerage]['Total']['amount'].add(Money().set_by_string(curr_total_value))

            if retirement_class not in brokerage_per_retirement_class:
                brokerage_per_retirement_class['Total'] = {'count':0, 'amount': Money(), 'percent': 0.00}
                brokerage_per_retirement_class['Retirement'] = {'count':0, 'amount': Money(), 'percent': 0.00}
                brokerage_per_retirement_class['Non_Retirement'] = {'count':0, 'amount': Money(), 'percent': 0.00}
            brokerage_per_retirement_class[retirement_class]['count'] += 1
            brokerage_per_retirement_class[retirement_class]['amount'].add(Money().set_by_string(curr_total_value))

            brokerage_per_retirement_class['Total']['count'] += 1
            brokerage_per_retirement_class['Total']['amount'].add(Money().set_by_string(curr_total_value))

        for brokerage, value in dict.items(brokerage_types):
            for retirement_class in ['Total', 'Retirement', 'Non_Retirement']:
                brokerage_types[brokerage][retirement_class]['percent'] = brokerage_types[brokerage][retirement_class]['amount'].percent(brokerage_per_retirement_class[retirement_class]['amount'])
                brokerage_per_retirement_class[retirement_class]['percent'] += brokerage_types[brokerage][retirement_class]['percent']

        for key, value in dict.items(brokerage_types):
            new_row = [ \
               key, \
               str(value['Total']['count']), \
               value['Total']['amount'].__str__(), \
               "%1.2f" % value['Total']['percent'], \
               str(value['Retirement']['count']), \
               value['Retirement']['amount'].__str__(), \
               "%1.2f" % value['Retirement']['percent'], \
               str(value['Non_Retirement']['count']), \
               value['Non_Retirement']['amount'].__str__(), \
               "%1.2f" % value['Non_Retirement']['percent'], \
           ]
            ac_misc_totals.append(new_row)

        new_row = [ \
              'Totals', \
              brokerage_per_retirement_class['Total']['count'], \
              brokerage_per_retirement_class['Total']['amount'].__str__(), \
              "%1.2f" % brokerage_per_retirement_class['Total']['percent'], \
              brokerage_per_retirement_class['Retirement']['count'], \
              brokerage_per_retirement_class['Retirement']['amount'].__str__(), \
              "%1.2f" % brokerage_per_retirement_class['Retirement']['percent'], \
              brokerage_per_retirement_class['Non_Retirement']['count'], \
              brokerage_per_retirement_class['Non_Retirement']['amount'].__str__(), \
              "%1.2f" % brokerage_per_retirement_class['Non_Retirement']['percent'], \
          ]
        ac_misc_totals.append(new_row)

        # ac_misc_totals += ['']  # Blank line after table
        # ac_misc_totals.append([list().append(' ') for x in new_row]) # blank row

        # output_list_totals += columnize_output(input_data=ac_misc_totals)


        retirement_class_table = []

        retirement_class_table.append([list().append(' ') for x in new_row]) # blank row


        '''
        new_row = [ \
              '', \
              'Tot', \
              'Tot', \
              'Tot', \
              'Ret', \
              'Ret', \
              'Ret', \
              'Non_Ret', \
              'Non_Ret', \
              'Non_Ret', \
          ]
        retirement_class_table.append([list().append(' ') for x in new_row]) # blank row
        retirement_class_table.append(new_row)

        new_row = [ \
              'retirement_class', \
              'count', \
              'amt', \
              'pct', \
              'count', \
              'amt', \
              'pct', \
              'count', \
              'amt', \
              'pct', \
          ]
        retirement_class_table.append(new_row)
        '''

        retirement_class_info = {}
        retirement_class_info_totals = {}
        result = self.get_Investments_list()
        for row in result:
            curr_total_value = row.get_value("curr_total_value")
            retirement_class = row.get_value("retirement_class")
            if retirement_class != 'Non_Retirement':
                retirement_class = 'Retirement'
            if retirement_class not in retirement_class_info:
                retirement_class_info[retirement_class] = {}
                retirement_class_info['Total'] = {'count':0, 'amount': Money()}
                retirement_class_info['Retirement'] = {'count':0, 'amount': Money()}
                retirement_class_info['Non_Retirement'] = {'count':0, 'amount': Money()}

            retirement_class_info[retirement_class]['count'] += 1
            retirement_class_info[retirement_class]['amount'].add(Money().set_by_string(curr_total_value))

            retirement_class_info['Total']['count'] += 1
            retirement_class_info['Total']['amount'].add(Money().set_by_string(curr_total_value))

            if retirement_class not in retirement_class_info_totals:
                retirement_class_info_totals['Total'] = {'count':0, 'amount': Money(), 'percent': 0.00}
                retirement_class_info_totals['Retirement'] = {'count':0, 'amount': Money(), 'percent': 0.00}
                retirement_class_info_totals['Non_Retirement'] = {'count':0, 'amount': Money(), 'percent': 0.00}
            retirement_class_info_totals[retirement_class]['count'] += 1
            retirement_class_info_totals[retirement_class]['amount'].add(Money().set_by_string(curr_total_value))

            retirement_class_info_totals['Total']['count'] += 1
            retirement_class_info_totals['Total']['amount'].add(Money().set_by_string(curr_total_value))

        for retirement_class in ['Total', 'Retirement', 'Non_Retirement']:
            retirement_class_info[retirement_class]['percent'] = retirement_class_info[retirement_class]['amount'].percent(retirement_class_info_totals['Total']['amount'])
            retirement_class_info_totals[retirement_class]['percent'] += retirement_class_info[retirement_class]['percent']

        new_row = [ \
              'retirement_class', \
              retirement_class_info_totals['Total']['count'], \
              retirement_class_info_totals['Total']['amount'].__str__(), \
              "%1.2f" % retirement_class_info_totals['Total']['percent'], \
              retirement_class_info_totals['Retirement']['count'], \
              retirement_class_info_totals['Retirement']['amount'].__str__(), \
              "%1.2f" % retirement_class_info_totals['Retirement']['percent'], \
              retirement_class_info_totals['Non_Retirement']['count'], \
              retirement_class_info_totals['Non_Retirement']['amount'].__str__(), \
              "%1.2f" % retirement_class_info_totals['Non_Retirement']['percent'], \
          ]
        retirement_class_table.append(new_row)

        ac_misc_totals += retirement_class_table

        # ac_misc_totals += ['']  # Blank line after table
        ac_misc_totals.append([list().append(' ') for x in new_row]) # blank row





        owner_table = []

        '''
        new_row = [ \
              '', \
              'Tot', \
              'Tot', \
              'Tot', \
              'Ret', \
              'Ret', \
              'Ret', \
              'Non_Ret', \
              'Non_Ret', \
              'Non_Ret', \
          ]
        owner_table.append([list().append(' ') for x in new_row]) # blank row
        owner_table.append(new_row)

        new_row = [ \
              'owner', \
              'count', \
              'amt', \
              'pct', \
              'count', \
              'amt', \
              'pct', \
              'count', \
              'amt', \
              'pct', \
          ]
        owner_table.append(new_row)
        '''

        owner_info = {}
        owner_info_totals = {}
        result = self.get_Investments_list()
        for row in result:
            owner = row.get_value("owner")
            curr_total_value = row.get_value("curr_total_value")
            retirement_class = row.get_value("retirement_class")
            if retirement_class != 'Non_Retirement':
                retirement_class = 'Retirement'
            if owner not in owner_info:
                owner_info[owner] = {}
            if retirement_class not in owner_info[owner]:
                owner_info[owner]['Total'] = {'count':0, 'amount': Money()}
                owner_info[owner]['Retirement'] = {'count':0, 'amount': Money()}
                owner_info[owner]['Non_Retirement'] = {'count':0, 'amount': Money(), 'percent': 0.00}

            owner_info[owner][retirement_class]['count'] += 1
            owner_info[owner][retirement_class]['amount'].add(Money().set_by_string(curr_total_value))

            owner_info[owner]['Total']['count'] += 1
            owner_info[owner]['Total']['amount'].add(Money().set_by_string(curr_total_value))

            if retirement_class not in owner_info_totals:
                owner_info_totals['Total'] = {'count':0, 'amount': Money(), 'percent': 0.00}
                owner_info_totals['Retirement'] = {'count':0, 'amount': Money(), 'percent': 0.00}
                owner_info_totals['Non_Retirement'] = {'count':0, 'amount': Money(), 'percent': 0.00}
            owner_info_totals[retirement_class]['count'] += 1
            owner_info_totals[retirement_class]['amount'].add(Money().set_by_string(curr_total_value))

            owner_info_totals['Total']['count'] += 1
            owner_info_totals['Total']['amount'].add(Money().set_by_string(curr_total_value))

        for owner, value in dict.items(owner_info):
            for retirement_class in ['Total', 'Retirement', 'Non_Retirement']:
                owner_info[owner][retirement_class]['percent'] = owner_info[owner][retirement_class]['amount'].percent(owner_info_totals[retirement_class]['amount'])
                owner_info_totals[retirement_class]['percent'] += owner_info[owner][retirement_class]['percent']



        for key, value in dict.items(owner_info):
            new_row = [ \
               key, \
               str(value['Total']['count']), \
               value['Total']['amount'].__str__(), \
               "%1.2f" % value['Total']['percent'], \
               str(value['Retirement']['count']), \
               value['Retirement']['amount'].__str__(), \
               "%1.2f" % value['Retirement']['percent'], \
               str(value['Non_Retirement']['count']), \
               value['Non_Retirement']['amount'].__str__(), \
               "%1.2f" % value['Non_Retirement']['percent'], \
           ]
            owner_table.append(new_row)

        new_row = [ \
              'Totals', \
              owner_info_totals['Total']['count'], \
              owner_info_totals['Total']['amount'].__str__(), \
              "%1.2f" % owner_info_totals['Total']['percent'], \
              owner_info_totals['Retirement']['count'], \
              owner_info_totals['Retirement']['amount'].__str__(), \
              "%1.2f" % owner_info_totals['Retirement']['percent'], \
              owner_info_totals['Non_Retirement']['count'], \
              owner_info_totals['Non_Retirement']['amount'].__str__(), \
              "%1.2f" % owner_info_totals['Non_Retirement']['percent'], \
          ]
        owner_table.append(new_row)

        ac_misc_totals += owner_table

        # ac_misc_totals += ['']  # Blank line after table
        ac_misc_totals.append([list().append(' ') for x in new_row]) # blank row


        filename = output_file_prefix + 'ac_misc_totals_table'
        rc, output_list_totals = columnize_output(input_data=ac_misc_totals, save_filename=filename)
        if rc != 0:
            reportWarning("Non-zero status from columnize_output()")

        text_to_insert = processing_message + '\n' + "-" * len(output_list_totals[0])
        fd_output = open(filename + ".txt.new", "w")
        fd_output.write(text_to_insert + '\n')
        for line in open(filename + ".txt", "r").read().splitlines():
            fd_output.write(line + '\n')
        fd_output.close()
        os.rename(filename + ".txt.new", filename + ".txt")

        if silent_option == False:
            if len(output_list_totals) > 0:
                printout(text_to_insert)
                for row in output_list_totals: printout(row)

        rc, html_table_string = csv2html.csv2html(list_of_objects=ac_misc_totals, num_header_lines_from_top=2)
        html_table_string = '<br>' + processing_message + '\n' + html_table_string
        with open(filename + ".html", 'w') as fd:
            fd.write(html_table_string)
        if all_table_files is not None:
            all_table_files.append(filename)
        processing_message = ''

        # return 0, ac_totals_sorted_list
        return 0, ''

    #==============================

    def add_to_investment(self, pt_cmd_add):

        rc, ac_totals_sorted_list = self.get_ac_amounts_from_inv_list()

        # print("before add:")
        # pprint(ac_totals_sorted_list)

        match = False
        asset_class_param = 'TBD_asset_class'
        ac_totals_sorted_list_revised = []
        pt_params = pt_cmd_add.split(':')[1:]
        for row in ac_totals_sorted_list:
            asset_class_from_list = row[0]
            Total_new_amount = Money().set_by_string(row[1]['Total']['amount'].__str__())
            Total_orig_amount = Money().set_by_string(row[1]['Total']['amount'].__str__())
            Total_added_amount = Money()
            Total_added_count = row[1]['Total']['count']
            Retirement_new_amount = Money().set_by_string(row[1]['Retirement']['amount'].__str__())
            Retirement_orig_amount = Money().set_by_string(row[1]['Retirement']['amount'].__str__())
            Retirement_added_amount = Money()
            Retirement_added_count = row[1]['Retirement']['count']
            Non_Retirement_new_amount = Money().set_by_string(row[1]['Non_Retirement']['amount'].__str__())
            Non_Retirement_orig_amount = Money().set_by_string(row[1]['Non_Retirement']['amount'].__str__())
            Non_Retirement_added_amount = Money()
            Non_Retirement_added_count = row[1]['Non_Retirement']['count']
            # marker = ''
            added_to = False
            for param in pt_params:
                asset_class_param = param.split(',')[0]
                ret_class_name_param = param.split(',')[1]
                if ret_class_name_param != 'Retirement' and ret_class_name_param != 'Non_Retirement':
                    reportError("Illegal retirement class '" + ret_class_name_param + "' in runstring.")
                    usage()
                new_added_amount = Money().set_by_string(param.split(',')[2])
                # print "1217", row[0] , asset_class_param
                if asset_class_from_list == asset_class_param:
                    added_to = True
                    match = True
                    if ret_class_name_param == 'Retirement':
                        Retirement_new_amount.add(new_added_amount)
                        Retirement_added_amount.add(new_added_amount)
                        Retirement_added_count += 1
                    if ret_class_name_param == 'Non_Retirement':
                        Non_Retirement_new_amount.add(new_added_amount)
                        Non_Retirement_added_amount.add(new_added_amount)
                        Non_Retirement_added_count += 1
                    Total_new_amount.add(new_added_amount)
                    # print '1225', Total_added_amount.__str__()
                    Total_added_amount.add(new_added_amount)
                    Total_added_count += 1
                    # marker = '* '

            new_row = [ \
               asset_class_from_list, \
               { \
                  'added_to': added_to, \
                  'Total': \
                     { \
                        'count':Total_added_count, \
                        'new_candidate_amount':Total_new_amount, \
                        'orig_amount':Total_orig_amount, \
                        'added_amount':Total_added_amount, \
                     }, \
                  'Retirement': \
                     { \
                        'count':Retirement_added_count, \
                        'new_candidate_amount':Retirement_new_amount, \
                        'orig_amount':Retirement_orig_amount, \
                        'added_amount':Retirement_added_amount, \
                     }, \
                  'Non_Retirement': \
                     { \
                        'count':Non_Retirement_added_count, \
                        'new_candidate_amount':Non_Retirement_new_amount, \
                        'orig_amount':Non_Retirement_orig_amount, \
                        'added_amount':Non_Retirement_added_amount, \
                     } \
               } \
           ]
            ac_totals_sorted_list_revised.append(new_row)

        if match == False:
            reportError("Unrecognized asset class name '" + asset_class_param + "' in runstring pt command.  pt_cmd_add = " + pt_cmd_add)
            sys.exit(1)

        # output_list = self.__show_ac_totals_sorted_list_revised_table__(ac_totals_sorted_list=ac_totals_sorted_list_revised, pt_cmd_lp=pt_cmd_lp)

        # print("after add:")
        # pprint(ac_totals_sorted_list_revised)

        return ac_totals_sorted_list_revised

    #==============================

    def get_symbol_list(self, input_filename):
        if not os.path.isfile(input_filename):
            return 1, "File does not exist: " + input_filename
        file_line_num = 0
        fd = open(input_filename, "r")
        filelist = fd.read().splitlines()
        fd.close()
        symbol_list = []
        skipped_symbols = []
        # skip_ac_for_next_symbol = False
        for line in filelist:
             file_line_num += 1
             # if '<asset_class>Individual_Stocks</asset_class>' in line:
             #    skip_ac_for_next_symbol = True
             #    continue
    
             if '<symbol>' in line and 'NOSYMB' not in line:
                  symbol = re.sub('^ *<symbol>([^<]+)<.*$', r'\1', line)
                  # if skip_ac_for_next_symbol == True:
                  #    skipped_symbols.append(symbol)
                  #    skip_ac_for_next_symbol = False
                  #    continue
                  if symbol not in symbol_list:
                      symbol_list.append(symbol)
                  continue

             if 'NOSYMB' in line:
                  symbol_list.append('NOSYMB')
    
        symbol_list_csv = ','.join(symbol_list)
        return 0, symbol_list_csv

    #==============================

    def Portfolio_xml_file_to_xml_string(self, input_filename):
        global price_web_update
        global ac_web_update
        global ac_from_web
        global processing_message

        self._errors = []
        if input_filename == '':
            msg = "Empty input_filename."
            reportError(msg)
            self._errors.append(msg)
            return 1, ''

        # if silent_option == False:
        #     printout(processing_message)
        #     processing_message = ''

        # print "1244", price_web_update

        # For a price_web_update, make sure multiple lots of the same investment use the same current share price.
        symbol_list_csv = ''
        share_prices = {}
        if price_web_update == 0:
            # processing_message = processing_message + "\nProcessing: for Portfolio_xml_file_to_xml_string():  --price_web_update"
            processing_message = "\nProcessing: --price_web_update"
            if silent_option == False:
                printout(processing_message)
                processing_message = ''
            # Create symbol list.
            symbol_list = ''
            separator = ''

            rc, results = self.get_symbol_list(input_filename)
            if rc != 0:
                reportError("Calling get_symbol_list().  Results = " + str(results))
                sys.exit(1)
            symbol_list_csv = results
            rc, results = get_share_price(symbol_list_csv)
            if rc != 0:
                reportError("Calling get_share_price() for symbols = " + symbol_list_csv + ".  Results = " + str(results))
                sys.exit(1)

            # print results
            share_prices = results
            # print "1257", share_prices

            import test_flags
            if hasattr(test_flags, '_product_called_from_test'):
                if test_flags._product_called_from_test == True:
                    # used within a test run
                    test_share_prices = {}
                    fake_price = 1
                    for key in dict.items(share_prices):
                        test_share_prices[key] = fake_price
                        if fake_price == 1:
                           fake_price = 10
                        else:
                           fake_price = 1
                    share_prices = test_share_prices
    
            price_web_update = 1

        asset_class_name_from_web_in_file = {}
        ac_comparison_dict = {}

        if ac_web_update == 0:
            # processing_message = processing_message + "\nProcessing: for Portfolio_xml_file_to_xml_string():  --ac_web_update"
            processing_message = "\nProcessing: --ac_web_update"
            if silent_option == False:
                printout(processing_message)
                processing_message = ''

            rc, results = self.get_symbol_list(input_filename)
            if rc != 0:
                reportError("Calling get_symbol_list().  Results = " + str(results))
                sys.exit(1)
            # print(1818, results)
            symbol_list_csv = results
            rc, results = get_asset_class_names_from_web(symbol_list_csv)
            if rc != 0:
                reportError("Calling get_asset_class_names_from_web() for symbols = " + symbol_list_csv + ".  Results = " + str(results))
                sys.exit(1)

            ac_from_web = results
            # print(1800, ac_from_web)
            # for symbol in skipped_symbols:
            #    ac_from_web[symbol] = 'Individual_Stocks'

            ac_web_update = 1

        # tree = ET.parse(input_filename)
        file_line_num = 0
        xml_string_final = ''
        field = ''
        tag = ''
        portfolio_version = ''

        Investment_start = False
        cost_basis_start = False
        cb_event_start = False
        tvh_start = False

        inv_ID_dict = {}
        account_ID_dict = {}

        get_errors = False
        for line in open(input_filename, "r").read().splitlines():
            file_line_num += 1

            if "<top>" in line:
                xml_string_final += '<top>'
                continue

            if "<Investments>" in line:
                xml_string_final += '<Investments>'
                continue

            if "<Portfolio_version>" in line:
                xml_string_final += line.strip()
                continue

            if "<errors>" in line:
                get_errors = True
                continue
            if "</errors>" in line:
                get_errors = False
                continue
            if get_errors == True:
                self._errors.append(line)
                continue

            if "<filename>" in line:
                continue  # ignore old value already in file
            if "<file_line_num>" in line:
                continue  # ignore old value already in file

            line = re.sub('^ *', '', line) # remove any indents from input lines

            #-----------------------
            # start of Investment record found.

            if "<Investment>" in line:
                Investment_start = True
                # fields to help debugging
                xml_string = "<Investment>"
                xml_string += "<filename>" + input_filename + "</filename>"
                xml_string += "<file_line_num>" + str(file_line_num) + "</file_line_num>"
                cost_basis_start = False
                cb_event_start = False
                tvh_start = False

                curr_total_value = 0.0
                curr_quantity = 0.0
                curr_share_price = "0.00"

                tvh_total_value = 0.0
                tvh_quantity = 0.0
                tvh_share_price = 0.0
                continue

            #-----------------------
            # end of Investment record found.

            if "</Investment>" in line:

                found = re.search("<symbol>([^<]*)</symbol>", xml_string)
                if not found:
                    msg = "xml_string missing symbol.  file_line_num = " + str(file_line_num) + ".  xml_string = " + xml_string
                    reportError(msg)
                    return 1, msg

                symbol = found.group(1)
                # print "1333", "symbol", symbol, "symbol"

                if price_web_update != 1 or share_prices.get(symbol, True):
                    found = re.search("<curr_share_price>([^<]*)</curr_share_price>", xml_string)
                    if not found:
                         msg = "Cannot find curr_share_price in xml_string"
                         reportError(msg)
                         return 1, msg
                    curr_share_price = found.group(1)
                else:
                    # rc, results = get_share_price(symbol)
                    # if rc != 0:
                    #    # reportError("Calling get_share_price(): " + str(results) + ": for symbol = " + symbol)
                    #    msg = "Calling get_share_price(): " + str(results)
                    #    reportError(msg)
                    #    return rc, msg
                    curr_share_price = share_prices.get(symbol, 'not_found')
                    if curr_share_price == 'not_found':
                        msg = symbol + " not found in share_prices dict."
                        reportError(msg)
                        return 1, msg
                    # print "1344", symbol, curr_share_price

                xml_string = re.sub("<curr_share_price>([^<]*)</curr_share_price>", "<curr_share_price>"+curr_share_price+"</curr_share_price>", xml_string)
                # print "1348", xml_string

                curr_share_price = float(curr_share_price)
                # print "1352", symbol, curr_share_price

                if curr_quantity != 0.0 or curr_share_price != 0.0:
                    curr_total_value = curr_quantity * curr_share_price
                xml_string = re.sub("<curr_total_value>([^<]*)</curr_total_value>", "<curr_total_value>"+ str("%1.2f" % curr_total_value) + "</curr_total_value>", xml_string)

                if tvh_quantity != 0.0 or tvh_share_price != 0.0:
                    tvh_total_value = tvh_quantity * tvh_share_price
                xml_string = re.sub("<tvh_total_value>([^<]*)</tvh_total_value>", "<tvh_total_value>"+ str("%1.2f" % tvh_total_value) + "</tvh_total_value>", xml_string)


                if ac_web_update == 1:
                    # Verify that asset_class has the correct value.
                    found = re.search("<asset_class>([^<]*)</asset_class>", xml_string)
                    if not found:
                        msg = "symbol " + symbol + ": Missing asset_class field in xml string."
                        reportError(msg)
                        return 1, msg
                    asset_class_name_in_file = found.group(1)

                    value = ac_from_web.get(symbol, 'unknown')
                    if value == 'unknown':
                        msg = "symbol " + symbol + ": Missing symbol in ac_from_web dict."
                        return 1, reportError(msg, mode='return_msg_only')
                    asset_class_name_from_web = ac_from_web[symbol]

                    found = re.search("<asset_class_from_web>([^<]*)</asset_class_from_web>", xml_string)
                    if not found:
                        msg = "symbol " + symbol + ": Missing asset_class_from_web field in xml string.  Will add it."
                        reportWarning(msg)
                        xml_string += "<asset_class_from_web>" + asset_class_name_from_web + "</asset_class_from_web>"
                        # asset_class_name_from_web_in_file[symbol] = asset_class_name_from_web
                        asset_class_name_from_web_in_file[symbol] = 'not_set'
                    else:
                        asset_class_name_from_web_in_file[symbol] = found.group(1)

                    if asset_class_name_from_web_in_file[symbol] != 'not_set':
                        if asset_class_name_from_web_in_file[symbol] != asset_class_name_from_web:
                            msg = "file_line_num " + str(file_line_num) + ": symbol " + symbol + ": asset_class_name_from_web_in_file[symbol](" + asset_class_name_from_web_in_file[symbol] + ") != asset_class_name_from_web(" + asset_class_name_from_web + ")."
                            reportError(msg)
                            return 1, msg

                    ac_comparison_dict[symbol] = {'from_web':asset_class_name_from_web, 'set_in_file': asset_class_name_in_file, 'from_web_in_file': asset_class_name_from_web_in_file[symbol]}
                    # if symbol == 'VDIGX':
                    #    print "1541," + ac_comparison_dict[symbol]['from_web'] + "," + ac_comparison_dict[symbol]['set_in_file'] + "," + symbol

                xml_string += "</Investment>"
                # dont_care, xml_string_sorted_list = sort_nested_list(xml_string)
                # print xml_string_sorted_list
                # xml_string_final += convert_nested_xml_list_to_xml_string(xml_string_sorted_list)

                xml_string_final += xml_string

                xml_string = ''
                Investment_start = False
                continue

            #-----------------------
            # process Investment record fields.

            if Investment_start == True:
                # print "line = " + line

                # single-line xml element

                if '<cost_basis>' in line:
                    cost_basis_start = True
                    xml_string += line
                    continue

                if '</cost_basis>' in line:
                    cost_basis_start = False
                    xml_string += line
                    continue

                if cost_basis_start == True:

                    if '<cb_event>' in line:
                        cb_event_start = True
                        cb_total_value = 0.0
                        cb_quantity = 0.0
                        cb_share_price = 0.0
                        xml_string += line
                        continue

                    if '</cb_event>' in line:
                        cb_event_start = False
                        if cb_quantity != 0.0 and cb_share_price != 0.0:
                            cb_total_value = cb_quantity * cb_share_price
                            xml_string = re.sub("<cb_total_value>([^<]*)</cb_total_value>", "<cb_total_value>"+ str("%1.2f" % cb_total_value) + "</cb_total_value>", xml_string)
                        xml_string += line
                        continue

                    if cb_event_start == True:

                        found = re.search("<cb_total_value>([^<]*)</cb_total_value>", line)
                        if found:
                            if found.group(1) != '' and 'TBD' not in found.group(1):
                                cb_total_value = float(found.group(1))
                            xml_string += line
                            continue

                        found = re.search("<cb_quantity>([^<]*)</cb_quantity>", line)
                        if found:
                            if found.group(1) != '' and 'TBD' not in found.group(1):
                                cb_quantity = float(found.group(1))
                            xml_string += line
                            continue

                        found = re.search("<cb_share_price>([^<]*)</cb_share_price>", line)
                        if found:
                            if found.group(1) != '' and 'TBD' not in found.group(1):
                                cb_share_price = float(found.group(1))
                            xml_string += line
                            continue

                        xml_string += line
                        continue

                if '<total_value_hi>' in line:
                    tvh_start = True
                    xml_string += line
                    continue

                if '</total_value_hi>' in line:
                    tvh_start = False
                    if tvh_quantity != 0.0 and tvh_share_price != 0.0:
                        tvh_total_value = tvh_quantity * tvh_share_price
                        xml_string = re.sub("<tvh_total_value>([^<]*)</tvh_total_value>", "<tvh_total_value>"+ str("%1.2f" % tvh_total_value) + "</tvh_total_value>", xml_string)
                    xml_string += line
                    continue

                if tvh_start == True:

                    found = re.search("<tvh_total_value>([^<]*)</tvh_total_value>", line)
                    if found:
                        xml_string += line
                        continue

                    found = re.search("<tvh_quantity>([^<]*)</tvh_quantity>", line)
                    if found:
                        if found.group(1) != '' and 'TBD' not in found.group(1):
                            tvh_quantity = float(found.group(1))
                        xml_string += line
                        continue

                    found = re.search("<tvh_share_price>([^<]*)</tvh_share_price>", line)
                    if found:
                        if found.group(1) != '' and 'TBD' not in found.group(1):
                            tvh_share_price = float(found.group(1))
                        xml_string += line
                        continue

                    xml_string += line
                    continue


                found = re.search("<curr_total_value>([^<]*)</curr_total_value>", line)
                if found:
                    if found.group(1) != '' and 'TBD' not in found.group(1):
                        curr_total_value = float(found.group(1))
                    xml_string += line
                    continue

                found = re.search("<curr_quantity>([^<]*)</curr_quantity>", line)
                if found:
                    if found.group(1) != '' and 'TBD' not in found.group(1):
                        curr_quantity = float(found.group(1))
                    xml_string += line
                    continue

                found = re.search("<curr_share_price>([^<]*)</curr_share_price>", line)
                if found:
                    if found.group(1) != '' and 'TBD' not in found.group(1):
                        curr_share_price = found.group(1)
                    xml_string += line
                    continue

                # found = re.search("<symbol>([^<]*)</symbol>", line)
                # if found:
                #    symbol = found.group(1)
                #
                # if '<symbol>' in line:
                #    xml_string += line
                #    continue

                # Verify there are no duplicates of our internal ID numbers.
                found = re.search("<inv_ID>([^<]*)</inv_ID>", line)
                if found:
                    inv_ID_string = found.group(1)
                    # print "1515: inv_ID_string", inv_ID_string
                    if inv_ID_string in inv_ID_dict:
                        msg = "inv_ID " + inv_ID_string + " at file_line_num = " + str(file_line_num) + " already exists at file_line_num = " + inv_ID_dict[inv_ID_string]
                        reportError(msg)
                        return 1, msg
                    inv_ID_dict[inv_ID_string] = str(file_line_num)
                    xml_string += line
                    continue

                # Verify there are no duplicate official account ID numbers.
                found = re.search("<account_ID>([^<]*)</account_ID>", line)
                if found:
                    account_ID_string = found.group(1)
                    if account_ID_string in account_ID_dict:
                        msg = "account_ID " + account_ID + " at file_line_num = " + str(file_line_num) + " already exists at file_line_num = " + account_ID_dict[account_ID_string]
                        reportError(msg)
                        return 1, msg
                    account_ID_dict[account_ID_string] = str(file_line_num)
                    xml_string += line
                    continue


                '''
                if re.search("^<[^>]+>.*</[^>]+>", line):
                   xml_string += line
                   continue
                '''
                # multi-line xml element
                '''
                if re.search("^<[^>]+>", line):
                   xml_string += line
                   continue
                if re.search("^</[^>]+>", line):
                   xml_string += line
                   continue
                xml_string += line
                '''
                xml_string += line

                continue
            # else ignore anything outside of an <Investment> block.

        if ac_web_update == 1:
            # Contains expected duplicates:
            # print '\n'.join(map(str, sorted(sorted([(value['from_web'], value['set_in_file']) for key, value in dict.items(ac_comparison_dict)], key=itemgetter('set_in_file')), key=itemgetter('from_web'))))
            filename = output_file_prefix + "ac_web_check"
            fd_output = open(filename + ".txt", "w")
            templist_sorted = list(map(lambda x: ','.join(x), sorted(sorted([(value['from_web'], value['set_in_file'], value['from_web_in_file'], key) for key, value in dict.items(ac_comparison_dict)], key=itemgetter(1)), key=itemgetter(0))))
            for line in templist_sorted:
                fd_output.write(str(line) + '\n')
            fd_output.close()
            # processing_message = "\nProcessing: for Portfolio_xml_file_to_xml_string():  --ac_web_update"
            create_output_files(filename, input_data=templist_sorted, silent_option=True)
            # Does not work:
            # print '\n'.join(sorted(sorted([(value['from_web'], value['set_in_file']) for key, value in dict.items(ac_comparison_dict)], key=itemgetter('set_in_file')), key=itemgetter('from_web')))

            '''
            # Does not contain duplicates:
            # print '-----------------------'
            templist_sorted = sorted(sorted([[value['from_web'], str(value['set_in_file']), value['from_web_in_file'], [key]] for key, value in dict.items(ac_comparison_dict)], key=itemgetter(1)), key=itemgetter(0))
            # print '\n'.join(map(str, [templist_sorted[index] for index in xrange(len(templist_sorted)) if index==0 or templist_sorted[index] != templist_sorted[index-1]]))
            filename = output_file_prefix + "ac_web_check_no_dupes"
            fd_output = open(filename + ".txt", "w")
            # templist_sorted_no_dupes = [templist_sorted[index] for index in xrange(len(templist_sorted)) if index==0 or templist_sorted[index][0] != templist_sorted[index-1][0]  or templist_sorted[index][1] != templist_sorted[index-1][1]]
            templist_sorted_no_dupes = []
            for index in xrange(len(templist_sorted)):
               if index==0:
                  templist_sorted_no_dupes.append(templist_sorted[index])
                  continue
               if templist_sorted[index][0] == templist_sorted[index-1][0] and templist_sorted[index][1] == templist_sorted[index-1][1]:
                  templist_sorted_no_dupes[-1][3].append(templist_sorted[index][3][0])
                  continue
               templist_sorted_no_dupes.append(templist_sorted[index])

            for line in templist_sorted_no_dupes:
               fd_output.write(str(line) + '\n')
            fd_output.close()

               for symbol in templist_sorted_no_dupes[index][3]:
                  print 1780, symbol, templist_sorted_no_dupes[index][0], asset_class_name_from_web_in_file[symbol]
                  if templist_sorted_no_dupes[index][0] == asset_class_name_from_web_in_file[symbol]:  # To avoid symbols/investments that return the wrong asset class from financial web sites.
                     continue
            '''


            msg = "One ac web match can have multiple internal ac matches.  Could indicate possible ac miscategorization.\n"
            possible_miscats = ""
            for index in xrange(1, len(templist_sorted)):
                if templist_sorted[index][3] == 'NOSYMB':
                    continue
                if templist_sorted[index][0] == templist_sorted[index][2]:  # To avoid symbols/investments that return the wrong asset class from financial web sites.
                    continue
                if templist_sorted[index][0] == templist_sorted[index-1][0] and templist_sorted[index][1] != templist_sorted[index-1][1]:
                    possible_miscats += str(templist_sorted[index-1]) + "\n"
                    possible_miscats += str(templist_sorted[index]) + "\n"

                    '''
                    msg = "One ac web match has multiple internal ac matches.  Could indicate possible ac miscategorization.\n" + \
                          "   ac_from_web:                   " + templist_sorted[index][0] + "\n" + \
                          "   ac_internal[index-1]:          " + templist_sorted[index-1][1] + "\n" + \
                          "   ac_internal[index-1][symbol]:  " + str(templist_sorted[index-1][2]) + "\n" + \
                          "   ac_internal[index]:            " + templist_sorted[index][1] + "\n" + \
                          "   ac_internal[index][symbol]:    " + str(templist_sorted[index][2]) + "\n"
                    '''
            if possible_miscats != "":
                msg += possible_miscats
                reportError(msg)

            # for key, value in dict.items(ac_comparison_dict):
            #   print "1731," + ac_comparison_dict[symbol]['from_web'] + "," + ac_comparison_dict[symbol]['set_in_file'] + "," + symbol

            '''
            # Look through our investments with miscategorized asset classes:
            # for loop in ['compare_web_to_file', 'compare_file_to_web']:
            for loop in ['compare_web_to_file']:
               if loop == 'compare_web_to_file':
                  compare_from = 'from_web'
                  compare_to   = 'set_in_file'
               else:  # 'compare_file_to_web'
                  compare_from = 'set_in_file'
                  compare_to   = 'from_web'

               print "================================================="
               print loop+':'
               for key, value in dict.items(ac_comparison_dict):
                  for key2, value2 in dict.items(ac_comparison_dict):
                     if ac_comparison_dict[key][compare_from] == ac_comparison_dict[key2][compare_from] and ac_comparison_dict[key][compare_to]   != ac_comparison_dict[key2][compare_to]:
                        # msg = "Mismatch on symbol " + key + " for ac_comparison_dict[key][compare_from] (" + ac_comparison_dict[key][compare_from] + ") == ac_comparison_dict[key2][compare_from] (" + ac_comparison_dict[key2][compare_from] + ") and ac_comparison_dict[key][compare_to] (" + ac_comparison_dict[key][compare_to] + ") != ac_comparison_dict[key2][compare_to] (" + ac_comparison_dict[key2][compare_to] + ")."
                        msg = "Mismatch for symbol " + key + " on:\n" + \
                              "   Should equal:\n" + \
                              "      ac_comparison_dict[key][compare_from]:  " + ac_comparison_dict[key][compare_from] + "\n" + \
                              "      ac_comparison_dict[key2][compare_from]: " + ac_comparison_dict[key2][compare_from] + "\n" + \
                              "   Should equal but does not:\n" + \
                              "      ac_comparison_dict[key][compare_to]:    " + ac_comparison_dict[key][compare_to] + "\n" + \
                              "      ac_comparison_dict[key2][compare_to]:   " + ac_comparison_dict[key2][compare_to]
                        reportError(msg)

            '''


            ac_web_update = -1


        xml_string_final += xml_string + '</Investments>' + '</top>'

        return 0, xml_string_final


    #==============================

    def xml_string_to_Python_data_tree(self, xml_string='', ListOrDict_child_xml_data_structure=None, parent_key_path='', list_of_list_parent_key_paths=None, phases=['create_Python_data_tree_and_lists_list', 'use_lists_list_to_correct_Python_data_tree']):

        import collections

        if '2' in get_option('--debug', ''): printout('Entered xml_string_to_Python_data_tree.  Phases: ' + str(phases))

        if list_of_list_parent_key_paths == None:
            list_of_list_parent_key_paths = []

        '''
        All user actions are performed on a Python data tree.
        which comes from
        an xml string
        which comes from
        an xml file.


        This function returns a data tree that does not contain pointers/instances.  The tree is self-contained.


        The current level in the XML data tree is what we will call the "parent".  Because for the parent to determine whether it is a dict, list, or element, it needs to examine its children to see:

        - Do all of its children have the same name and data type?  If so, the parent is a list.
        - If any of its children have a different name and data type from each other, then the parent is a dict.
        - If the parent has no children, then the parent is an element.

        - Exception:  If a parent only has one child, is the parent a dict or a list?  Example:  top:Investments:Investment[1]:cost_basis:cb_event contains one cb_event.

  It's possible that another equivalent parent in our xml data tree may have 2 or more matching children, which means that that parent is a list:

  This cost_basis parent contains 2 cb_events:
     top:Investments:Investment[2]:cost_basis:cb_event[0]
     top:Investments:Investment[2]:cost_basis:cb_event[1]

  So we will need to perform one phase looking for all list parents and recording them in a list.

  Then repeat the phase but when we encounter one-child parents, we'll compare them to our list and if these parents are on our list, treat these parents as lists.

        '''

        for phase in phases:

            # print "phase: " + phase

            # print "xml_string = " + xml_string
            # print "ListOrDict_parent_Python_data_structure: " + str(ListOrDict_parent_Python_data_structure)

            top = False
            # print "1556", ListOrDict_child_xml_data_structure
            if ListOrDict_child_xml_data_structure is None:
                # Do initialization for each phase of this recursive function.
                top = True
                # xml_string = "<top>" + xml_string + "</top>" # so findall works correctly.
                # print "1602", xml_string
                tree = get_xml_tree(xml_string)
                root = tree.getroot()
                Investment_start = False
                # ListOrDict_parent_Python_data_structure_name = "top"
                # ListOrDict_parent_Python_data_structure[ListOrDict_parent_Python_data_structure_name] = None
                # print "first: " + str(ListOrDict_parent_Python_data_structure[ListOrDict_parent_Python_data_structure_name])
                # ListOrDict_parent_Python_data_structure = ListOrDict_parent_Python_data_structure[ListOrDict_parent_Python_data_structure_name]
                # ListOrDict_child_xml_data_structure = list(root)
                ListOrDict_child_xml_data_structure = root
                self._python_data_tree = None
                parent_key_path = 'top'

            ListOrDict_parent_Python_data_structure = None

            # Identify current ListOrDict type Python data type (dict, list, none) depending on its child elements.  For example, if all of its child elements are the same type with the same element name, then that is a Python list.
            # ListOrDict_parent_xml_data_type = 'single'
            if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1583 len(ListOrDict_child_xml_data_structure) = " + str(len(ListOrDict_child_xml_data_structure)))
            curr_child_tag = ''
            for child in ListOrDict_child_xml_data_structure:
                if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1585 child = " + str(child))
                # print "findall: " + curr_child_tag + "," + child.tag
                if curr_child_tag == '':
                    curr_child_tag = child.tag
                    # ListOrDict_parent_xml_data_type = 'dict'
                    # ListOrDict_parent_Python_data_structure = collections.OrderedDict()  # OrderedDict so Portfolio_version field stays at top of the tree.
                    if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1592 type(ListOrDict_parent_Python_data_structure) = " + str(type(ListOrDict_parent_Python_data_structure)))
                    continue
                if child.tag != curr_child_tag:
                    # ListOrDict_parent_xml_data_type = 'dict'
                    ListOrDict_parent_Python_data_structure = collections.OrderedDict()  # OrderedDict so Portfolio_version field stays at top of the tree.
                    if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1598 type(ListOrDict_parent_Python_data_structure) = " + str(type(ListOrDict_parent_Python_data_structure)))
                    break
                else:
                    # ListOrDict_parent_xml_data_type = 'list'
                    ListOrDict_parent_Python_data_structure = []
                    if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1604 type(ListOrDict_parent_Python_data_structure) = " + str(type(ListOrDict_parent_Python_data_structure)))

            if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1606 type(ListOrDict_parent_Python_data_structure) = " + str(type(ListOrDict_parent_Python_data_structure)))

            if phase == 'create_Python_data_tree_and_lists_list':
                # if ListOrDict_parent_xml_data_type == 'list':
                if 'list' in str(type(ListOrDict_parent_Python_data_structure)):
                    if parent_key_path not in list_of_list_parent_key_paths:
                        list_of_list_parent_key_paths.append(parent_key_path)
                        if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1610 Collected list parent_key_path = " + parent_key_path)

            else:  # phase == 'use_lists_list_to_correct_Python_data_tree'
                if '2' in get_option('--debug', ''):
                    printout(phase[0] + ' ' + "1611", "parent_key_path = ", parent_key_path)
                    for loop in list_of_list_parent_key_paths:
                        printout(phase[0] + ' ' + "1599", "list parent_key_paths", loop)

                if parent_key_path in list_of_list_parent_key_paths:
                    if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + 'match, parent_key_path: ' + parent_key_path)
                    if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1620 type(ListOrDict_parent_Python_data_structure) = " + str(type(ListOrDict_parent_Python_data_structure)))
                    ListOrDict_parent_Python_data_structure = []
                    if 'cost_basis' in parent_key_path:
                        if '2' in get_option('--debug', ''):
                            printout(phase[0] + ' ' + '1619 cost_basis: ', parent_key_path)
                            import pprint
                            pprint.pprint(ListOrDict_parent_Python_data_structure)
                    if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1622 Corrected list parent_key_path = " + parent_key_path)
                    if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1624 type(ListOrDict_parent_Python_data_structure) = " + str(type(ListOrDict_parent_Python_data_structure)))


            if ListOrDict_parent_Python_data_structure is None:
                ListOrDict_parent_Python_data_structure = collections.OrderedDict()  # OrderedDict so Portfolio_version field stays at top of the tree.


            # for ListOrDict_parent_xml in ListOrDict_child_xml_data_structure:
            # for ListOrDict_parent_xml in ListOrDict_child_xml_data_structure.findall('.//*'):
            # for ListOrDict_parent_xml in ListOrDict_child_xml_data_structure: print "1612", ListOrDict_parent_xml
            for ListOrDict_child_xml in ListOrDict_child_xml_data_structure:
                if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1608", parent_key_path, ListOrDict_child_xml)
                if '2' in get_option('--debug', ''): printout("len: " + str(len(ListOrDict_child_xml)))

                if len(ListOrDict_child_xml) == 0:  # child is an end element
                    if 'list' in str(type(ListOrDict_parent_Python_data_structure)):
                    # if ListOrDict_parent_xml_data_type == 'list':  # current ListOrDict is list
                        # if ListOrDict_parent_Python_data_structure is None:
                        #    ListOrDict_parent_Python_data_structure = []
                        ListOrDict_parent_Python_data_structure.append([ListOrDict_child_xml.tag, ListOrDict_child_xml.text])
                        printout(phase[0] + ' ' + "1670 " + ListOrDict_child_xml.tag + ", " + str(ListOrDict_child_xml.text))
                    else:  # current ListOrDict is dict
                        # if ListOrDict_parent_Python_data_structure is None:
                        #    ListOrDict_parent_Python_data_structure = collections.OrderedDict()  # OrderedDict so Portfolio_version field stays at top of the tree.
                        ListOrDict_parent_Python_data_structure[ListOrDict_child_xml.tag] = ListOrDict_child_xml.text
                        if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1675 " + ListOrDict_child_xml.tag + ", " + str(ListOrDict_child_xml.text))

                else: # current ListOrDict parents are dicts or lists themselves.

                    if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1644 type(ListOrDict_parent_Python_data_structure) = " + str(type(ListOrDict_parent_Python_data_structure)))

                    # Recursion

                    if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1642 Recursion", ListOrDict_child_xml)
                    if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1658 parent_key_path = ", parent_key_path)
                    rc, temp_Python_data_structure, list_of_list_parent_key_paths = self.xml_string_to_Python_data_tree('', ListOrDict_child_xml_data_structure=ListOrDict_child_xml, list_of_list_parent_key_paths=list_of_list_parent_key_paths, parent_key_path=parent_key_path+':'+ListOrDict_child_xml.tag, phases=[phase])

                    if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1661 Returned from Recursion", ListOrDict_child_xml)
                    if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1662 parent_key_path = " + parent_key_path)
                    if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1663 type(ListOrDict_parent_Python_data_structure) = " + str(type(ListOrDict_parent_Python_data_structure)))
                    if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1687 ListOrDict_child_xml.tag = " + ListOrDict_child_xml.tag)

                    if parent_key_path+':'+ListOrDict_child_xml.tag in list_of_list_parent_key_paths:
                        if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + 'match, parent_key_path: ' + parent_key_path)
                        if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1620 type(ListOrDict_parent_Python_data_structure) = " + str(type(ListOrDict_parent_Python_data_structure)))
                        if ListOrDict_parent_Python_data_structure is None:
                            ListOrDict_parent_Python_data_structure = []
                        elif 'dict' in str(type(ListOrDict_parent_Python_data_structure)).lower():
                            if len(ListOrDict_parent_Python_data_structure) == 0:
                                ListOrDict_parent_Python_data_structure = []

                            # if len(ListOrDict_parent_Python_data_structure) > 0:
                            #    reportError("Cannot convert ListOrDict_parent_Python_data_structure from a dict to a list.  It already contains " + str(len(ListOrDict_parent_Python_data_structure)) + " elements.")
                            #    for key, value in dict.items(ListOrDict_parent_Python_data_structure):
                            #       print "key="+str(key)+", value="+str(value)
                            # sys.exit(1)

                    if 'list' in str(type(ListOrDict_parent_Python_data_structure)):
                        # if ListOrDict_parent_Python_data_structure is None:
                        #    ListOrDict_parent_Python_data_structure = []
                        if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1692 ListOrDict_parent_Python_data_structure.append([" + ListOrDict_child_xml.tag + ", " + str(temp_Python_data_structure) + "])")
                        if ListOrDict_parent_Python_data_structure is None:
                            ListOrDict_parent_Python_data_structure = []
                        ListOrDict_parent_Python_data_structure.append([ListOrDict_child_xml.tag, temp_Python_data_structure])

                    elif 'dict' in str(type(ListOrDict_parent_Python_data_structure)).lower():
                        # if ListOrDict_parent_Python_data_structure is None:
                        #    ListOrDict_parent_Python_data_structure = collections.OrderedDict()  # OrderedDict so Portfolio_version field stays at top of the tree.
                        if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1697 ListOrDict_parent_Python_data_structure[" + ListOrDict_child_xml.tag + "] = " + str(temp_Python_data_structure))
                        if ListOrDict_parent_Python_data_structure is None:
                            ListOrDict_parent_Python_data_structure = collections.OrderedDict()  # OrderedDict so Portfolio_version field stays at top of the tree.
                        ListOrDict_parent_Python_data_structure[ListOrDict_child_xml.tag] = temp_Python_data_structure

                    if '2' in get_option('--debug', ''): printout(phase[0] + ' ' + "1674 type(ListOrDict_parent_Python_data_structure) = " + str(type(ListOrDict_parent_Python_data_structure)))

                    if '2' in get_option('--debug', ''):
                        if 'cost_basis' in parent_key_path:
                            printout(phase[0] + ' ' + '1656 cost_basis: ', parent_key_path)
                            import pprint
                            pprint.pprint(ListOrDict_parent_Python_data_structure)


                    '''
                    if ListOrDict_parent_xml_data_type == 'list':  # current is list
                       if ListOrDict_parent_Python_data_structure is None:
                          ListOrDict_parent_Python_data_structure = []
                       if ListOrDict_parent_xml.tag == "Investment":
                          ListOrDict_parent_Python_data_structure.append([ListOrDict_parent_xml.tag, Investment(temp_Python_data_structure)])
                       else:
                          ListOrDict_parent_Python_data_structure.append([ListOrDict_parent_xml.tag, temp_Python_data_structure])
                       # print "ListOrDict_parent_Python_data_structure[" + ListOrDict_parent_xml.tag + "] = " + str(ListOrDict_parent_Python_data_structure[ListOrDict_parent_xml.tag])
                    else:  # dict
                       if ListOrDict_parent_Python_data_structure is None:
                          ListOrDict_parent_Python_data_structure = collections.OrderedDict()  # OrderedDict so Portfolio_version field stays at top of the tree.
                       if ListOrDict_parent_xml.tag == "Investment":
                          ListOrDict_parent_Python_data_structure[ListOrDict_parent_xml.tag] = Investment(temp_Python_data_structure)
                       else:
                          ListOrDict_parent_Python_data_structure[ListOrDict_parent_xml.tag] = temp_Python_data_structure
                    '''


            if top == True:
                self._python_data_tree = ListOrDict_parent_Python_data_structure

                # Identify all lists and change all equivalent dicts into one-row lists.
                # dont_care, list_of_list_parent_key_paths = traverse_Python_data_tree(command="find_lists", indent=True, key="top", Python_data_tree=self._python_data_tree, line_break_char='', list_of_list_parent_key_paths=[])

                # for row in list_of_list_parent_key_paths:
                #    print row

                # if '2' in get_option('--debug', ''): print "1691 type(ListOrDict_parent_Python_data_structure) = " + str(type(ListOrDict_parent_Python_data_structure))
                #
                # import pprint
                # pprint.pprint(ListOrDict_parent_Python_data_structure)

                # Reset for the next phase
                ListOrDict_child_xml_data_structure = None

        return 0, ListOrDict_parent_Python_data_structure, list_of_list_parent_key_paths


    #==============================

    def show_Python_data_tree(self):
        printout('''
  ------------------------------
  TBD: This feature needs work based on this slightly revised hierarchy:

  top:{
     Investments:[
        { Investment:
          { status:active,

  tree['top']['Investments'][3]['Investment']['status']
  ------------------------------

  Real tree:

  ''') 

        dont_care, output_pdt = traverse_Python_data_tree(command="output", indent=True, key="top", Python_data_tree=self._python_data_tree, line_break_char='')
        for row in output_pdt:
           printout(row['full_entry'])

        # # pprint does not handle pointers to Investment instances.
        # # Strange, it works now.
        # import pprint
        # # pprint.pprint(self._python_data_tree)  # DOES NOT WORK FOR OrderedDicts.
        # 
        # pprint.pprint(self._python_data_tree.items())


        # Does not work.
        # print dir(self._python_data_tree)

        # Does not work.
        # print self._python_data_tree.__dict__

        # Does not work.
        # logging_wrappers.dump_obj_type(self._python_data_tree, indent='')


    #==============================

    def show_investments_table(self, show_purchase_lots=False):
        ac_investments = {}

        # Sort the asset class sections alphabetically.

        inv_totals = { \
           'count': 0, \
           'lot_count': 0, \
           'curr_total_value': Money(), \
           'cb_total_value': Money(), \
           'cb_gain_loss': Money(), \
           }
        result = self.get_Investments_list()
        for row in result:
            ac_name = row.get_value("asset_class")
            if ac_name not in ac_investments:
                ac_investments[ac_name] = []

            # print "1230", row.get_value('file_line_num')
            # print "1231", row.get_value('cost_basis:cb_event:cb_total_value')
            cb_event_list = row.get_value('cost_basis')
            # print cb_event_list
            # print type(cb_event_list)
            # import pprint
            # pprint.pprint(cb_event_list)

            if show_purchase_lots == True:
                cb_event_list_filtered = []
                for cb_event in cb_event_list:
                    if cb_event[1]['cb_event_type'] == 'purchase':
                        cb_event_list_filtered.append(cb_event[1])
                cb_event_list_sorted = sorted(cb_event_list_filtered, key=itemgetter('cb_date'))
                # cb_event_list_sorted = sorted(cb_event_list_filtered, key=lambda k: k[1]['cb_date'])

                for cb_event_dict in cb_event_list_sorted:
                    gain_loss_amount = Money().set_by_string(row.get_value('curr_total_value').__str__()).sub(Money().set_by_string(cb_event_dict['cb_total_value'].__str__()))
                    gain_loss_str = gain_loss_amount.__str__()
                    g_l_percent = gain_loss_amount.percent(cb_event_dict['cb_total_value'])

                    # common_dict = common_columns(data_row=row)[1]
                    #
                    # print "common_dict before", common_dict
                    # print "1911", common_dict.update({'curr_total_value':row.get_value("curr_total_value"), 'cb_date':cb_event_dict['cb_date'], 'cb_quantity':cb_event_dict['cb_quantity'], 'cb_share_price':cb_event_dict['cb_share_price'], 'cb_total_value': cb_event_dict['cb_total_value'], 'gain_loss':gain_loss_str, 'g_l_percent': g_l_percent})
                    # ac_investments[ac_name].append(dict(common_dict.items() + {'curr_total_value':row.get_value("curr_total_value"), 'cb_date':cb_event_dict['cb_date'], 'cb_quantity':cb_event_dict['cb_quantity'], 'cb_share_price':cb_event_dict['cb_share_price'], 'cb_total_value': cb_event_dict['cb_total_value'], 'gain_loss':gain_loss_str, 'g_l_percent': g_l_percent}.items()))
                    ac_investments[ac_name].append(dict(list(common_columns(data_row=row)[1].items()) + list({'curr_total_value':row.get_value("curr_total_value"), 'cb_date':cb_event_dict['cb_date'], 'cb_quantity':cb_event_dict['cb_quantity'], 'cb_share_price':cb_event_dict['cb_share_price'], 'cb_total_value': cb_event_dict['cb_total_value'], 'gain_loss':gain_loss_str, 'g_l_percent': g_l_percent}.items())))
                    # print "1912", ac_investments[ac_name]
                    # print "common_dict after", common_dict

                    inv_totals['count'] += 1
                    inv_totals['curr_total_value'].add(row.get_value("curr_total_value"))
                    inv_totals['cb_total_value'].add(cb_event_dict["cb_total_value"])
                    inv_totals['cb_gain_loss'].add(gain_loss_amount)

            # print "1919", ac_investments
            # for key, value in dict.items(ac_investments):
            #    print key, value
            #    for entry in ac_investments[key]:
            #       print entry

            if show_purchase_lots == False:
                lot_count = 0
                cb_total_value = Money()
                for cb_event in cb_event_list:
                    if cb_event[1]['cb_event_type'] == 'purchase':
                        lot_count += 1
                        cb_total_value.add(cb_event[1]['cb_total_value'])

                gain_loss_amount = Money().set_by_string(row.get_value('curr_total_value').__str__()).sub(Money().set_by_string(cb_total_value.__str__()))
                gain_loss_str = gain_loss_amount.__str__()
                g_l_percent = gain_loss_amount.percent(cb_total_value)

                ac_investments[ac_name].append(dict(list(common_columns(data_row=row)[1].items())+list({'lot_count':lot_count, 'curr_total_value':row.get_value("curr_total_value"), 'cb_total_value': cb_total_value, 'gain_loss':gain_loss_str, 'g_l_percent': g_l_percent}.items())))
                inv_totals['count'] += 1
                inv_totals['lot_count'] += lot_count
                inv_totals['curr_total_value'].add(row.get_value("curr_total_value"))
                inv_totals['cb_total_value'].add(cb_event[1]["cb_total_value"])
                inv_totals['cb_gain_loss'].add(gain_loss_amount)

                # print row.get_ID()
                # print row.__str__()

        inv_list_sorted_by_ac = sorted(list(ac_investments.items()), key=itemgetter(0))

        # Sort the entries alphabetically in each asset class section

        if show_purchase_lots == True:
            col_headers = common_columns()[0]+['Curr_Tot', 'CB_Date', 'CB_Qty', 'CB_ShPr', 'CB_Tot', 'GainLoss', 'GL_%']
        else:
            col_headers = common_columns()[0]+['Lot', 'Curr_Tot', 'CB_Tot', 'GainLoss', 'GL_%']
        inv_list_fully_sorted = []
        inv_list_fully_sorted.append(col_headers)
        # for row in inv_list_sorted_by_ac:
        #    print "1947", row
        for row in inv_list_sorted_by_ac:
            inv_list_fully_sorted.append(['---'+row[0]+'---', '', '', '', '', '', '', '', '', '', '', '', ''])
            asset_list = []
            for asset_row in row[1]:
                if show_purchase_lots == True:
                    asset_list.append(common_columns(asset_row=asset_row)[2]+[asset_row['curr_total_value'], asset_row['cb_date'], asset_row['cb_quantity'], asset_row['cb_share_price'], asset_row['cb_total_value'], asset_row['gain_loss'], "%1.2f" % asset_row['g_l_percent']])
                else:
                    asset_list.append(common_columns(asset_row=asset_row)[2]+[asset_row['lot_count'], asset_row['curr_total_value'], asset_row['cb_total_value'], asset_row['gain_loss'], "%1.2f" % asset_row['g_l_percent']])
                '''
                inv_totals['count'] += 1
                inv_totals['curr_total_value'].add(asset_row['curr_total_value'])
                inv_totals['cb_total_value'].add(asset_row['cb_total_value'])
                inv_totals['gain_loss'].add(asset_row['gain_loss'])
                '''

            asset_list_sorted = sorted(asset_list, key=itemgetter(0))
            inv_list_fully_sorted += asset_list_sorted

        inv_list_fully_sorted.append(['---Totals---', '', '', '', '', '', '', '', '', '', '', '', ''])
        totals_row = []
        for header in col_headers:
            if header == 'Asset':
                totals_row.append(inv_totals['count'])
            elif header == 'LotCount':
                totals_row.append(inv_totals['lot_count'])
            elif header == 'Curr_Tot':
                totals_row.append(inv_totals['curr_total_value'])
            elif header == 'CB_Tot':
                totals_row.append(inv_totals['cb_total_value'])
            elif header == 'GainLoss':
                totals_row.append(inv_totals['cb_gain_loss'])
            else:
                totals_row.append('')
        inv_list_fully_sorted.append(totals_row)

        if show_purchase_lots == True:
            filename = output_file_prefix + "lots_table"
        else:
            filename = output_file_prefix + "inv_table"

        create_output_files(filename, input_data=inv_list_fully_sorted)

        return 0



# class functions above
#===================================================================================

def create_output_files(filename, input_data, silent_option=False):
    global processing_message

    if '1' in get_option('--debug', ''): printout("Entering create_output_files")

    # for row in input_data: print row
    rc, results = columnize_output(input_data=input_data, justify_cols='L,R', save_filename=filename)
    if rc != 0:
        reportWarning("Non-zero status from columnize_output()")

    inv_list_columnized = results

    # for row in inv_list_columnized:
    #    print row

    text_to_insert = "\n" + processing_message + '\n' + "-" * len(inv_list_columnized[0])
    fd_output = open(filename + ".txt.new", "w")
    fd_output.write(text_to_insert + '\n')
    for line in open(filename + ".txt", "r").read().splitlines():
        fd_output.write(line + '\n')
    fd_output.close()
    os.rename(filename + ".txt.new", filename + ".txt")

    # print(2742,  silent_option, processing_message)
    if silent_option == False:
        if len(inv_list_columnized) > 0:
            printout(text_to_insert)
            for row in inv_list_columnized: printout(row)

    rc, html_table_string = csv2html.csv2html(list_of_objects=input_data, num_header_lines_from_top=1)
    html_table_string = '<br>' + processing_message + '\n' + html_table_string
    with open(filename + ".html", 'w') as fd:
        fd.write(html_table_string)
    if all_table_files is not None:
        all_table_files.append(filename)
    processing_message = ''

    return 0, input_data, inv_list_columnized


#==============================

ac_from_web = {}

def get_asset_class_names_from_web(symbols_csv_string):
    rc, results = get_stock_asset_class(symbols_csv_string)
    if rc != 0:
        return rc, reportError("ERROR in get_stock_asset_class.  results: " + results, mode='return_msg_only')
    # print(2744, results)
    for line in results.split('\n'):
        if 'threadname:' in line:
            continue
        if line == '':
            continue
        symbol_from_web, ac_web_name = line.split(':', 1)
        if ac_web_name == 'null':
            ac_from_web[symbol_from_web] = 'Individual_Stocks'
        else:
            ac_from_web[symbol_from_web] = ac_web_name
        # print 2760, symbol_from_web, ac_web_name

    return 0, ac_from_web

#==============================

# These functions need debugging.

# Use the indentation in the fields in xml_string to determine nesting.

def sort_nested_list(xml_string='', index=-1):
    list_to_sort = []
    curr_indent = 'not_set_yet'
    xml_list = xml_string.split('\n')
    while True:
        index += 1
        if index >= len(xml_list): break
        printout(xml_list[index], index)
        if xml_list[index] == '':
            continue
        found = re.search('^( *)[^]', xml_list[index])
        if not found:
            reportError("Cannot find indentation.  field:" + xml_list[index])
            sys.exit(1)
        field_indent = found.group(1)
        if curr_indent == 'not_set_yet':
            printout("curr", "not_set_yet", "new", len(field_indent))
            curr_indent = field_indent
            printout("2022: list_to_sort", xml_list[index])
            list_to_sort.append([xml_list[index], ''])
            continue

        printout("curr", len(curr_indent), "new", len(field_indent))
        if len(field_indent) == len(curr_indent):
            printout("2028: list_to_sort", xml_list[index])
            list_to_sort.append([xml_list[index], ''])
        elif len(field_indent) > len(curr_indent):
            curr_indent = field_indent
            printout("2031: list_to_sort", xml_list[index])
            list_to_sort.append([xml_list[index], ''])
            index, new_sorted_sub_list = sort_nested_list(xml_string=xml_string, index=index)
            list_to_sort[-1][1] = new_sorted_sub_list
            printout("2034: list_to_sort", xml_list[index])
            list_to_sort.append([xml_list[index], ''])
        else:  # len(field_indent) < len(curr_indent):
            break

    sorted_list = sorted(list_to_sort, key=itemgetter(0))

    return index, sorted_list


def convert_nested_xml_list_to_xml_string(xml_sorted_list):
    xml_string = ''
    for entry in xml_sorted_list:
        xml_string += entry[0] + '\n'
        if 'list' in str(type(entry[1])):
            xml_string += convert_nested_xml_list_to_xml_string(entry[1])

    return xml_string


#==============================

def common_columns(data_row=None, asset_row=None):
    col_headers = ['Asset', 'Symb', 'Own', 'iID', 'Account_ID', 'Ret_Class']
    data_row_list = None
    if data_row is not None:
        data_row_list = {'Name':data_row.get_value("name_short"), 'symbol':data_row.get_value("symbol"), 'owner':data_row.get_value('owner_short'), 'inv_ID':data_row.get_value("inv_ID"), 'account_ID':data_row.get_value("account_ID"), 'retirement_class_short':data_row.get_value("retirement_class_short")}
    asset_row_list = None
    if asset_row is not None:
        asset_row_list = [asset_row['Name'], asset_row['symbol'], asset_row['owner'], asset_row['inv_ID'], asset_row['account_ID'], asset_row['retirement_class_short']]
    return col_headers, data_row_list, asset_row_list

#====================================================

def diff_investments_tables(investment_list1, investment_list2):

    investments = {}

    inv_list2 = investment_list2.get_Investments_list() # Grab one copy of list2 to save time in loops that follow.

    for row in investment_list1.get_Investments_list():
        ac_name = row.get_value("asset_class")
        if ac_name not in investments:
            investments[ac_name] = []

        for row2 in inv_list2:
            if row.get_value("inv_ID") == row2.get_value("inv_ID"):
                diff_Money = Money(row2.get_value("curr_total_value")).sub(Money(row.get_value("curr_total_value")))
                # print(2795, diff_Money.get_cents())
                investments[ac_name].append(dict(list(common_columns(data_row=row)[1].items()) + list({'curr_total_value1':row.get_value("curr_total_value"), 'curr_total_value2':row2.get_value("curr_total_value"), 'sp1':row.get_value('curr_share_price'), 'sp2':row2.get_value('curr_share_price'), 'diff':diff_Money}.items())))
                break

    inv_list_sorted_by_ac = sorted(list(investments.items()), key=itemgetter(0))

    inv_list_fully_sorted = []
    inv_list_fully_sorted.append(common_columns()[0] + ['Curr_Tot1', 'Curr_Tot2', 'ShPr1', 'ShPr2', 'Diff', 'Diff%'])
    inv_totals = { \
       'count': 0, \
       'curr_total_value1': Money(), \
       'curr_total_value2': Money(), \
       'diff': Money(), \
       'count_positive': 0, \
       'count_negative': 0, \
       'count_neutral': 0, \
       'diff_percent': 0.0, \
       }
    for row in inv_list_sorted_by_ac:
        inv_list_fully_sorted.append(['---'+row[0]+'---', '', '', '', '', '', '', '', '', '', ''])
        asset_list = []
        for asset_row in row[1]:
            # if '2' in get_option('--debug', ''): printout(2829, asset_row)
            # print(2829, asset_row['diff'].get_cents())
            diff_percent = Money(asset_row['diff'].get_cents()).percent(asset_row['curr_total_value1'])
            # print(2818, Money(asset_row['diff']).get_cents(), asset_row['curr_total_value1'])
            # print(2829, diff_percent)
            asset_list.append(common_columns(asset_row=asset_row)[2]+[asset_row['curr_total_value1'], asset_row['curr_total_value2'], asset_row['sp1'], asset_row['sp2'], asset_row['diff'], diff_percent])
            inv_totals['count'] += 1
            inv_totals['curr_total_value1'].add(asset_row['curr_total_value1'])
            inv_totals['curr_total_value2'].add(asset_row['curr_total_value2'])
            inv_totals['diff'].add(asset_row['diff'])
            # if '2' in get_option('--debug', ''): printout(2824, inv_totals['diff'].get_cents())
            if asset_row['diff'].get_cents() > 0:
                inv_totals['count_positive'] += 1
            elif asset_row['diff'].get_cents() < 0:
                inv_totals['count_negative'] += 1
            else:
                inv_totals['count_neutral'] += 1
            inv_totals['diff_percent'] += diff_percent
        asset_list_sorted = sorted(asset_list, key=itemgetter(0))
        inv_list_fully_sorted += asset_list_sorted

    inv_list_fully_sorted.append(['---Stats---', '', '', '', '', '', '', '', '', '', ''])
    stats_row = [ \
          'Totals', \
          inv_totals['count'], \
          '', \
          '', \
          '', \
          '', \
          inv_totals['curr_total_value1'], \
          inv_totals['curr_total_value2'], \
          '', \
          '', \
          inv_totals['diff'], \
          '', \
         ]
    inv_list_fully_sorted.append(stats_row)

    stats_row = [ \
          'Totals diff percent', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          inv_totals['diff'].percent(inv_totals['curr_total_value1']), \
         ]
    inv_list_fully_sorted.append(stats_row)

    stats_row = [ \
          'Avg diff percent', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          "%02.2f" % (float(inv_totals['diff_percent']) / float(inv_totals['count'])), \
         ]
    inv_list_fully_sorted.append(stats_row)

    stats_row = [ \
          'Count pos diff percent', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          inv_totals['count_positive'], \
         ]
    inv_list_fully_sorted.append(stats_row)

    stats_row = [ \
          'Count neg diff percent', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          inv_totals['count_negative'], \
         ]
    inv_list_fully_sorted.append(stats_row)

    stats_row = [ \
          'Count neutral diff percent', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          '', \
          inv_totals['count_neutral'], \
         ]
    inv_list_fully_sorted.append(stats_row)

    filename = output_file_prefix + 'inv_diff_table'

    rc, dont_care, inv_list_columnized = create_output_files(filename, input_data=inv_list_fully_sorted)

    return 0, inv_list_fully_sorted, inv_list_columnized


#====================================================

import io
import itertools as IT

PY2 = sys.version_info[0] == 2
StringIO = io.BytesIO if PY2 else io.StringIO

def get_xml_tree(xml_string):
    try:
        tree = ET.ElementTree(ET.fromstring(xml_string))
    except ET.ParseError as err:
        lineno, column = err.position
        line = next(IT.islice(StringIO(xml_string), lineno))
        caret = '{:=>{}}'.format('^', column)
        err.msg = '{}\n{}\n{}'.format(err, line, caret)
        raise
    return tree

#====================================================

def show_Portfolio_xml_file_stats(Portfolio_xml_file):

    # Investment_type = {'Vanguard': 0, 'Fidelity': 0, 'MM_Yahoo': 0, 'Individual_Stocks': 0, 'Unrecognized': 0 }
    Investment_type = {}
    Investment_start = False
    ac_investment_count = 0
    fileline = 0
    for line in open(Portfolio_xml_file, 'r').read().splitlines():
        fileline += 1

        if line == '':
            continue

        if '<Investment>' in line:
            Investment_first_line_num = fileline
            ac_investment_count += 1
            Investment_start = True
            one_Investment = {}
            continue

        if '</Investment>' in line:
            Investment_start = False

            '''
            if 'Yahoo'.lower() in one_Investment['<account_ID>'].lower():
               Investment_type['MM_Yahoo'] += 1
               continue

            if 'Vanguard' in one_Investment['<name>']:
               Investment_type['Vanguard'] += 1
               continue

            if 'Fidelity' in one_Investment['<name>']:
               Investment_type['Fidelity'] += 1
               continue

            if 'Individual_Stocks' in one_Investment['<asset_class>']:
               Investment_type['Individual_Stocks'] += 1
               continue

            reportError("Unrecognized Investment, line num: " + str(Investment_first_line_num))
            Investment_type['Unrecognized'] += 1
            '''

            continue

        if Investment_start == True:
            '''
            found = re.search('^[^<]*(<[^>]+>)', line)
            if found:
               key = found.group(1)
               if key not in one_Investment:
                  one_Investment[key] = line
            '''

            found = re.search('<brokerage>([^<]*)<', line)
            if found:
                key = found.group(1)
                if key not in Investment_type:
                    Investment_type[key] = 1
                else:
                    Investment_type[key] += 1


    output = ''
    output += "ac_investment_count:" + str(ac_investment_count) + '\n'
    output += "Breakdown--" + '\n'
    for key, value in dict.items(Investment_type):
        output += key + ":" + str(value) + '\n'

    return 0, output

#====================================================


all_option_preconfigured = []
all_option_preconfigured.append({'name':'--price_web_update', 'value': ''})
all_option_preconfigured.append({'name':'--ac_web_update', 'value': ''})
all_option_preconfigured.append({'name':'--pt', 'value': "show_percent"})
all_option_preconfigured.append({'name':'--pt', 'value': "show_ac_misc_totals"})
all_option_preconfigured.append({'name':'--inv', 'value': "lots"})
all_option_preconfigured.append({'name':'--inv', 'value': "diff"})


#====================================================

scriptName = os.path.basename(sys.argv[0])

def get_docstring():
    # all_option_preconfigured_string = '            ' + '\n            '.join([key+' '+value for x in all_option_preconfigured for key, value in dict.items(x)])
    all_option_preconfigured_string = '\n            '.join([key+' '+value for x in all_option_preconfigured for key, value in dict.items(x)])
    return __doc__ % {'scriptName': scriptName, 'all_option_preconfigured': all_option_preconfigured_string,}


def usage(exit_or_return='exit'):
    printout(get_docstring())
    if exit_or_return == 'exit':
        sys.exit(1)
    else:
        return

# def get_test_runstrings():
#     test_runstrings = []
#     for line in get_docstring().split('\n'):
#         found = re.search('^ *(' + scriptName + ' +-.+)$', line)
#         if found:
#             test_runstrings.append(found.group(1))
#     return test_runstrings


#===================================================



# Function for processing the  --all   option.

def Portfolio_processing(options_list):

    global Portfolio_xml_filename, Portfolio_xml_filename2
    global price_web_update
    global ac_web_update
    global processing_message

    processing_message_all = "\nProcessing: user_runstring = " + ' '.join(sys.argv) + '\n'
    if get_option('--all', False):
        replace_option('--all', all_option_preconfigured)
        processing_message_all += "\nExpanded to: " + create_options_list_string() + '\n'
    printout(processing_message_all)

    Portfolio_xml_filename  = get_option('--pfile', None)
    if ',' in Portfolio_xml_filename:
        Portfolio_xml_filename, Portfolio_xml_filename2 = get_option('--pfile', None).split(',')
    else:
        Portfolio_xml_filename2 = ''

    if re.search("^\$", Portfolio_xml_filename):  # expand Portfolio_xml_filename environment variable in the command
        env_var = re.sub('^\$', '', Portfolio_xml_filename)
        env_var_value = os.environ.get(env_var)
        if env_var_value == None:
            reportError("Environment variable " + Portfolio_xml_filename + " is not set for command:  " + ' '.join(sys.argv))
            sys.exit(1)
        Portfolio_xml_filename = env_var_value

    if not os.path.isfile(Portfolio_xml_filename):
        reportError("File does not exist: " + Portfolio_xml_filename)
        sys.exit(1)


    if Portfolio_xml_filename2 != '':
        if re.search("^\$", Portfolio_xml_filename2):  # expand any environment variable in the command for the portfolio filename
             env_var = re.sub('^\$', '', Portfolio_xml_filename2)
             env_var_value = os.environ.get(env_var)
             if env_var_value == None:
                 reportError("Environment variable " + Portfolio_xml_filename2 + " is not set for command:  " + ' '.join(sys.argv))
                 sys.exit(1)
             Portfolio_xml_filename2 = env_var_value

        if not os.path.isfile(Portfolio_xml_filename2):
             reportError("Portfolio_xml_file2 does not exist: " + Portfolio_xml_filename2)
             usage()

    Portfolio_xml_file_basename = os.path.basename(Portfolio_xml_filename)
    Portfolio_xml_file_dir = os.path.dirname(Portfolio_xml_filename)
    if Portfolio_xml_file_dir == '':
        Portfolio_xml_file_dir = '.'

    output_file_prefix = Portfolio_xml_file_dir + '/' + Portfolio_xml_file_basename + '_'

    price_web_update = -1  # default = not needed
    ac_web_update = -1  # default = not needed
    created_xml = False
    created_Python_data_tree = False

    silent_option = False

    while True:
        next_option_name, next_option_value = get_next_option()
        if next_option_name == None:
            break

        if next_option_name == '--price_web_update':
            price_web_update = 0  # Needed but not done yet
            continue

        if next_option_name == '--ac_web_update':
            ac_web_update = 0  # Needed but not done yet
            continue

        if next_option_name == '--silent':
            silent_option = True
            continue

        if created_xml == False:
            value = get_option('--inv', False)
            if value == 'diff':
               price_web_update_save = price_web_update
               price_web_update = -1  # For a diff, the first xml file is never web-updated.

            investment_list = Investments()

            # processing_message = processing_message + "Processing: Portfolio_xml_file_to_xml_string()"
            rc, xml_string = investment_list.Portfolio_xml_file_to_xml_string(Portfolio_xml_filename)
            if rc != 0:
                printout(xml_string)
                sys.exit(1)

            if value == 'diff':
                price_web_update = price_web_update_save  # restore prev value

            created_xml = True

        if next_option_name == '--xmlfile':
            processing_message = processing_message + "<comment>" + "Processing: " + str(next_option_name) + ' ' + str(next_option_value) + "</comment>"
            if silent_option == False:
                printout(processing_message)
                processing_message = ''

            # Not pretty enough!  :-)
            # import xml.dom.minidom
            # xml = xml.dom.minidom.parseString(xml_string)
            # pretty_xml_as_string = xml.toprettyxml()
            # print pretty_xml_as_string

            root = etree.fromstring(xml_string)
            printout(etree.tostring(root, pretty_print=True))

            sys.exit(0)

        if created_Python_data_tree == False:
            rc, dont_care, dont_care = investment_list.xml_string_to_Python_data_tree(xml_string=xml_string, ListOrDict_child_xml_data_structure=None)
            if rc != 0:
                reportError("xml_string_to_Python_data_tree error.  rc = " + str(rc))
                sys.exit(1)
            created_Python_data_tree = True

        if next_option_name == '--xml':
            processing_message = processing_message + "<comment>" + "Processing: " + str(next_option_name) + ' ' + str(next_option_value) + "</comment>"
            if silent_option == False:
                printout(processing_message)
                processing_message = ''
            printout(investment_list.xml_from_pdt(indent=(get_option('--noindent', True))))
            sys.exit(0)

        if next_option_name == '--pdt':
            processing_message = processing_message + "\nProcessing: " + str(next_option_name) + ' ' + str(next_option_value)
            if silent_option == False:
                printout(processing_message)
                processing_message = ''
            investment_list.show_Python_data_tree()
            sys.exit(0)

        if next_option_name == '--stats':
            processing_message = processing_message + "\nProcessing: " + str(next_option_name) + ' ' + str(next_option_value)
            if silent_option == False:
                printout(processing_message)
                processing_message = ''
            investment_list.show_stats()
            sys.exit(0)


        if next_option_name == '--pt':
            output = ''
            pt_cmd_lp = ''
            pt_cmd_add = ''
            pt_cmd_show = ''
            ac_totals_sorted_list = None
            sub_options_list = []
            index = -1
            if next_option_value == 'show':
                printout("\n--pt show = --pt show_percent and --pt show_ac_misc_totals")
                sub_options_list.append("show_percent")
            else:
                sub_options_list = next_option_value.split('%')
            if sub_options_list[0] == 'show':
                del sub_options_list[0]
            while True:
                index += 1
                if index >= len(sub_options_list): break
                pt_cmd = sub_options_list[index]
                # print "2432", pt_cmd
                # processing_message = "\nProcessing: --pt " + pt_cmd
                # if silent_option == False:
                #     print(processing_message)
                ac_percents_table_body = ''

                if 'lp' == pt_cmd:
                    pt_cmd_lp = pt_cmd
                    if ac_percents_table_body == '':
                        silent_option_prev = silent_option
                        silent_option = True
                        rc, ac_percents_table_body = investment_list.show_ac_percents_table(pt_cmd_add, ac_totals_sorted_list=ac_percents_table_body, pt_cmd_lp=pt_cmd_lp, pt_cmd_show=pt_cmd_show)
                        silent_option = silent_option_prev
                    rc, ac_percents_table_body = investment_list.show_ac_lp_table(ac_percents_table_body, pt_cmd_lp=pt_cmd_lp)
                    # rc, ac_totals_sorted_list = investment_list.show_ac_lp_table(ac_percents_table_body, pt_cmd_lp=pt_cmd_lp)
                    continue

                if 'lp_diff' == pt_cmd:
                    pt_cmd_lp = pt_cmd
                    if pt_cmd_add == '':
                        reportError("No previous 'add' command done so cannot do an lp_diff.")
                        sys.exit(1)
                    silent_option_prev = silent_option
                    silent_option = True
                    if ac_percents_table_body != None and len(ac_percents_table_body) > 0:
                        ac_percents_table_body_with_add = ac_percents_table_body
                        rc, ac_percents_table_body_no_add = investment_list.show_ac_percents_table(pt_cmd_add='', ac_totals_sorted_list=ac_percents_table_body, pt_cmd_lp=pt_cmd_lp, pt_cmd_show=pt_cmd_show)
                    else:
                        if ac_totals_sorted_list != None and len(ac_totals_sorted_list) > 0:
                            rc, ac_percents_table_body_with_add = investment_list.show_ac_percents_table(pt_cmd_add, ac_totals_sorted_list=ac_percents_table_body, pt_cmd_lp=pt_cmd_lp, pt_cmd_show=pt_cmd_show)
                            ac_totals_sorted_list = None
                            rc, ac_percents_table_body_no_add = investment_list.show_ac_percents_table(pt_cmd_add='', ac_totals_sorted_list=ac_percents_table_body, pt_cmd_lp=pt_cmd_lp, pt_cmd_show=pt_cmd_show)
                        else:
                            reportError("No previous valid ac_totals_sorted_list and ac_percents_table_body available so cannot do an lp_diff.")
                            sys.exit(1)
                    silent_option = silent_option_prev
                    investment_list.show_ac_lp_diff_table(ac_percents_table_body_no_add, ac_percents_table_body_with_add)
                    continue

                if 'add:' in pt_cmd:
                    # pt_cmd_add = pt_cmd.replace('add:', '')
                    pt_cmd_add = pt_cmd

                    processing_message = processing_message + "\nProcessing: " + str(next_option_name) + ' ' + pt_cmd
                    if silent_option == False:
                        printout(processing_message)
                        processing_message = ''

                    ac_totals_sorted_list = investment_list.add_to_investment(pt_cmd_add)
                    continue

                if "show_percent" in pt_cmd:
                    pt_cmd_show = pt_cmd
                    processing_message = processing_message + "\nProcessing: " + str(next_option_name) + ' ' + pt_cmd
                    # if ac_percents_table_body == '':
                    rc, ac_percents_table_body = investment_list.show_ac_percents_table(pt_cmd_add, ac_totals_sorted_list=ac_totals_sorted_list, pt_cmd_lp=pt_cmd_lp, pt_cmd_show=pt_cmd_show)
                    # rc, results = investment_list.show_ac_percents_table(pt_cmd_add, ac_totals_sorted_list=ac_percents_table_body, pt_cmd_lp=pt_cmd_lp, pt_cmd_show=pt_cmd_show)
                    if rc != 0:
                         reportError("show_ac_percents_table() error.  results = " + results)
                         sys.exit(1)
                    break

                if "show_ac_misc_totals" in pt_cmd:
                    # print(3350)
                    # for line in debug_run_status("snapshot"): printout(line)

                    processing_message = processing_message + "\nProcessing: " + str(next_option_name) + ' ' + pt_cmd
                    rc, results = investment_list.show_ac_misc_totals_table(ac_totals_sorted_list)
                    if rc != 0:
                         reportError("show_ac_misc_totals_table() error.  results = " + results)
                         sys.exit(1)
                    # print(3361)
                    # for line in debug_run_status("snapshot"): printout(line)
                    break

                reportError("Unrecognized pt option = " + pt_cmd)
                usage()

            continue

        if next_option_name == '--inv':
            if 'show' in next_option_value:
                processing_message = processing_message + "\nProcessing: --inv show"
                rc = investment_list.show_investments_table(show_purchase_lots=False)
            elif 'lots' in next_option_value:
                processing_message = processing_message + "\nProcessing: --inv lots"
                rc = investment_list.show_investments_table(show_purchase_lots=True)
            elif 'diff' in next_option_value:
                investment_list2 = Investments()

                if Portfolio_xml_filename2 != '':
                    price_web_update = -1
                    # processing_message = processing_message + "Processing: Portfolio_xml_file_to_xml_string()"
                    rc, xml_string = investment_list2.Portfolio_xml_file_to_xml_string(Portfolio_xml_filename2)
                    if rc != 0:
                        reportError("Calling Portfolio_xml_file_to_xml_string(): near line 3211, investment_list2: " + str(xmml_string))
                else:
                    if price_web_update == -1:
                        price_web_update = 0
                    # Portfolio_xml_filename2 = ''
                    # processing_message = processing_message + "Processing: Portfolio_xml_file_to_xml_string()"
                    rc, xml_string = investment_list2.Portfolio_xml_file_to_xml_string(Portfolio_xml_filename)
                    if rc != 0:
                        reportError("Calling Portfolio_xml_file_to_xml_string(): near line 3219, investment_list2: " + str(xmml_string))

                rc, dont_care, dont_care = investment_list2.xml_string_to_Python_data_tree(xml_string=xml_string, ListOrDict_child_xml_data_structure=None)
                if rc != 0:
                    reportError("Calling xml_string_to_Python_data_tree(): near line 3223, investment_list2: " + str(xmml_string))

                processing_message = processing_message + "\nProcessing: --inv diff"
                rc, dont_care, inv_list_columnized = diff_investments_tables(investment_list, investment_list2)

            continue

    if all_table_files is not None:
        filename = output_file_prefix + 'all_table'
        try:
            os.remove(filename + ".html")
        except:
            None
        fd_output = open(filename + ".html", 'a')
        fd_output.write(processing_message_all)
        for html_file in all_table_files:
            fd_input = open(html_file + ".html", 'r')
            for line in fd_input:
                fd_output.write(line)
            fd_input.close()
        fd_output.close()

        try:
            os.remove(filename + ".txt")
        except:
            pass
        fd_output = open(filename + ".txt", 'a')
        fd_output.write(processing_message_all)
        for txt_file in all_table_files:
            fd_input = open(txt_file + ".txt", 'r')
            for line in fd_input:
                fd_output.write(line)
            fd_input.close()
        fd_output.close()

#====================================================

# Similar to your_dict.get('name', default_value) but this works on a list with one dict entry per cell.

def get_option(name, value=None):
    for option in options_list:
        # print(3449, option)
        if option['name'] == name:
            value = option['value']
            break
    return value
   
def get_next_option():
    if len(options_list) == 0:
        return None, None
    name  = options_list[0]['name']
    value = options_list[0]['value']
    del options_list[0]
    return name, value
   
def del_option(name):
    for index in xrange(len(options_list)):
        # print(3449, options_list[index])
        if options_list[index]['name'] == name:
            del options_list[index]
            break
   

def create_options_list_string():
    separator = ''
    options_list_string = ''
    for option in options_list:
        # print(3449, options_list[index])
        if 'str' not in str(type(option['value'])):
            value = ''
        else:
            value = option['value']
        options_list_string += separator + option['name'] + ' ' + value
        separator = ' '
    return options_list_string
   
def replace_option(name, new_options):
    global options_list
    for index in xrange(len(options_list)):
        # print(3449, option)
        if options_list[index]['name'] == name:
            options_list = options_list[:index] + new_options + options_list[index+1:]
            break
   

#====================================================


if __name__ == '__main__':

    command_list.command_list(argv=sys.argv, your_scripts_help_function=[usage, 'return'])

    if len(sys.argv) == 1:
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["h", "stats", "xml", "noindent", "debug=", "unit_test", "xmlfile", "pt=", "inv=", "pdt", "price_web_update", "ac_web_update", "all", "silent", "pfile=", "trace=", "debug_linenum"])
    except getopt.GetoptError as err:
        reportError("Runstring " + str(err))
        usage()

    logging_setup(logMsgPrefix=scriptName, logfilename=scriptName + '.log', loglevel=logging.ERROR)

    options_list = []

    debug = False

    trace_options = {}

    all_table_files = None
    any_option = False

    silent_option = False

    for opt, arg in opts:
        any_option = True
        if opt == "--stats":
            options_list.append({'name':opt, 'value':''})
        elif opt == "--inv":
            options_list.append({'name':opt, 'value':arg})
        elif opt == "--pt":
            options_list.append({'name':opt, 'value':arg})
        elif opt == "--xml":
            options_list.append({'name':opt, 'value':True})
        elif opt == "--xmlfile":
            options_list.append({'name':opt, 'value':True})
        elif opt == "--pdt":
            options_list.append({'name':opt, 'value':True})
        elif opt == "--price_web_update":
            options_list.append({'name':opt, 'value':True})
        elif opt == "--ac_web_update":
            options_list.append({'name':opt, 'value':True})
        elif opt == "--noindent":
            options_list.append({'name':opt, 'value':False})
        elif opt == "--debug":
            # setLoggingLevel(logging.DEBUG)
            options_list.append({'name':opt, 'value':arg})
            debug = True
        elif opt == "--debug_linenum":
            printoutput.printout_format = 1
        elif opt == "--pfile":
            options_list.append({'name':opt, 'value':arg})
        elif opt == "--all":
            all_table_files = []
            options_list.append({'name':opt, 'value':True})
        elif opt == "--silent":
            options_list.append({'name':opt, 'value':True})
        elif opt == "--h":
            usage()
        elif opt == "--trace":
            trace_options['trace_logfile_type'] = 'single_file'
            trace_options['tracePythonLogfileBasename'] = "tracelog"
            trace_options['watch_var_name'] = ''
            trace_options['watch_var_action'] = ''
            for suboption in arg.split(','):
                if 'wa:' in suboption:
                    trace_options['watch_var_name'] = suboption.split(':')[1]
                    trace_options['watch_var_action'] = 'report_all'
                elif 'wc:' in suboption:
                    trace_options['watch_var_name'] = suboption.split(':')[1]
                    trace_options['watch_var_action'] = 'report_changed'
                elif 'f:' in suboption:
                    trace_options['tracePythonLogfileBasename'] = suboption.split(':')[1]
                else:
                    printout("ERROR: Unrecognized suboption = " + suboption)
                    sys.exit(1)
            trace_mi.enableTrace(trace_options)
        elif opt == "--unit_test":
            options_list.append({'name':opt, 'value':True})
        else:
            reportError("Unrecognized runstring option: " + opt)
            usage()

    if any_option == False:
        reportError("Missing required params in runstring.")
        usage()

    value = get_option('--pfile', None)
    if value == None:
       reportError("Missing --pfile Portfolio_xml_filename in runstring.")
       usage()

    # filename = scriptName + '_test_runstrings'
    # fd_output = open(filename + ".txt", "w")
    # for line in get_test_runstrings():
    #     fd_output.write(line + '\n')
    # fd_output.close()

    Portfolio_processing(options_list)

    if len(trace_options) > 0:
        printout()
        printout("TRACE: You enabled trace for this test run.  Refer to logfiles " + trace_options['tracePythonLogfileBasename']+"*.log for the trace events captured.")
        printout()



