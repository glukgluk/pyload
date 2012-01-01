# -*- coding: utf-8 -*-
from time import time

from module.utils import uniqify

class EventManager:
    def __init__(self, core):
        self.core = core
        self.clients = []

    def newClient(self, uuid):
        self.clients.append(Client(uuid))

    def clean(self):
        for n, client in enumerate(self.clients):
            if client.lastActive + 30 < time():
                del self.clients[n]

    def getEvents(self, uuid):
        events = []
        validUuid = False
        for client in self.clients:
            if client.uuid == uuid:
                client.lastActive = time()
                validUuid = True
                while client.newEvents():
                    events.append(client.popEvent().toList())
                break
        if not validUuid:
            self.newClient(uuid)
            events = [ReloadAllEvent("queue").toList(), ReloadAllEvent("collector").toList()]
        return uniqify(events, repr)

    def addEvent(self, event):
        for client in self.clients:
            client.addEvent(event)

    def dispatchEvent(self, *args):
        pass


class Client:
    def __init__(self, uuid):
        self.uuid = uuid
        self.lastActive = time()
        self.events = []

    def newEvents(self):
        return len(self.events) > 0

    def popEvent(self):
        if not len(self.events):
            return None
        return self.events.pop(0)

    def addEvent(self, event):
        self.events.append(event)
