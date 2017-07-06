#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, sys, re
from pprint import pprint
import Money
from Investments import Investments
from Investment import Investment
from Money import Money


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

def convert_Vanguard_webpage_to_Investment(inputfile):
    output_list = []

    outputfile = inputfile + '.csv'

    output_fd = open(outputfile, 'w')

    filelines = open(inputfile, "r").read().splitlines()

    list_size = len(filelines)
    # print "list_size = " + str(list_size)

    found_section = False
    fileline_index = -1
    section_title = ''
    new_section_start = 'Registration details|YAHOO'
    section_index = -1
    symbol_start = False
    quantity_list = []
    funds = Investments()
    Yahoo_entries_start = False
    # print "<Comments>"

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
                if "YAHOO" in filelines[fileline_index]:
                    section_title = filelines[fileline_index]
                # print "Section:" + section_title
                # print
            else:
                section_title = filelines[fileline_index]
            continue

        if re.search('^Total', filelines[fileline_index]):
            found_section = False
            section_index = -1
            quantity_list.append("")
            output_fd.write('\n')
            Yahoo_entries_start = False
            continue

        if "YAHOO" in section_title:
            if not Yahoo_entries_start:
                if not re.search('Current balance', filelines[fileline_index]):
                    continue
                fileline_index += 1

            Yahoo_entries_start = True

            found = re.search('^([^        ]+)     ([^     ]+)     ([^     ]+)', filelines[fileline_index])
            if not found:
                print("ERROR: input file line " + str(fileline_index) + ": " + filelines[fileline_index] + ".  Expecting fund name, quantity, share price.")
                sys.exit(1)
            section_index += 1
            symbol = "TBD_symbol"
            name   = found.group(1)
            account_ID = "TBD_account_ID"
            quantity = found.group(2).strip().replace(',','')
            share_price = found.group(3).strip()[1:]
            owner = "Mireille"
            retirement_class = "401K"

        else:
            # print "line2: " + str(fileline_index) + ": " + filelines[fileline_index]
            # if not re.search('Change\s+Current balance|Buy\s+Sell', filelines[fileline_index]):
            # print filelines[fileline_index]
            if not re.search('Current balance|Buy  ', filelines[fileline_index]):
                continue

            if 'Buy        ' in filelines[fileline_index]:
                if 'Total' in filelines[fileline_index+1]:
                    continue

            fileline_index += 1

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

            # details_file = "Vanguard_details/" + symbol + "," + name + "," + account_ID + ".txt"
            # if not os.path.isfile(details_file):
            #    print "WARNING: File does not exist: " + details_file

            quantity = re.sub(',', '', found.group(2))  # remove embedded commas
            # quantity_list.append(quantity)
            share_price = found.group(3)[1:]

            if "Mark T." in section_title and "Mireille" in section_title:
                owner = "Joint"
            elif "Mark T." in section_title:
                owner = "Mark"
            elif "Mireille" in section_title:
                owner = "Mireille"
            else:
                owner = ""

            if owner == "Joint":
                retirement_class = "Non_Retirement"
            else:
                if '—' in section_title:
                    retirement_class = section_title.split('—')[1].strip()
                    if '-' in retirement_class:
                        retirement_class = retirement_class.split('-')[0].strip()

                if retirement_class == "SEP":
                    retirement_class = "SEP IRA"

        investment_total = Money().__set_by_string__(share_price).__mult__(quantity).__str__()

        # output_line = str(section_index) + "," + symbol + "," + name + "," + quantity
        output_line = symbol + "," + name + "," + account_ID + "," + quantity + "," + share_price + "," + investment_total
        # output_list.append(output_line)
        # print "output_line: " + output_line
        output_fd.write(output_line + '\n')

        funds.__add__(Investment(symbol=symbol, name=name, account_ID=account_ID, quantity=quantity, share_price=share_price, owner=owner, retirement_class=retirement_class))

    output_fd.close()

    # print "</Comments>"

    # for row in quantity_list:
    #    print row

    return 0, funds


#========================================================================

if __name__ == '__main__':

    if len(sys.argv) == 1:
        usage()

    rc, funds_list = convert_Vanguard_webpage_to_Investment(sys.argv[1])

    # total = Money(0)

    print(funds_list.__str__())

    print()
    # print "Total investments = " + str(funds_list.__get_num_total__())
    # print
    # print "Total amount = " + str(funds_list.__get_total_amount__())

    funds_list.__show_stats__()

    # for fund in funds_list.__get_list__():
        # print fund.__str__()
        # total.__add__(Money.Money().__set_by_string__(row.split(',')[5]))

    # print "total = " + total.__str__()


'''
8.214 * 52.69 = 432.79566

5269 * 8 = 42152

5269 * (214/1000) = 1127.566

43279.566 =>
'''
