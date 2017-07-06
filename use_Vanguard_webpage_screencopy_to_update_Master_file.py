#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, sys, re
from pprint import pprint
import Money
from logging_wrappers import debug_option, srcLineNum
import getopt
from Portfolio import show_xml_file_stats
from operator import itemgetter
import xml_mi


#========================================================================

scriptName = os.path.basename(os.path.abspath(sys.argv[0])).replace('.pyc', '.py')


def usage():

    print ""
    print "Runstring:"
    print scriptName + " Vanguard_screen_copy_text_file MASTER_LIST.xml"
    print ""
    print "Manually screen-copy our Vanguard accounts page into a text file and then run this script on the text file to get updated share quantities and prices."
    print ""
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
    section_index = -1
    symbol_start = False
    quantity_list = []
    file_entries = []

    owner = ''
    retirement_class = "<retirement_class>TBD_retirement_class</retirement_class>"
    brokerage = "<brokerage>TBD_brokerage</brokerage>"

    list_of_dicts_of_updated_webpage_xml_fields = []
    update_id_num = -1
    TBD_lambda = lambda x,y:x if '$' in x else 'TBD_'+y
    params_set = False

    ret_class_dict = {
       'Traditional IRA': 'Traditional IRA',
       'Roth IRA': 'Roth IRA',
       'SEP-IRA': 'SEP-IRA',
       'SEP IRA': 'SEP-IRA',
       'Rollover IRA': 'Rollover IRA',
       }

    while True:
        # print "fileline_index = " + str(fileline_index) +  " .  list_size = " + str(list_size)
        # print "line  = " + filelines[fileline_index]
        fileline_index += 1
        if fileline_index >= list_size:
            break

        if filelines[fileline_index] == '':
            continue

        # print "line: " + str(fileline_index) + ", list_size = " + str(list_size)
        # print "line: " + str(fileline_index) + ": " + filelines[fileline_index]
        # print "found_section = " + str(found_section)

        if owner == '':

            if re.search("^ *Mark.+Mireille", filelines[fileline_index]):
                owner = "<owner>Joint</owner>"
                retirement_class = "<retirement_class>Non_Retirement</retirement_class>"
                brokerage = "<brokerage>Vanguard</brokerage>"
                continue

            # found = re.search("^ *Mark T. Ikemoto—([^-]+) *-*", filelines[fileline_index])
            # found = re.search("^ *Mark T. Ikemoto[^a-zA-Z0-9 -]*([a-zA-Z0-9 ]+) *-*", filelines[fileline_index])
            found = re.search("^ *Mark T. Ikemoto(.*)$", filelines[fileline_index])
            if found:
                retirement_class = ''
                ret_class = found.group(1).strip()
                for key, value in dict.items(ret_class_dict):
                    if key in ret_class:
                        retirement_class = "<retirement_class>" + value  + "</retirement_class>"
                if retirement_class == '':
                    print "ERROR: Unrecognized retirement_class.  Location: webpage holdings fileline_index = " + str(fileline_index)
                    continue
                owner = "<owner>Mark</owner>"
                brokerage = "<brokerage>Vanguard</brokerage>"
                continue

            found = re.search("^ *Mireille S Majoor(.*)$", filelines[fileline_index])
            if found:
                retirement_class = ''
                ret_class = found.group(1).strip()
                for key, value in dict.items(ret_class_dict):
                    if key in ret_class:
                        retirement_class = "<retirement_class>" + value  + "</retirement_class>"
                if retirement_class == '':
                    print "ERROR: Unrecognized retirement_class.  Location: webpage holdings fileline_index = " + str(fileline_index)
                    continue
                owner = "<owner>Mireille</owner>"
                brokerage = "<brokerage>Vanguard</brokerage>"
                continue

            found = re.search("^ *YAHOO 401(K) PLAN - 092466", filelines[fileline_index])
            if found:
                owner = "<owner>Mireille</owner>"
                retirement_class = "<retirement_class>Roth 401K</retirement_class>"
                brokerage = "<brokerage>Yahoo</brokerage>"
                continue


        '''
        # For the holdings HTML web page.
        if re.search("^   +Current balance", filelines[fileline_index]):

           fileline_index += 1
           symbol = "<symbol>" + filelines[fileline_index].split('\t')[0].strip() + "</symbol>"
           name = "<name>" + filelines[fileline_index].split('\t')[1].strip() + "</name>"

           fileline_index += 9
           account_ID = "<account_ID>" + filelines[fileline_index].split('\t')[3].strip() + "</account_ID>"

           fileline_index += 1
           curr_total_value = "<curr_total_value>" + TBD_lambda(filelines[fileline_index].strip().replace('$','').replace(',',''), 'curr_total_value') + "</curr_total_value>"

           cb_quantity = "<cb_quantity>0.00</cb_quantity>"
           cb_share_price = "<cb_share_price>0.00</cb_share_price>"
           cb_total_value = "<cb_total_value>0.00</cb_total_value>"
           cb_gain_loss = "<cb_gain_loss>0.00</cb_gain_loss>"
           cb_total_gain_loss = "<cb_total_gain_loss>0.00</cb_total_gain_loss>"
           params_set = True
        '''

        # For the holdings screen copy web page.
        if re.search("^Total", filelines[fileline_index]):
            owner = ''
            continue

        if re.search("^   *Buy    +Sell", filelines[fileline_index]):

            if owner == '':
                print "ERROR: 'owner' not set.  Location: webpage holdings fileline_index = " + str(fileline_index)
                continue

            # 2-line or 3-line entry?

            if filelines[fileline_index-2].split('\t')[0].strip() == '':
                # 3-line
                symbol = "<symbol>" + filelines[fileline_index-3].split('\t')[0].strip() + "</symbol>"
                name = "<name>" + filelines[fileline_index-3].split('\t')[1].strip() + "</name>"
                account_ID = "<account_ID>" + filelines[fileline_index-2].split('\t')[2].strip() + "</account_ID>"
                curr_quantity = "<curr_quantity>" + filelines[fileline_index-2].split('\t')[3].strip() + "</curr_quantity>"
                curr_share_price = "<curr_share_price>" + filelines[fileline_index-2].split('\t')[4].strip().replace('$','').replace(',','') + "</curr_share_price>"

            else:
                # 2-line
                symbol = "<symbol>" + filelines[fileline_index-2].split('\t')[0].strip() + "</symbol>"
                name = "<name>" + filelines[fileline_index-2].split('\t')[1].strip() + "</name>"
                account_ID = "<account_ID>" + filelines[fileline_index-2].split('\t')[3].strip() + "</account_ID>"
                curr_quantity = "<curr_quantity>" + filelines[fileline_index-2].split('\t')[4].strip() + "</curr_quantity>"
                curr_share_price = "<curr_share_price>" + filelines[fileline_index-2].split('\t')[5].strip().replace('$','').replace(',','') + "</curr_share_price>"

            curr_total_value = "<curr_total_value>" + TBD_lambda(filelines[fileline_index-1].strip().replace('$','').replace(',',''), 'curr_total_value') + "</curr_total_value>"
            if '>0.00<' in curr_total_value:
                status = "<status>not_active</status>"
            else:
                status = "<status>active</status>"

            cb_quantity = "<cb_quantity>0.00</cb_quantity>"
            cb_share_price = "<cb_share_price>0.00</cb_share_price>"
            cb_total_value = "<cb_total_value>0.00</cb_total_value>"
            cb_gain_loss = "<cb_gain_loss>0.00</cb_gain_loss>"
            cb_total_gain_loss = "<cb_total_gain_loss>0.00</cb_total_gain_loss>"
            params_set = True

        # For the cost-basis web page.
        if re.search("^Average cost", filelines[fileline_index]):
            if owner == '':
                print "ERROR: 'owner' not set.  Location: webpage cost-basis fileline_index = " + str(fileline_index)
                continue

            symbol = "<symbol>" + filelines[fileline_index-2].split('\t')[0].strip() + "</symbol>"
            name = "<name>" + filelines[fileline_index-2].split('\t')[1].strip() + "</name>"
            account_ID = "<account_ID>" + filelines[fileline_index-1].strip() + "</account_ID>"
            curr_quantity = "<curr_quantity>0.000</curr_quantity>"
            curr_share_price = "<curr_share_price>0.00</curr_share_price>"
            curr_total_value = "<curr_total_value>" + TBD_lambda(filelines[fileline_index].split('\t')[4].strip().replace('$','').replace(',',''), 'curr_total_value') + "</curr_total_value>"
            if '>0.00<' in curr_total_value:
                status = "<status>not_active</status>"
            else:
                status = "<status>active</status>"

            cb_quantity = "<cb_quantity>" + filelines[fileline_index].split('\t')[1].strip() + "</cb_quantity>"
            cb_share_price = "<cb_share_price>" + TBD_lambda(filelines[fileline_index].split('\t')[2].strip().replace('$','').replace(',',''), 'cb_share_price') + "</cb_share_price>"
            cb_total_value = "<cb_total_value>" + TBD_lambda(filelines[fileline_index].split('\t')[3].strip().replace('$','').replace(',',''), 'cb_total_value') + "</cb_total_value>"
            cb_gain_loss = "<cb_gain_loss>" + TBD_lambda(filelines[fileline_index].split('\t')[5].strip().replace('$','').replace(',',''), 'cb_gain_loss') + "</cb_gain_loss>"
            cb_total_gain_loss = "<cb_total_gain_loss>" + TBD_lambda(filelines[fileline_index].split('\t')[6].strip().replace('$','').replace(',',''), 'cb_total_gain_loss') + "</cb_total_gain_loss>"
            params_set = True


        if params_set == True:
            update_id_num += 1
            list_of_dicts_of_updated_webpage_xml_fields.append(
                     {
                        'update_num': str(update_id_num),
                        'line_num': fileline_index,
                        '<status>': status,
                        '<owner>': owner,
                        '<brokerage>': brokerage,
                        '<retirement_class>': retirement_class,
                        "<symbol>": symbol,
                        "<name>": name,
                        "<account_ID>": account_ID,
                        "<cb_quantity>": cb_quantity,
                        "<cb_share_price>": cb_share_price,
                        "<cb_total_value>": cb_total_value,
                        "<cb_gain_loss>": cb_gain_loss,
                        "<cb_total_gain_loss>": cb_total_gain_loss,
                        "<curr_quantity>": curr_quantity,
                        "<curr_share_price>": curr_share_price,
                        "<curr_total_value>": curr_total_value,
                     }
                  )
            params_set = False
        continue

        '''
        # print "line2: " + str(fileline_index) + ": " + filelines[fileline_index]
        if not re.search('Change\s+Current balance|Buy\s+Sell', filelines[fileline_index]):
           continue
        # print "after"

        fileline_index += 1

        if re.search('^Total', filelines[fileline_index]):
           found_section = False
           section_index = -1
           quantity_list.append("")
           print
           output_fd.write('\n')
           continue

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

        details_file = "Vanguard_details/" + symbol + "," + name + "," + account_ID + ".txt"
        if not os.path.isfile(details_file):
           print "WARNING: File does not exist: " + details_file

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
     '''

    return 0, list_of_dicts_of_updated_webpage_xml_fields

