# -*- coding: utf-8 -*-

import asynchat
import json
import sys


CALLBACK_PREFIX = 'Network_'


class Channel(asynchat.async_chat):

    endchars = '\0---\0'

    def __init__(self, sock=None, addr=None, server=None):
        asynchat.async_chat.__init__(self, sock)
        self.addr = addr
        self._server = server
        self._ibuffer = ''
        self.set_terminator(self.endchars)
        self.sendqueue = []

    def collect_incoming_data(self, data):
        self._ibuffer += data

    def found_terminator(self):
        data = json.loads(self._ibuffer)
        self._ibuffer = ''

        if type(dict()) == type(data) and 'action' in data:
            method = CALLBACK_PREFIX + data['action']
            for m in (method, CALLBACK_PREFIX):
                if hasattr(self, m):
                    getattr(self, m)(data)
        else:
            raise Exception('There is no such action: %s' % data)

    def pump(self):
        for data in self.sendqueue:
            asynchat.async_chat.push(self, data)
        self.sendqueue = []

    def Send(self, data):
        out = json.dumps(data) + self.endchars
        self.sendqueue.append(out)
        return len(out)

    def handle_connect(self):
        if hasattr(self, 'Connected'):
            self.Connected()
        else:
            print 'Unhandled Connected()'

    def handle_error(self):
        try:
            self.close()
        except:
            pass

        if hasattr(self, 'Error'):
            self.Error(sys.exc_info()[1])
        else:
            asynchat.async_chat.handle_error(self)

    def handle_close(self):
        if hasattr(self, 'Close'):
            self.Close()
        else:
            asynchat.async_chat.handle_close(self)
