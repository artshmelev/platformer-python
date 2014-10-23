# -*- coding: utf-8 -*-

import asyncore
import socket

from platformer_python.net.channel import Channel


class Server(asyncore.dispatcher):

    ChannelClass = Channel

    def __init__(self, localaddr=('127.0.0.1', 8000), listeners=5):
        asyncore.dispatcher.__init__(self)

        self.channels = []
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.set_reuse_addr()
        self.bind(localaddr)
        self.listen(listeners)

    def handle_accept(self):
        sock, addr = self.accept()

        self.channels.append(self.ChannelClass(sock, addr, self))
        if hasattr(self, 'Connected'):
            self.Connected(self.channels[-1], addr)

    def pump(self):
        for c in self.channels:
            c.pump()
        asyncore.poll(map=self._map)
