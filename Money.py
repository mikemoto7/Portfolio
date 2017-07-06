#!/usr/bin/env python

import sys, os, re

import inspect

scriptName = os.path.basename(__file__).replace('.pyc', '.py')
scriptDir  = os.path.dirname(os.path.realpath(__file__))

sys.path.append(scriptDir + '/lib')
sys.path.append(scriptDir + '/bin')

from logging_wrappers import reportError


class Money():

    #==============================

    def __init__(self, value=0):
        # print value, str(type(value))

        self._errors = []
        # print "init:", type(value), value.__class__.__name__
        if 'int' in str(type(value)):
            self._cents = int(value)
        elif 'str' in str(type(value)):
            self._cents = Money().set_by_string(value)._cents
        else:
            self._cents = 0

        # print self._cents

        # print "self: " + str(id(self))

    #==============================

    def get_cents(self):
        return self._cents

    #==============================

    def set_cents(self, value=0):
        self._cents = value

    #==============================

    def set_by_string(self, value='0.00'):
        self._errors = []
        value = value.replace('$', '')  # if present
        if value == '' or re.search('[^0-9\.\$\-]', value):
            msg = "ERROR: Non-numeric value passed to Money.__set_by_string method.  Value = " + value
            reportError(msg)
            self._errors.append(msg)
            (frame, filename, line_number, function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
            print((frame, filename, line_number, function_name, lines, index))
            return self
        if not '.' in value:
            value += '.0'
        dollar_str, cents_str = value.split('.')
        self._cents = int(dollar_str) * 100 + int(cents_str)
        # Above statements will set neg sign
        # if value[0] == '-':
        #      self._cents = -self._cents
        return self

    #==============================

    def set_by_fields(self, dollars=0, cents=0):
        self._errors = []
        self._cents = int(dollars) * 100 + int(cents)
        return self

    #==============================

    def __str__(self, pretty_print=False):
        # user-friendly form, locale specific if needed
        if pretty_print:
            dollar_string = str(self._cents / 100)
            dollar_string_with_commas = ''
            char_count = 0
            # for char in reversed(dollar_string):
            # for index in xrange(len(dollar_string), 0, -1):
            for char in dollar_string[::-1]:
                if char_count == 3:
                    dollar_string_with_commas = ',' + dollar_string_with_commas
                    char_count = 0
                dollar_string_with_commas = char + dollar_string_with_commas
                char_count += 1
            amount = '$' + dollar_string_with_commas
        else:
            amount = str(self._cents / 100)

        if '.' in amount:  # Python 3
           amount = amount.split('.')[0]
        # else:  # Python 2
        amount_cents = str(self._cents % 100)
        if len(amount_cents) == 1:
            amount_cents = '0' + amount_cents
        amount += '.' + amount_cents

        return amount

    #==============================

    def less_than(self, other):
        return self._cents < Money(other)._cents

    #==============================

    def add(self, other, keep=True):
        # print "add:", type(other)
        other_type = str(type(other))
        if 'instance' in other_type or 'Money' in other_type:
            if keep == True:
                self._cents += other._cents
                return self
            else:
                return self._cents + other._cents
        elif 'str' in other_type:
            if keep == True:
                self._cents += Money(other)._cents
                return self
            else:
                return self._cents + Money(other)._cents
        elif 'long' in other_type or 'int' in other_type:
            if keep == True:
                self._cents += other
                return self
            else:
                return self._cents + other
        else:
            (frame, filename, line_number, function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
            reportError("add: Unrecognized input param (%s) variable type: %s.  Stack info:\nframe: %s\nfilename: %s\nline_number: %s\nfunction_name: %s\nlines: %s\nindex: %s\n" % (str(other), other_type, frame, filename, line_number, function_name, lines, index))
            sys.exit(1)

    #==============================

    def sub(self, other, keep=True):
        # print "sub:", type(other)
        other_type = str(type(other))
        if 'instance' in other_type or 'Money' in other_type:
            if keep == True:
                self._cents -= other._cents
                return self
            else:
                return self._cents - other._cents
        elif 'str' in other_type:
            if keep == True:
                self._cents -= Money(other)._cents
                return self
            else:
                return self._cents - Money(other)._cents
        elif 'long' in other_type:
            if keep == True:
                self._cents -= other
                return self
            else:
                return self._cents - other
        else:
            reportError("sub: Unrecognized input param (" + str(other) + ") variable type: " + other_type)
            (frame, filename, line_number, function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
            print((frame, filename, line_number, function_name, lines, index))
            sys.exit(1)

    #==============================

    def mult(self, multiplier="0.0"):
        whole_num_str, decimal_str = multiplier.split('.')
        whole_num_str = whole_num_str.replace(",", "")
        # print whole_num_str
        # print decimal_str
        cents_orig = self._cents
        self._cents = cents_orig * int(whole_num_str)
        divisor = 1
        for index in xrange(len(decimal_str)):
            divisor *= 10
        # print "divisor: " + str(divisor)
        # print (float(decimal_str) / float(divisor))
        self._cents += int(cents_orig * (float(decimal_str) / float(divisor)))
        # print "self._cents = " + str(self._cents)
        return self

    #==============================

    def percent(self, other):
        other_type = str(type(other))
        if 'instance' in other_type or 'Money.Money' in other_type:
            divisor = other._cents
        elif 'str' in other_type:
            divisor = Money().set_by_string(other)._cents
        elif 'long' in other_type or 'int' in other_type:
            divisor = other
        elif 'float' in other_type:
            divisor = other
        else:
            reportError("percent: Unrecognized input param (" + str(other) + ") variable type: " + other_type)
            (frame, filename, line_number, function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
            print((frame, filename, line_number, function_name, lines, index))
            sys.exit(1)

        if divisor == 0:
            return 0.00

        # percent = long(round((float(self._cents) / float(divisor._cents)) * 100))
        percent = (round((float(self._cents) / float(divisor)) * 100, 2))
        return percent

    #==============================



if __name__ == '__main__':

    # file_of_nums = sys.argv[1]

    total = 0.0
    final_total = 1454590.89
    final_total_str = '1454590.89'
    final_total_money = Money().set_by_string(final_total_str)
    # for num in open(file_of_nums, 'r').read().splitlines():
    num_list = sys.stdin.read().splitlines()
    for num in num_list:
        total += float(num)

    for num in num_list:
        num_money = Money().set_by_string(num)
        print(str(num) + "        " + str(float(num)/total*100) + "       " + num_money.percent(final_total_money).__str__())

    print(total)
