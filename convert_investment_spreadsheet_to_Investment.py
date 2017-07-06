#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, sys, re
from pprint import pprint
import Money
from Investments import Investments
from Investment import Investment
from Money import Money
from get_csv import get_csv


#========================================================================

scriptName = os.path.basename(os.path.abspath(sys.argv[0])).replace('.pyc', '.py')


def usage():

    print("")
    print("Runstring:")
    print(scriptName + " investment_spreadsheet_text_file")
    print("")
    print("'Save As' investment spreadsheet into a text file and then run this script on the text file to get updated share quantities and prices.")
    print("")
    sys.exit(1)

#========================================================================

error_list = []

def convert_investment_spreadsheet_to_Investment(inputfile):

    output_list = []

    outputfile = inputfile + '.csv'

    output_fd = open(outputfile, 'w')

    # filelines = open(inputfile, "r").readlines()
    filelines = open(inputfile, "r").read().splitlines()

    list_size = len(filelines)
    # print "list_size = " + str(list_size)

    # Get price per share
    start_capturing = False
    share_prices = {}
    for line in filelines:
        if 'Current Last Price' in line:
            start_capturing = True
            continue
        if start_capturing == True:
            key, price = line.split(',')[:2]
            # print key, price
            if key == '':
                break
            share_prices[key] = price.replace('$', '')

    '''
    found_section = False
    section_title = ''
    new_section_start = 'Registration details|YAHOO'
    section_index = -1
    symbol_start = False
    quantity_list = []
    Yahoo_entries_start = False
    # print "<Comments>"
    '''

    funds = Investments()
    fileline_index = -1
    retirement_class = "TBD_retirement_class"
    owner = "TBD_owner"
    broken_line = ''
    ignore_lines = False
    one_time_retirement_class = ''

    while True:
        # print "fileline_index = " + str(fileline_index) +  " .  list_size = " + str(list_size)
        # print "line  = " + filelines[fileline_index]
        fileline_index += 1
        if fileline_index >= list_size:
            break

        # filelines[fileline_index] = re.sub('^"', '', filelines[fileline_index])

        if re.search('^Non-Retirement Assets', filelines[fileline_index]):
            retirement_class = "Non_Retirement"
            continue

        if re.search('^Retirement Assets', filelines[fileline_index]):
            retirement_class = "Retirement"
            ignore_lines = True
            continue

        if re.search('^Name of Investment', filelines[fileline_index]):
            ignore_lines = False
            continue

        if ignore_lines:
            continue

        if retirement_class == "TBD_retirement_class":
            continue

        '''
        # if not re.search(",,,,,,,,,,,,", filelines[fileline_index]):
        # if not re.search("\$", filelines[fileline_index]):
        # print "temp = " + temp
        # print "line = " + filelines[fileline_index]
        # if not re.search("\$", filelines[fileline_index]):
        # if not re.search("\r", filelines[fileline_index]):
        temp = filelines[fileline_index]
        temp = temp.rstrip()
        if temp == filelines[fileline_index]: # line missing end ^M
        '''
        if not re.search(",,,,,,,$", filelines[fileline_index]):
            broken_line += filelines[fileline_index]
            # print "broken_line = " + broken_line
            continue
        else:  # line ends with ^M
            if broken_line != '':
                broken_line += filelines[fileline_index]
                filelines[fileline_index] = broken_line
                # print "broken_line = " + broken_line
                broken_line = ''
            # else:  # regular single line ending with ^M

        if re.search('^,,,,,,,,,,,,', filelines[fileline_index]):
            continue

        found = re.search("^([^ ]+?[- ]IRA),,,,,", filelines[fileline_index])
        if found:
            retirement_class = found.group(1)
            one_time_retirement_class = ''
            continue

        found = re.search("^.+?(Traditional[- ]IRA)[^,]*,", filelines[fileline_index], re.IGNORECASE)
        if found:
            one_time_retirement_class = found.group(1)

        found = re.search("^.+?(Traditional[- ]401K)[^,]*,", filelines[fileline_index], re.IGNORECASE)
        if found:
            one_time_retirement_class = found.group(1)

        found = re.search("^.+?(Roth[- ]401K)[^,]*,", filelines[fileline_index], re.IGNORECASE)
        if found:
            one_time_retirement_class = found.group(1)

        found = re.search("^.+?(Roth[- ]IRA)[^,]*,", filelines[fileline_index], re.IGNORECASE)
        if found:
            one_time_retirement_class = found.group(1)

        if re.search('^Vanguard joint account', filelines[fileline_index]):
            owner = "Joint"
            continue

        if re.search("^Mark's Vanguard retirement account", filelines[fileline_index]):
            owner = "Mark"
            continue

        if re.search("^Mireille's Vanguard retirement account", filelines[fileline_index]):
            owner = "Mireille"
            continue

        if re.search("^Mireille's Yahoo 401K", filelines[fileline_index]):
            owner = "Mireille"
            retirement_class = "401K"
            continue

        if re.search("^Mark misc. retirement accounts", filelines[fileline_index]):
            owner = "Mark"
            continue

        if re.search(',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,', filelines[fileline_index]):
            continue

        if re.search("^Totals for all above", filelines[fileline_index]):
            break

        if re.search("^Total", filelines[fileline_index]):
            continue

        # print str(fileline_index-1) + " = " + filelines[fileline_index]
        # line_list = filelines[fileline_index].split(',')
        rc, line_list, max_num_columns = get_csv(csv_input_source="string", csv_string=filelines[fileline_index])
        # print rc
        # print len(line_list)
        # print line_list[0]

        '''
        if len(line_list[1]) < 2:  # ignore labels
           continue
        if line_list[1] == '':  # ignore labels
           continue
        '''

        if retirement_class == "Non_Retirement":
            name = line_list[0]
            history = name
            description = line_list[0]
            symbol = line_list[1]
            account_ID = "TBD_account_ID"
            quantity = line_list[2].replace(',', '')

            header = [ "Name of Investment","Symbol","Number of shares","Cost Basis","Cost Basis date","difference","Cost Basis percent change","","","","Small Growth","Mid Growth","Large Growth","Small Blend","Mid Blend Aggressive","Large Blend","Small Value","Mid Value","Large Value","Bonds","Energy","Global","Healthcare","REIT","Individual Stocks"]

            '''
            Fidelity Contrafund (FCNTX),FCNTX,831.612,"$45,877 ",,"$38,748 ",84%,,,,,,"$84,625",,,,,,,,,,,,,,,,,,,

            '''
            asset_class = "TBD_asset_class"
            for index in range(10, len(header)):
                if line_list[index] != '':
                    asset_class = header[index]
                    total_value = line_list[index]
                    break
        else:
            # print filelines[fileline_index]
            name = line_list[0]
            history = name
            description = line_list[0]
            symbol = line_list[1]
            account_ID = "TBD_account_ID"
            quantity = line_list[3].replace(',', '')

            header = [ "Name of Investment","Symbol","Fund & Account","Number of shares","Cost Basis","Cost Basis date","Difference","Cost Basis Percent change","","Tradtional IRA - pre-tax","Traditional IRA - post-tax","Roth IRA","Traditional 401K","Roth 401K","Small Growth","Mid Growth","Large Growth","Small Blend","Mid Blend","Large Blend","Small Value","Mid Value","Large Value","Bonds","Energy","Global","Healthcare","REIT","","","" ]

            asset_class = "TBD_asset_class"
            for index in range(14, len(header)):
                if line_list[index] != '':
                    asset_class = header[index]
                    total_value = line_list[index]
                    break

        if symbol in share_prices:
            share_price = share_prices[symbol]
        else:
            msg = "ERROR: Share price for symbol " + symbol + " missing from lookup table in spreadsheet."
            print(msg)
            error_list.append(msg)
            share_price = "TBD_share_price_missing_from_spreadsheet"

        save_retirement_class = retirement_class
        if one_time_retirement_class != '':
            retirement_class = one_time_retirement_class

        funds.add(Investment(symbol=symbol, name=name, description=description, quantity=quantity, account_ID=account_ID, owner=owner, asset_class=asset_class, retirement_class=retirement_class,history=history,total_value=total_value,share_price=share_price,filename=inputfile,file_line_num=str(fileline_index)))

        one_time_retirement_class = ''
        retirement_class = save_retirement_class

        '''
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
              print "ERROR: input file line " + str(fileline_index) + ": " + filelines[fileline_index] + ".  Expecting fund name, quantity, share price."
              sys.exit(1)
           section_index += 1
           symbol = "TBD_symbol"
           name   = found.group(1)
           account_ID = "TBD_account_ID"
           quantity = found.group(2).strip()
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
              print "ERROR: input file line " + str(fileline_index) + ": " + filelines[fileline_index] + ".  Expecting stock symbol and name."
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
              print "ERROR: input file quantity line " + str(fileline_index) + ": " + filelines[fileline_index] + ".  Expecting stock quantity."
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

        funds.add(Investment(symbol=symbol, name=name, account_ID=account_ID, quantity=quantity, share_price=share_price, owner=owner, retirement_class=retirement_class))

     output_fd.close()

     # print "</Comments>"

     # for row in quantity_list:
     #    print row
     '''

    return 0, funds


#========================================================================

if __name__ == '__main__':

    if len(sys.argv) == 1:
        usage()

    print("<Investments>")
    print()

    rc, funds_list = convert_investment_spreadsheet_to_Investment(sys.argv[1])
    if len(error_list) > 0:
        print("<errors>")
        for error in error_list: print(error)
        print("</errors>")

    # total = Money(0)

    print(funds_list.__str__())

    print()
    # print "Total investments = " + str(funds_list.get_num_total())
    # print
    # print "Total amount = " + str(funds_list.get_total_amount())

    funds_list.show_stats()

    # for fund in funds_list.get_list():
        # print fund.__str__()
        # total.add(Money.Money().set_by_string(row.split(',')[5]))

    # print "total = " + total.__str__()

    print("<errors>")
    for error in error_list: print(error)
    print("</errors>")

    print()
    print("</Investments>")


'''
8.214 * 52.69 = 432.79566

5269 * 8 = 42152

5269 * (214/1000) = 1127.566

43279.566 =>
'''