#========================================================================

def get_master_list_indents(MASTER_LIST_xml_file):
    MASTER_LIST_xml_file_indents = {}
    for line in open(MASTER_LIST_xml_file, "r").read().splitlines():
        found = re.search('^( *)(<[^>]*>)', line)
        if found:
            indent = found.group(1)
            key = found.group(2)
            if key not in MASTER_LIST_xml_file_indents:
                MASTER_LIST_xml_file_indents[key] = indent

    # for key, value in dict.items(MASTER_LIST_xml_file_indents):
    #    print "key:" + key + ",value:" + value + ":end_value"

    return 0, MASTER_LIST_xml_file_indents

#========================================================================

'''
def format_list_of_xml_strings(list_of_xml_strings):
   xml_list_formatted = []
   for row in list_of_xml_strings:
      output = ''
      line_num = row.split(':')[0]
      xml_string = '<line_num>' + line_num + '</line_num>' + row.split(':')[1]
      indent = ''
      while True:
         if xml_string == '':
            break
         found = re.search('^(<[^>]+>[^<]*<[^>]+>)(.*)$', xml_string)
         if not found:
            break
         output += indent + found.group(1) + '\n'
         indent += '  '
         xml_string = found.group(2)
      xml_list_formatted.append(output)

   # xml_list_sorted = sorted(xml_list_sorted, key=itemgetter(1))
   # xml_list_sorted = sorted(xml_list_sorted, key=itemgetter(5))
   #
   # for row in xml_list_sorted:
   #    # output += row[1] + row[5] + row[2] + row[3] + row[4] + row[0] + '\n'
   #    indent = ''
   #    for index in [1,5,2,3,4,0]:
   #       output += indent + row[index] + '\n'
   #       indent += '  '

   return xml_list_formatted
'''

