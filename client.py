# -*- coding: utf-8 -*-

"""
Network BF interpreter (client)

Reads BF source code from file, sends it to server.
After receiving result of evaluation prints it to the console.
"""

__author__ = "Michal Grzywna"
__mail__ = "michal(at)grzywna.me"


import sys, socket


def evaluate(filename, host):
    f = open(filename, 'r')
    code = f.read()
    f.close

    s = socket.socket()
    s.connect((host, 1337))
    s.send(code)
    result = s.recv(4096)
    s.close()
    return result


if __name__ == "__main__":
    if len(sys.argv) == 2:
        result = evaluate(sys.argv[1], 'localhost')
        print result
    else:
        print "USAGE: {} filename".format(sys.argv[0])

