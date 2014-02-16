"""
Copyright (c) 2014, Sam Dodrill
All rights reserved.

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

    1. The origin of this software must not be misrepresented; you must not
    claim that you wrote the original software. If you use this software
    in a product, an acknowledgment in the product documentation would be
    appreciated but is not required.

    2. Altered source versions must be plainly marked as such, and must not be
    misrepresented as being the original software.

    3. This notice may not be removed or altered from any source
    distribution.
"""

NAME="Web App"
DESC="A web frontend to Cod"

import cherrypy
import json
import sys
from threading import Thread

thread = None

def initModule(cod):
    global thread

    thread = RunThread(cod)
    thread.start()

    cherrypy.config.update({'server.socket_port': 9996,
        'server.socket_host': '0.0.0.0', 'engine.autoreload_on': False})

    access_log = cherrypy.log.access_log
    for handler in tuple(access_log.handlers):
        access_log.removeHandler(handler)

def destroyModule(cod):
    global thread

    cherrypy.server.stop()

    del thread

class RunThread(Thread):
    def __init__(self, cod):
        Thread.__init__(self)
        self.cod = cod

    def run(self):
        self.cod.log("Started webserver", "WEB")
        cherrypy.quickstart(CodWebApp(self.cod))

class CodWebApp(object):
    def __init__(self, cod):
        self.cod = cod

    def index(self):
        cherrypy.response.headers['Content-Type'] = 'text/plain'

        replies = []

        replies.append("| Nick | User | Host | Gecos | Channels |\n")
        replies.append("|:---- |:---- |:---- |:----- |:-------- |\n")

        for uid in self.cod.clients:
            client = self.cod.clients[uid]

            try:
                replies.append("| %s | %s | %s | %s | %s |\n" %
                        (client.nick, client.user, client.host, client.gecos,
                            ", ".join([x.name for x in client.channels])))
            except AttributeError:
                pass

        replies.append("\n\n")

        replies.append("| Channel name | Ops |\n")
        replies.append("|:------------ |:--- |\n")

        for chname in self.cod.channels:
            channel = self.cod.channels[chname]

            ops = []

            for uid in channel.clients:
                chancli = channel.clients[uid]

                if "@" in chancli.prefix:
                    ops.append(chancli.client.nick)

            if ops == [] or len(channel.clients) == 0:
                continue

            replies.append("| %s | %s |\n" % (channel.name, " ".join(ops)))

        replies.append("\n\n")

        replies.append("| Channel name | Modes | TS | Population | Nicks |\n")
        replies.append("|:------------ |:----- |:-- |:---------- |:----- |\n")

        for chname in self.cod.channels:
            channel = self.cod.channels[chname]

            nicks = []

            if len(channel.clients) == 0:
                continue

            for client in channel.clients:
                client = channel.clients[client].client

                if client.nick in nicks:
                    self.cod.servicesLog("Wtf: duplicate client %s" % client.nick)

                try:
                    nicks.append("%s%s" % (channel.clients[client].prefix, client.nick))
                except:
                    nicks.append(client.nick)

            replies.append("| %s | %s | %s | %d | %s |\n" %
                    (chname, channel.modes, channel.ts, len(nicks), " ".join(nicks)))

        return replies
    index.exposed = True

