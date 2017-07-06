#!/usr/bin/env python

import unittest


if __name__ == '__main__':
    # unittest.main()

    # group = unittest.loader.findTestCases(test_run_2_one_test_case_multiple_funcs.py)
    group = unittest.defaultTestLoader.discover('.', pattern='test_run_2_*')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(group)
