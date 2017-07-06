#!/usr/bin/env python

import os, sys, re
from pprint import pprint
import Money


#========================================================================

scriptName = os.path.basename(os.path.abspath(sys.argv[0])).replace('.pyc', '.py')


def usage():

    print("")
    print("Runstring:")
    print(scriptName + " Vanguard_screen_copy_text_file")
    print("")
    print("Manually screen-copy our Vanguard accounts page into a text file and then run this script on the text file to get updated share quantities and prices.")
    print("")
    sys.exit(1)

#========================================================================

def extract_Vanguard_info(inputfile):
    output_list = []

    outputfile = inputfile + '.csv'

    output_fd = open(outputfile, 'w')

    filelines = open(inputfile, "r").read().splitlines()

    list_size = len(filelines)
    # print "list_size = " + str(list_size)

    found_section = False

    fileline_index = -1
    section_title = ''
    new_section_start = 'Registration details'
    section_index = -1
    symbol_start = False
    quantity_list = []

    while True:
        # print "fileline_index = " + str(fileline_index) +  " .  list_size = " + str(list_size)
        # print "line  = " + filelines[fileline_index]
        fileline_index += 1
        if fileline_index >= list_size:
            break

        if re.search('Add another Vanguard account', filelines[fileline_index]):
            break
        if re.search('^\s*$', filelines[fileline_index]):
            continue

        # print "line: " + str(fileline_index) + ", list_size = " + str(list_size)
        # print "line: " + str(fileline_index) + ": " + filelines[fileline_index]
        # print "found_section = " + str(found_section)
        if found_section == False:
            if re.search(new_section_start, filelines[fileline_index]):
                found_section = True
                section_index += 1
                print("Section:" + section_title)
            else:
                section_title = filelines[fileline_index]
            continue

        # print "line2: " + str(fileline_index) + ": " + filelines[fileline_index]
        if not re.search('Change\s+Current balance|Buy\s+Sell', filelines[fileline_index]):
            continue
        # print "after"

        fileline_index += 1

        if re.search('^Total', filelines[fileline_index]):
            found_section = False
            section_index = -1
            quantity_list.append("")
            print()
            output_fd.write('\n')
            continue

        found = re.search('^(\S+)\s+(.+)$', filelines[fileline_index])
        if not found:
            print("ERROR: input file line " + str(fileline_index) + ": " + filelines[fileline_index] + ".  Expecting stock symbol and name.")
            sys.exit(1)
        section_index += 1
        symbol = found.group(1)
        name   = found.group(2).strip()
        fileline_index += 1
        # found = re.search('^\s+\S+\s+\S+\s+(\S+)\s+', filelines[fileline_index])
        # found = re.search('%\s+\S+\s+(\S+)\s+', filelines[fileline_index])
        # print "line3: " + filelines[fileline_index]
        found = re.search('^\s+\S+\s+(\S+)\s+(\S+)\s+(\S+)\s+', filelines[fileline_index])
        if not found:
            print("ERROR: input file quantity line " + str(fileline_index) + ": " + filelines[fileline_index] + ".  Expecting stock quantity.")
            sys.exit(1)
        account_ID = found.group(1)

        details_file = "Vanguard_details/" + symbol + "," + name + "," + account_ID + ".txt"
        if not os.path.isfile(details_file):
            print("WARNING: File does not exist: " + details_file)

        quantity = re.sub(',', '', found.group(2))  # remove embedded commas
        # quantity_list.append(quantity)
        share_price = found.group(3)[1:]

        investment_total = Money.Money().__set_by_string__(share_price).__mult__(quantity).__str__()

        # output_line = str(section_index) + "," + symbol + "," + name + "," + quantity
        output_line = symbol + "," + name + "," + account_ID + "," + quantity + "," + share_price + "," + investment_total
        output_list.append(output_line)
        # print "output_line: " + output_line
        output_fd.write(output_line + '\n')

    output_fd.close()

    # for row in quantity_list:
    #    print row

    return 0, output_list


#========================================================================

if __name__ == '__main__':

    if len(sys.argv) == 1:
        usage()

    rc, output_list = extract_Vanguard_info(sys.argv[1])

    total = Money.Money(0)

    for row in output_list:
        print(row)
        total.__add__(Money.Money().__set_by_string__(row.split(',')[5]))

    print("total = " + total.__str__())


'''
8.214 * 52.69 = 432.79566

5269 * 8 = 42152

5269 * (214/1000) = 1127.566

43279.566 =>
'''
