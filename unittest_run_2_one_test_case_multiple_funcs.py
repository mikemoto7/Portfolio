#!/usr/bin/env python

import unittest
from Portfolio import command_processing


class TestMethods(unittest.TestCase):

    def test_1(self):
        opt = "--all"
        all_table_html_files = []
        options = {}
        options['--web'] = True
        all_option = []
        all_option.append({'--pt': "show_percents"})
        all_option.append({'--pt': "show_ac_misc_totals"})
        all_option.append({'--inv': "lots"})
        all_option.append({'--inv': "diff"})
        options[opt] = all_option
        xml_filename = 'MASTER_LIST_201702041811.xml'
        self.assertEqual(command_processing(), 'FOO')

    def test_2(self):
        options = {}
        options['--inv'] = 'diff'
        xml_filename = 'MASTER_LIST_201702041811.xml'
        self.assertEqual(command_processing(), 'FOO')

if __name__ == '__main__':
    # unittest.main()

    tc_group = unittest.TestLoader().loadTestsFromTestCase(TestMethods)
    unittest.TextTestRunner(verbosity=2).run(tc_group)
