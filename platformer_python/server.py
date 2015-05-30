#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import sys
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

    def __init__(self, log=None, *args, **kwargs):
        self.players = {}
        if log:
            self._log = log
        Server.__init__(self, *args, **kwargs)

    def _print_log(self):
        self._log.seek(0)
        self._log.truncate()
        for c1, c2 in self.players.items():
            addr1 = c1.addr[0] + ':' + str(c1.addr[1])
            addr2 = c2.addr[0] + ':' + str(c2.addr[1]) if c2 else 'None'
            self._log.write(addr1+' -- '+addr2+'<br>\n')
        self._log.flush()

    def Connected(self, channel, addr):
        print 'new connection:', channel.addr
        flag = True
        for c in self.channels[:-1]:
            if not self.players[c]:
                self.players[c] = channel
                self.players[channel] = c

                c.Send({'action': 'startgame'})
                channel.Send({'action': 'startgame'})

                flag = False
                break

        if flag:
            self.players[channel] = None
        self._print_log()

    def delete_channel(self, channel):
        print 'delete channel:', channel.addr

        if self.players[channel]:
            channel.Send({'action': 'endgame'})
            self.players[channel].Send({'action': 'endgame'})

            self.players[self.players[channel]] = None

        self.players.pop(channel)

        for i, c in enumerate(self.channels):
            if c == channel:
                del self.channels[i]
                break
        self._print_log()

    def send_hero(self, channel, data):
        if self.players[channel]:
            self.players[channel].Send({
                'action': 'gethero',
                'left': data['left'],
                'top': data['top'],
                'cur_frame': data['cur_frame']
            })

    def send_winner(self, channel, data):
        if self.players[channel]:
            self.players[channel].Send({'action': 'getwinner'})


def main():
    parser = argparse.ArgumentParser(description='Platformer-python server')
    parser.add_argument('--port', type=int, default=8000, help='port number')
    parser.add_argument('--logfile', type=str, default='', help='path to log file')
    parser.add_argument('--infofile', type=str, default='', help='path to info file')
    ns = parser.parse_args()

    log = None
    if ns.logfile:
        log = open(ns.logfile, 'w')

    if ns.infofile:
        try:
            info = open(ns.infofile, 'a')
            info.write(str(ns.port))
            info.flush()
        except:
            return

    delta = 1.0/180
    server = GameServer(localaddr=('0.0.0.0', ns.port), log=log)
    while True:
        server.pump()
        try:
            time.sleep(delta)
        except:
            if ns.infofile:
                try:
                    info.seek(-len(str(ns.port)), 2)
                    info.truncate()
                    info.close()
                except:
                    pass
            if ns.logfile:
                log.close()
            return


if __name__ == '__main__':
    main()
