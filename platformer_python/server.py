#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

from platformer_python.net.channel import Channel
from platformer_python.net.server import Server


class ClientChannel(Channel):

    def Close(self):
        self._server.delete_channel(self)
        self.close()

    def Network_sendhero(self, data):
        self._server.send_hero(self, data)

    def Network_sendwinner(self, data):
        self._server.send_winner(self, data)


class GameServer(Server):

    ChannelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)

    def Connected(self, channel, addr):
        num_channels = len(self.channels)
        if num_channels == 1 or num_channels == 2:
            print 'new connection:', channel.addr
            if num_channels == 2:
                for c in self.channels:
                    c.Send({'action': 'startgame'})
        else:
            print 'Connection refused. Two players have already connected.'

    def delete_channel(self, channel):
        print 'delete channel:', channel.addr
        for c in self.channels:
            c.Send({'action': 'endgame'})

        for i, c in enumerate(self.channels):
            if c == channel:
                del self.channels[i]
                break

    def send_hero(self, channel, data):
        for c in self.channels:
            if c != channel:
                c.Send({
                    'action': 'gethero',
                    'left': data['left'],
                    'top': data['top'],
                    'cur_frame': data['cur_frame']
                })

    def send_winner(self, channel, data):
        for c in self.channels:
            if c != channel:
                c.Send({'action': 'getwinner'})


def main():
    delta = 1.0/180
    server = GameServer(localaddr=('0.0.0.0', int(8000)))
    while True:
        server.pump()
        time.sleep(delta)


if __name__ == '__main__':
    main()
