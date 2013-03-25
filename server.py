# -*- coding: utf-8 -*-

"""
Network BF interpreter (server)

Server listens on port 1337 and is trying to evaluate every data sent by client
and sends back result of evaluation. If some error occurs it sends error message.
"""

__author__ = "Michal Grzywna"
__mail__ = "michal(at)grzywna.me"


import socket, time
from bf import bfeval

BUFFER_SIZE = 4096

def receiveall(socket):
    """Receive all data from client."""
    socket.setblocking(0)
    buff = []
    while True:
        try:
            data = socket.recv(BUFFER_SIZE)
            if data: buff.append(data)
            else: break
        except:
            break
    return "".join(buff)


if __name__ == '__main__':

    HOST = ''
    PORT = 1337
    server = socket.socket()
    server.bind((HOST, PORT))
    server.listen(5)

    while True:
        client, address = server.accept()
        data = receiveall(client)

        try:
            result = bfeval(data)
        except EvalError as error:
            result = "<ERROR: {}>".format(error)

        client.send(result)
        client.close()

