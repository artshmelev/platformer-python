# -*- coding: utf-8 -*-

from platformer_python.net.channel import CALLBACK_PREFIX
from platformer_python.net.endpoint import EndPoint


connection = EndPoint()


class ConnectionListener(object):

    def connect(self, *args, **kwargs):
        connection.Connect(*args, **kwargs)
        self.pump()

    def pump(self):
        for data in connection.queue:
            method = CALLBACK_PREFIX + data['action']
            if hasattr(self, method):
                getattr(self, method)(data)

    def send(self, data):
        connection.Send(data)
