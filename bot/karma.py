import json
import logging
import re

logger = logging.getLogger(__name__)

class Karma(object):
    def __init__(self, name):
        self.name = name
        self.negative = 0
        self.positive = 0
    def get_karma(self):
        return self.positive - self.negative
    def add(self):
       self.positive = self.positive + 1
    def remove(self):
       self.negative = self.negative + 1
    def to_string(self):
        return "Karma for " + self.name + ": " + str(self.get_karma()) + " with " + str(self.positive) + " positive and " + str(self.negative) + " negative"

class KarmaHandler(object):
    def __init__(self, msg_writer):
        self.msg_writer = msg_writer
        self.karma = {}

    def is_karma(self, msg_txt):
        return msg_txt.endswith(("++", "--", "+-", "-+"))

    def help(self):
        return "Add ++, --, -+, +- at the end of a text to give karma. Do !karma [text] to get the current karma"

    def get_karma(self, name):
        txt = ""
        if name not in self.karma:
            return "No karma for " + name
        else:
            return self.karma[name].to_string()

    def handle(self, channel, msg_txt):
        name=msg_txt[0:-2]
        action=msg_txt[-2:]
        if name not in self.karma:
            self.karma[name] = Karma(name)
        if "+" in action:
            self.karma[name].add()
        if "-" in action:
            self.karma[name].remove()
