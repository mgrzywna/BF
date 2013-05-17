# -*- coding: utf-8 -*-

"""
BF interpreter
"""

__author__ = "Michal Grzywna"


import sys
from bf import bfeval


if __name__ == "__main__":
    if len(sys.argv) == 2:
        f = open(sys.argv[1])
        code = f.read()
        f.close()
        bfeval(code)
    else:
        print "USAGE: {} filename".format(sys.argv[0])
