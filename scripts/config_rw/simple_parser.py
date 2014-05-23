#!/usr/bin/env python
# coding=utf-8

__author__ = 'iLiKo'

def simple_parse_config(filename):
    COMMENT_CHAR = '#'
    OPTION_CHAR = '='
    options = {}
    f = open(filename)
    for line in f:
        # First, remove comments:
        if COMMENT_CHAR in line:
            # split on comment char, keep only the part before
            line, comment = line.split(COMMENT_CHAR, 1)
        # Second, find lines with an option=value:
        if OPTION_CHAR in line:
            # split on option char:
            option, value = line.split(OPTION_CHAR, 1)
            # strip spaces:
            option = option.strip()
            value = value.strip()
            # store in dictionary:
            options[option] = value
    f.close()
    return options

path = raw_input("Enter the path to file: ")
options = simple_parse_config(path)
print options