def format_xml_string(xml_string, first_element=''):
    xml_string_formatted = ''
    line_num_element = '<line_num>' + xml_string.split(':')[0] + '</line_num>'
    xml_string = xml_string.split(':')[1]
    while True:
        if xml_string == '':
            break
        found = re.search('^(<[^>]+>[^<]*<[^>]+>)(.*)$', xml_string)
        if not found:
            break
        if first_element == '':
            xml_string_formatted += found.group(1) + '\n'
        elif first_element in found.group(1):
            xml_string_formatted = found.group(1) + '\n' + xml_string_formatted
            first_element = ''
        else:
            xml_string_formatted += found.group(1) + '\n'

        xml_string = found.group(2)

    xml_string_formatted += line_num_element

    xml_string_formatted_string = ''
    indent = '   '
    for element in xml_string_formatted.split('\n'):
        xml_string_formatted_string += indent + element + '\n'
        indent += '   '

    return xml_string_formatted_string


#========================================================================

if __name__ == '__main__':

    if len(sys.argv) == 1:
        usage()

    # Set a global debug flag based on an environment variable, or use logging.DEBUG below, or both.
    debug_flag = debug_option(__file__ + "," + srcLineNum())

    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["debug"])
    except:
        print("ERROR: Unrecognized runstring option.")
        usage()

    for opt, arg in opts:
        if opt == "--debug":
            # setLoggingLevel(logging.DEBUG)
            debug_flag = True
        else:
            print("ERROR: Runstring options.")
            usage()


    Vanguard_screen_copy_text_file = args[0]
    MASTER_LIST_xml_file = args[1]

    rc, list_of_dicts_of_updated_webpage_xml_fields = extract_Vanguard_info(Vanguard_screen_copy_text_file)

    # must_match_field_list = ['<owner>', '<retirement_class>', '<symbol>', '<name>', '<account_ID>']
    must_match_field_list = ['<owner>', '<status>', '<retirement_class>', '<symbol>', '<account_ID>', '<brokerage>']
    webpage_full_tag_sets = []
    for entry in list_of_dicts_of_updated_webpage_xml_fields:
        line = str(entry['line_num']) + ":"
        for key in must_match_field_list:
            line += entry[key]
        webpage_full_tag_sets.append(line)

    fd_webpage_full_tag_sets = open(scriptName + "_debug_webpage_full_tag_sets.xml", "w")

    rc, MASTER_LIST_xml_file_indents = get_master_list_indents(MASTER_LIST_xml_file)

    candidate_new_master_file = scriptName + "_new_Master_file.xml"
    fd_new_master_file = open(candidate_new_master_file, "w")
    fd_new_master_file.write(MASTER_LIST_xml_file_indents['<top>'] + '<top>' + '\n')
    fd_new_master_file.write(MASTER_LIST_xml_file_indents['<Investments>'] + '<Investments>' + '\n')

    # for debugging
    fd_web_page = open(scriptName + "_debug_web_page.xml", "w")
    fd_web_page_no_match = open(scriptName + "_debug_web_page_no_match.xml", "w")
    fd_file_all_tags = open(scriptName + "_debug_file_all_tags.xml", "w")
    file_all_tags = []
    file_full_tag_sets = []
    fd_file_full_tag_sets = open(scriptName + "_debug_file_full_tag_sets.xml", "w")

    fd_stats = open(scriptName + "_debug_stats.txt", "w")


    file_inv_block = []
    webpage_matches_for_file_block = []
    no_webpage_matches_for_file_block = []
    file_blocks_count = 0
    file_blocks_count_active = 0


    # file_matches_for_webpage_status_list = []
    # for web_entry in list_of_dicts_of_updated_webpage_xml_fields:
    #    file_matches_for_webpage_status_list.append({'file_matches':list(), 'web_entry': web_entry})

    # match_status_list = []
    # for web_entry in list_of_dicts_of_updated_webpage_xml_fields)
    #    match_status_list.append({'match_type': str(), 'file_matches':list(), 'web_entry': entry})

    # match_status_webpage_list = list(list_of_dicts_of_updated_webpage_xml_fields)
    file_matches_for_webpage_block = []
    no_file_matches_for_webpage_block = []

    error_list = ''
    file_inv_block_dict = {}

    fileline = -1

    for line in open(MASTER_LIST_xml_file, "r").read().splitlines():
        fileline += 1

        if line == '':
            continue

        if '<Investment>' in line:
            file_inv_block_line_num = fileline
            # file_inv_block = ['fileline:' + str(file_inv_block_line_num), line]
            file_inv_block = [line]
            continue

        if '</Investment>' in line:
            file_inv_block.append(line)
            file_blocks_count += 1

            if file_inv_block_dict['<status>'] == 'active':
                file_blocks_count_active += 1

            # We have an investment entry from the file.
            # Loop through our web page updates and see if there is a match.

            file_matches_for_webpage_for_one_file_inv = list(list_of_dicts_of_updated_webpage_xml_fields)

            candidate_webpage_blocks = [] # Use a list because it's possible multiple web page blocks may match a file block.
            if debug_flag: print '245', len(candidate_webpage_blocks)


            # For debugging
            temp_debug_line = ''
            for must_match_field in must_match_field_list:
                if debug_flag: print '248', len(candidate_webpage_blocks), must_match_field, "file block line start", file_inv_block_line_num
                file_field_found = ''
                for file_field in file_inv_block:
                    if must_match_field in file_field:
                        file_field_found = file_field
                        if temp_debug_line == '':
                            temp_debug_line = str(file_inv_block_line_num) + ":"
                        temp_debug_line += file_field.strip()
                        if debug_flag: print '256', 'temp_debug_line = ' + file_field
                        break
            file_full_tag_sets.append(temp_debug_line)

            debug_line = ''

            for must_match_field in must_match_field_list:
                if debug_flag: print '248', len(candidate_webpage_blocks), must_match_field, "file block line start", file_inv_block_line_num
                file_field_found = ''
                for file_field in file_inv_block:
                    if must_match_field in file_field:
                        file_field_found = file_field
                        if debug_line == '':
                            debug_line = str(file_inv_block_line_num) + ":"
                        debug_line += file_field.strip()
                        if debug_flag: print '256', 'debug_line = ' + file_field
                        break
                if file_field_found == '':
                    print "ERROR: File investment " + file_inv_block[0] + " is missing field " + file_field
                    sys.exit(1)

                if len(candidate_webpage_blocks) > 0:
                    index = -1
                    while True:
                        index += 1
                        if index >= len(candidate_webpage_blocks):
                            break
                        if debug_flag: print candidate_webpage_blocks[index][must_match_field]
                        if debug_flag: print file_field_found
                        file_field_found_filtered = re.sub('</[^>]+>', '', file_field_found.strip())
                        if file_field_found_filtered not in candidate_webpage_blocks[index][must_match_field]:
                            del candidate_webpage_blocks[index]
                            if debug_flag: print '268', len(candidate_webpage_blocks)
                            index -= 1

                    '''
                    if must_match_field == '<symbol>':
                       print "debug: fileline = " + str(fileline)
                       print "debug: file_field_found = " + file_field_found
                       print "debug: len(candidate_webpage_blocks) = " + str(len(candidate_webpage_blocks))
                       for loop in candidate_webpage_blocks:
                          print "debug: candidate_webpage_blocks:"
                          print loop
                       sys.exit(1)
                    '''

                    if len(candidate_webpage_blocks) == 0:
                        break

                    continue

                # Create initial collection of candidate_webpage_blocks.
                index = -1
                while True:
                    index += 1
                    if index >= len(file_matches_for_webpage_for_one_file_inv):
                        break
                    if file_matches_for_webpage_for_one_file_inv[index][must_match_field] in file_field_found:
                        candidate_webpage_blocks.append(file_matches_for_webpage_for_one_file_inv[index])
                        '''
                        file_matches_for_webpage_for_one_file_inv[index]['match_flag'] = True
                        match_status_webpage_list[index]['match_flag'] = True
                        webpage_matches_for_file_block.append([file_matches_for_webpage_for_one_file_inv[index], file_inv_block])
                        match += 1
                        '''


                if debug_flag: print '301', len(candidate_webpage_blocks)
                if len(candidate_webpage_blocks) == 0:
                    break

                if debug_flag: print '306', len(candidate_webpage_blocks)
                continue



            if debug_flag: print '309', len(candidate_webpage_blocks)
            if len(candidate_webpage_blocks) == 0:
                no_webpage_matches_for_file_block.append(file_inv_block)
            else:
                webpage_matches_for_file_block.append({'fileline': file_inv_block_line_num , 'file_inv_block':file_inv_block, 'webpage_blocks': candidate_webpage_blocks })
                if len(candidate_webpage_blocks) > 1:
                    separator = ''
                    webpage_line_nums = ''
                    for entry in candidate_webpage_blocks:
                        webpage_line_nums += separator + str(entry['line_num'])
                        separator = ','
                    error_list += "ERROR: Multiple webpage blocks match a file block at fileline " + str(file_inv_block_line_num) + '.  webpage line nums: ' + webpage_line_nums + '\n'

            # if len(candidate_webpage_blocks) == 1:
            file_inv_block_dict = {}
            webpage_inv_block_dict = {}
            new_master_file_list = []
            for fib_line in file_inv_block:
                '''
                # for tag in ['<Investment>', '<cost_basis>', '<cb_event>', '</cb_event>', '</cost_basis>', '</Investment>' ]:
                for tag in ['<cost_basis>', '<cb_event>', '</cb_event>', '</cost_basis>']:
                   if tag in fib_line:
                      # print MASTER_LIST_xml_file_indents[tag] + tag
                      fib_line = MASTER_LIST_xml_file_indents[tag] + tag
                      break
                '''

                found2 = False
                tags_to_update = ['<cb_quantity>', '<cb_share_price>', '<cb_total_value>', '<curr_total_value>', '<cb_gain_loss>', '<cb_total_gain_loss>', '<curr_quantity>', '<curr_share_price>']
                for tag in tags_to_update:
                    found = re.search('^ *'+tag+'([^<]*)<', fib_line)
                    if found:
                        fib_line_xml_value = found.group(1)
                        if 'TBD' in fib_line_xml_value:
                            fib_line_xml_value = 0.00
                        else:
                            fib_line_xml_value = float(fib_line_xml_value)

                        # fib_line = MASTER_LIST_xml_file_indents[tag] + file_matches_for_webpage_for_one_file_inv[0][tag]
                        file_inv_block_dict[tag] = fib_line_xml_value

                        found2 = re.search('^ *'+tag+'([^<]*)<', file_matches_for_webpage_for_one_file_inv[0][tag])
                        if found2:
                            webpage_line_xml_value = found.group(1)
                            if 'TBD' in webpage_line_xml_value:
                                webpage_line_xml_value = 0.00
                            else:
                                webpage_line_xml_value = float(webpage_line_xml_value)

                            webpage_inv_block_dict[tag] = webpage_line_xml_value

                            break

                new_master_file_list.append(fib_line)

            for key,value in dict.items(file_inv_block_dict):
                if key == '<curr_quantity>' or key == '<cb_quantity>':
                    format = '%1.3f'
                else:
                    format = '%1.2f'
                if webpage_inv_block_dict[key] > value:
                    new_fib_line = MASTER_LIST_xml_file_indents[key] + key + format % webpage_inv_block_dict[key] + key.replace('<','</')
                else:
                    new_fib_line = MASTER_LIST_xml_file_indents[key] + key + format % value + key.replace('<','</')
                for index in xrange(len(new_master_file_list)):
                    if key in new_master_file_list[index]:
                        new_master_file_list[index] = new_fib_line
                        break

                if webpage_inv_block_dict['<curr_total_value>'] > file_inv_block_dict['<curr_total_value>']:
                    new_curr_total_value = webpage_inv_block_dict['<curr_total_value>']
                else:
                    new_curr_total_value = file_inv_block_dict['<curr_total_value>']

                if (webpage_inv_block_dict['<curr_quantity>'] * webpage_inv_block_dict['<curr_share_price>']) > new_curr_total_value:
                    new_curr_total_value = webpage_inv_block_dict['<curr_quantity>'] * webpage_inv_block_dict['<curr_share_price>']

                if (file_inv_block_dict['<curr_quantity>'] * file_inv_block_dict['<curr_share_price>']) > new_curr_total_value:
                    new_curr_total_value = file_inv_block_dict['<curr_quantity>'] * file_inv_block_dict['<curr_share_price>']


            for index in xrange(len(new_master_file_list)):
                if '<curr_total_value>' in new_master_file_list[index]:
                    new_master_file_list[index] = MASTER_LIST_xml_file_indents['<curr_total_value>'] + '<curr_total_value>' + "%1.2f" % new_curr_total_value + '</curr_total_value>'
                fd_new_master_file.write(new_master_file_list[index] + '\n')

            file_matches_for_webpage_block.append({'file_inv_block_list':file_inv_block, 'webpage_blocks': candidate_webpage_blocks })

            file_inv_block = []
            file_matches_for_webpage_for_one_file_inv = []


            file_all_tags.append(debug_line)

            continue


        # Collect all other file block lines.
        file_inv_block.append(line)

        tag = xml_mi.extract_strings_from_xml_element_string(line)[0]
        value = xml_mi.extract_strings_from_xml_element_string(line)[1]
        rest_of_xml_string = xml_mi.extract_strings_from_xml_element_string(line)[2]

        file_inv_block_dict[tag] = value



    fd_new_master_file.write(MASTER_LIST_xml_file_indents['</Investments>'] + '</Investments>' + '\n')
    fd_new_master_file.write(MASTER_LIST_xml_file_indents['</top>'] + '</top>' + '\n')
    fd_new_master_file.close()

    for row in file_all_tags:
        fd_file_all_tags.write(row + '\n')
    fd_file_all_tags.close()



    '''
    for web_block in list_of_dicts_of_updated_webpage_xml_fields:
       debug_line = web_block['update_num'] + ":"
       for must_match_field in must_match_field_list:
          debug_line += web_block[must_match_field].strip()
       fd_web_page.write(debug_line + '\n')
    fd_web_page.close()

    for entry in match_status_webpage_list:
       if entry['match_flag'] == True:
          file_matches_for_webpage_block.append(entry)
       else:
          no_file_matches_for_webpage_block.append(entry)

    for webpage_block in no_file_matches_for_webpage_block:
       fd_web_page_no_match.write(str(webpage_block) + '\n')
    fd_web_page_no_match.close()
    # Format a nicer-looking txt file
    fd_web_page_no_match = open(scriptName + "_debug_web_page_no_match.xml", "r")
    fd_web_page_no_match_txt = open(scriptName + "_debug_web_page_no_match.txt", "w")


    for entry in fd_web_page_no_match:
       entry = re.sub('([0-9]),([0-9])', r'\1\2', entry)
       for entry_row in entry.split(','):
          if 'update_num' in entry_row:
             continue
          entry_row = re.sub("^.'<[^:]+: ", '', entry_row)
          entry_row = re.sub("^ *'(.+)'$", r'\1', entry_row)
          entry_row = re.sub("['}]", '', entry_row)
          entry_row = re.sub("^ *", '', entry_row)
          entry_row = re.sub("^ *", '', entry_row)
          key = re.sub("^ *([^>]*>).*$", r'\1', entry_row)
          entry_row = MASTER_LIST_xml_file_indents[key] + entry_row
          fd_web_page_no_match_txt.write(entry_row + '\n')


    fd_web_page_no_match_txt.close()
    fd_web_page_no_match.close()
    '''


    stats_output = '\n'
    stats_output += 'Matched fields: ' + ','.join(must_match_field_list) + '\n'
    stats_output += '\n'
    stats_output += 'Master file: ' + MASTER_LIST_xml_file + '\n'
    stats_output += "file_blocks_count = " + str(file_blocks_count) + '\n'
    stats_output += "file_blocks_count_active = " + str(file_blocks_count_active) + '\n'
    stats_output += "len(webpage_matches_for_file_block) = " + str(len(webpage_matches_for_file_block)) + '\n'
    stats_output += "len(no_webpage_matches_for_file_block) = " + str(len(no_webpage_matches_for_file_block)) + '\n'
    fd_no_webpage_matches_for_file_block = open(scriptName + "_no_webpage_matches.xml", "w")
    for loop in no_webpage_matches_for_file_block:
        fd_no_webpage_matches_for_file_block.write(str(loop) + '\n')
    fd_no_webpage_matches_for_file_block.close()

    stats_output += '\n'
    stats_output += 'Webpage file: ' + Vanguard_screen_copy_text_file + '\n'
    stats_output += "len(list_of_dicts_of_updated_webpage_xml_fields) = " + str(len(list_of_dicts_of_updated_webpage_xml_fields)) + '\n'
    stats_output += "len(file_matches_for_webpage_block) = " + str(len(file_matches_for_webpage_block)) + '\n'
    stats_output += "len(no_file_matches_for_webpage_block) = " + str(len(no_file_matches_for_webpage_block)) + '\n'

    stats_output += '\n'
    stats_output += 'Match details:\n'
    if error_list != '':
        stats_output += error_list + '\n'

    '''
    for entry in webpage_matches_for_file_block:
       stats_output += 'Fileline = ' + str(entry['fileline']) + ', num webpage matches = ' + str(len(entry['webpage_blocks'])) + '\n'
    '''

    for row in file_full_tag_sets:
        fd_file_full_tag_sets.write(row + '\n')
    fd_file_full_tag_sets.close()

    for row in webpage_full_tag_sets:
        fd_webpage_full_tag_sets.write(row + '\n')
    fd_webpage_full_tag_sets.close()

    stats_output += '\n'
    file_found_matching_webpage = []
    file_did_not_find_matching_webpage = []
    for row in file_full_tag_sets:
        found = False
        search_string = row.split(':')[1]
        for row2 in webpage_full_tag_sets:
            if search_string in row2:
                file_found_matching_webpage.append(row2)
                found = True
        if not found:
            file_did_not_find_matching_webpage.append(row)

    stats_output += 'len(file_full_tag_sets) = ' + str(len(file_full_tag_sets)) + '\n'
    stats_output += 'Entries in file_full_tag_sets matched by webpage_full_tag_sets = ' + str(len(file_found_matching_webpage)) + '\n'

    stats_output += '\n'
    webpage_found_matching_file = []
    webpage_did_not_find_matching_file = []
    for row in webpage_full_tag_sets:
        # print "row: " + row.split(':')[0]
        found = ''
        search_string = row.split(':')[1]
        for row2 in file_full_tag_sets:
            if search_string in row2:
                if found != '':
                    print "WARNING: Multiple file matches for webpage:"
                    print "webpage entry: " + row
                    print "file entry: " + found
                    print "file entry: " + row2
                webpage_found_matching_file.append(row2)
                found = row2
        if found == '':
            webpage_did_not_find_matching_file.append(row)

    stats_output += 'len(webpage_full_tag_sets) = ' + str(len(webpage_full_tag_sets)) + '\n'
    stats_output += 'Entries in webpage_full_tag_sets matched by file_full_tag_sets = ' + str(len(webpage_found_matching_file)) + '\n'
    stats_output += '\n'

    rc, file_stats = show_xml_file_stats(MASTER_LIST_xml_file)
    stats_output += file_stats

    stats_output += '\n'
    stats_output += 'len(file_full_tag_sets) = ' + str(len(file_full_tag_sets)) + '\n'
    stats_output += 'len(webpage_full_tag_sets) = ' + str(len(webpage_full_tag_sets)) + '\n'
    stats_output += 'Diff = ' + str(len(file_full_tag_sets) - len(webpage_full_tag_sets)) + '\n'
    stats_output += '\n'

    stats_output += 'file_did_not_find_matching_webpage:' + '\n'
    stats_output += 'len(file_did_not_find_matching_webpage) = ' + str(len(file_did_not_find_matching_webpage)) + '\n'
    xml_list = list(file_did_not_find_matching_webpage)
    for search_string in ['<status>not_active</status>', '<brokerage>Fidelity</brokerage>', '<brokerage>Schwab</brokerage>', '<brokerage>Yahoo</brokerage>' ]:
        stats_output += '\n'
        stats_output += 'Expected--  ' + search_string + '\n'
        stats_output += '\n'
        index = -1
        while True:
            index += 1
            if index >= len(xml_list):
                break
            if search_string in xml_list[index]:
                stats_output += format_xml_string(xml_list[index], search_string)
                del xml_list[index]
                index -= 1
    stats_output += 'Unexpected--' + '\n'
    if len(xml_list) == 0:
        stats_output += 'None' + '\n'
    else:
        for loop in xml_list:
            stats_output += loop

    stats_output += '\n'
    stats_output += 'webpage_did_not_find_matching_file:' + '\n'
    stats_output += 'len(webpage_did_not_find_matching_file) = ' + str(len(webpage_did_not_find_matching_file)) + '\n'
    for loop in webpage_did_not_find_matching_file:
        stats_output += loop + '\n'

    stats_output += '\n'
    stats_output += 'Candidate xml file created: ' + candidate_new_master_file + '\n'



    fd_stats.write(stats_output)
    fd_stats.close()
    print stats_output
