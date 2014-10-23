# -*- coding: utf-8 -*-

import asyncore
import socket

from platformer_python.net.channel import Channel


class EndPoint(Channel):

    def __init__(self):
        self.queue = []

    def Connect(self, address=None):
        if address:
            self.address = address
        else:
            self.address = ('127.0.0.1', 8000)

        try:
            Channel.__init__(self)
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.connect(self.address)
        except socket.error, e:
            self.queue.append({'action': 'error', 'error': e.args[1]})

    def pump(self):
        Channel.pump(self)
        self.queue = []
        asyncore.poll(map=self._map)

    def Connected(self):
        self.queue.append({'action': 'connected'})

    def Close(self):
        self.close()
        self.queue.append({'action': 'disconnected'})

    def Error(self, error):
        self.queue.append({'action': 'error', 'error': error})

    def Network_(self, data):
        self.queue.append(data)
