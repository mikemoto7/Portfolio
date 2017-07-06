#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, sys, re
from pprint import pprint
import Money
from Portfolio import Investments
from Portfolio import Investment
from Money import Money


#====================================================

def copy_list(old_list, new_list_name=''):
    new_list = old_list
    new_list._list_name = new_list_name
    return new_list

#====================================================

'''
def update_Master_list(newer_list_file, Master_list_file):

   output_list = []

   # print "Loading " + newer_list_file
   newer_list = Investments("newer_list")
   rc, xml_string = newer_list.__xml_file_to_xml_string__(newer_list_file)
   # print newer_list.__str__()
   # newer_list.__show_stats__()
   rc = newer_list.__xml_string_to_Python_data_tree__(xml_string, None)

   # print "Loading " + Master_list_file
   Master_list = Investments("Master_list")
   Master_list.__xml_file_to_xml_string__(Master_list_file)
   # print Master_list.__str__()
   # Master_list.__show_stats__()
   rc = Master_list.__xml_string_to_Python_data_tree__(xml_string, None)

   error_list = []

   updated_Master_list = copy_list(Master_list, "updated_Master_list")

   return_rc = -1

   for loop in [[newer_list, Master_list], [Master_list, newer_list]]:
      list1 = copy_list(loop[0], loop[0]._list_name)
      list2 = copy_list(loop[1], loop[1]._list_name)

      # print "list2._list_name = " + list2._list_name
      # print "list2._str__() = " + list2.__str__()

      for investment in list1.__get_list__():
         rc = list2._list[0].__valid_format__(investment)
         if rc != 0:
            return_rc = rc
            msg = "ERROR: Format error for newer_list investment = " + investment.__get_ID__()
            print msg
            error_list.append(msg)

         rc, found_index = list2.contains(investment)
         if rc == 1:
            error_list += list2._errors
            return_rc = rc
         elif rc == -1:
            return_rc = 1
            msg = "ERROR: " + list2._list_name + " does not contain " + list1._list_name + " investment = " + investment.__get_ID__()
            # print investment.__str__()
            # print investment.__get_ID__()
            print "<errors>"
            print msg
            print "</errors>"
            error_list.append(msg)
         else:  # rc == 0
            if list2._list_name == Master_list._list_name:
               updated_Master_list._list[found_index].set_value("quantity", investment.get_value("quantity").replace(',',''))
               updated_Master_list._list[found_index].set_value("share_price", investment.get_value("share_price"))
               updated_Master_list._list[found_index].set_value("filename", investment.get_value("filename"))
               updated_Master_list._list[found_index].set_value("file_line_num", investment.get_value("file_line_num"))

   if return_rc == -1:
      return_rc = 0


   return return_rc, [error_list, updated_Master_list]
'''

#========================================================================

def Vanguard_update_Master_list(newer_list_file, Master_list_file):

    output_list = []

    # print "Loading " + newer_list_file

    for line in open(newer_list_file, 'r').read().splitlines():
        if line == '':
            continue


    newer_list = Investments("newer_list")
    rc, xml_string = newer_list.__xml_file_to_xml_string__(newer_list_file)
    # print newer_list.__str__()
    # newer_list.__show_stats__()
    rc = newer_list.__xml_string_to_Python_data_tree__(xml_string, None)

    # print "Loading " + Master_list_file
    Master_list = Investments("Master_list")
    Master_list.__xml_file_to_xml_string__(Master_list_file)
    # print Master_list.__str__()
    # Master_list.__show_stats__()
    rc = Master_list.__xml_string_to_Python_data_tree__(xml_string, None)

    error_list = []

    updated_Master_list = copy_list(Master_list, "updated_Master_list")

    return_rc = -1

    for loop in [[newer_list, Master_list], [Master_list, newer_list]]:
        list1 = copy_list(loop[0], loop[0]._list_name)
        list2 = copy_list(loop[1], loop[1]._list_name)

        # print "list2._list_name = " + list2._list_name
        # print "list2._str__() = " + list2.__str__()

        for investment in list1.__get_list__():
            rc = list2._list[0].__valid_format__(investment)
            if rc != 0:
                return_rc = rc
                msg = "ERROR: Format error for newer_list investment = " + investment.__get_ID__()
                print msg
                error_list.append(msg)

            rc, found_index = list2.contains(investment)
            if rc == 1:
                error_list += list2._errors
                return_rc = rc
            elif rc == -1:
                return_rc = 1
                msg = "ERROR: " + list2._list_name + " does not contain " + list1._list_name + " investment = " + investment.get_ID()
                # print investment.__str__()
                # print investment.get_ID()
                print "<errors>"
                print msg
                print "</errors>"
                error_list.append(msg)
            else:  # rc == 0
                if list2._list_name == Master_list._list_name:
                    updated_Master_list._list[found_index].set_value("quantity", investment.get_value("quantity").replace(',',''))
                    updated_Master_list._list[found_index].set_value("share_price", investment.get_value("share_price"))
                    updated_Master_list._list[found_index].set_value("filename", investment.get_value("filename"))
                    updated_Master_list._list[found_index].set_value("file_line_num", investment.get_value("file_line_num"))

    if return_rc == -1:
        return_rc = 0


    return return_rc, [error_list, updated_Master_list]


#========================================================================

scriptName = os.path.basename(os.path.abspath(sys.argv[0])).replace('.pyc', '.py')


def usage():

    print ""
    print "Runstring:"
    print scriptName + " temp_Vanguard_screencopy_Master_file  Master_file"
    print ""
    print "Manually screen-copy our Vanguard accounts page into a text file and then run this script on the text file to get updated share quantities, prices, and cost basis."
    print ""
    sys.exit(1)

#========================================================================

if __name__ == '__main__':

    if len(sys.argv) == 1:
        usage()

    error_list = []

    print "<Investments>"
    print

    rc, results = Vanguard_update_Master_list(sys.argv[1], sys.argv[2])
    # print "rc = " + str(rc)
    error_list = results[0]
    updated_Master_list = copy_list(results[1], "updated_Master_list")

    print updated_Master_list.__str__()

    updated_Master_list.show_stats()
    error_list += updated_Master_list._errors

    print
    if len(error_list) > 0:
        print "<errors>"
        for line in results[0]:
            print line
        print "</errors>"

    print
    print "</Investments>"
