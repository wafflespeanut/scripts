# Parse the "messages.htm" file in your Facebook data and put them
# into a JSON file for analysis (I just wanted to review my history)
# I (personally) think that HTMLParser is very inefficient, but well,
# it's available in all python distributions...

from HTMLParser import HTMLParser
from datetime import datetime as dt
from timeit import default_timer as timer

import os, sys, contextlib


class FacebookDataParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.username = None
        self.current_participants = None
        self.repetition = 0
        self.message = ''
        self.current_transcript = []
        self.stack = []
        self.parsed = {}

        self.count = 0
        self.timer = timer()
        self.last_time = self.timer
        self.total_time = 0

        self.set_user = False
        self.get_participant = False
        self.get_talker = False
        self.get_time = False

    def handle_starttag(self, tag, attrs):
        self.stack.append(tag)
        if tag == 'div':
            for name, value in attrs:
                if name == 'class':
                    if not self.username and value == 'contents':
                        self.set_user = True
                    elif value == 'thread':
                        self.get_participant = True
        elif tag == 'span':
            for name, value in attrs:
                if name == 'class':
                    if value == 'user':
                        self.get_talker = True
                    elif value == 'meta':
                        self.get_time = True

    def handle_endtag(self, tag):
        tag = self.stack.pop()
        if tag == 'p':
            self.current_transcript += [self.message]
            self.message = ''   # ignore this and you'll probably crash your PC
            self.parsed[self.current_participants].append(self.current_transcript)
        elif tag == 'body':
            print '\n\nTotal time: %s s' % round(self.total_time, 3)

    def handle_data(self, data):
        data = data.strip()

        if self.set_user and self.stack[-1] == 'h1':
            self.username = data
            self.set_user = False

        elif self.get_participant:
            users = data.split(', ')
            if self.username in users:
                users.remove(self.username)

            self.current_participants = ', '.join(users)
            if self.current_participants in self.parsed:
                self.current_participants += '-%d' % self.repetition
                self.repetition += 1
            self.parsed[self.current_participants] = []
            self.get_participant = False

            self.timer = timer()
            interval = self.timer - self.last_time
            self.total_time += interval
            self.last_time = self.timer
            if self.count:
                print ' (%s s)' % round(interval, 3)
            sys.stdout.write('%s. %s' % (self.count + 1, self.current_participants))
            sys.stdout.flush()
            self.count += 1

        elif self.get_talker:
            self.current_transcript = [data]
            self.get_talker = False

        elif self.get_time:
            timestamp = dt.strptime(data, '%A, %d %B %Y at %H:%M UTC+05:30')
            self.current_transcript += [timestamp]
            self.get_time = False

        elif self.stack and self.stack[-1] == 'p':
            self.message += data.decode('utf-8')

    def handle_charref(self, ref):
        self.handle_entityref("#" + ref)

    def handle_entityref(self, ref):
        self.handle_data(self.unescape("&%s;" % ref))


def parse_data(path):
    with open(path, 'r') as in_fd, \
         contextlib.closing(FacebookDataParser()) as parser:
        parser.feed(in_fd.read())
        return parser.parsed
